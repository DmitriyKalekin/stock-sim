from app.dto.order.res import Order
from app.models.consts import OrderEClass, OrderEType, OrderEStatus

class MarketOrderNotExecutableException(Exception):
    pass

class OrderBook:
    def __init__(self, stock):
        self.stock = stock
        self.last_id = 0
        self.bids: list[Order] = []  # OrderedDict better
        self.asks: list[Order] = []  # OrderedDict better

    def get_new_id(self):
        self.last_id += 1
        return str(self.last_id).zfill(12)

    def _sort_order_book(self, book: OrderEType = None):
        if not book or book == OrderEType.BID:
            self.bids = sorted(self.bids, key=lambda order: (-order.price, order.ts))

        if not book or book == OrderEType.ASK:
            self.asks = sorted(self.asks, key=lambda order: (order.price, order.ts))
        return

    def execute_matching_orders(self, order: Order) -> bool:
        price = 0

        book, covered_volume = self.select_matching(order)
        if order.price == OrderEClass.MARKET and covered_volume < order.volume:
            order.set_status(OrderEStatus.ERROR)
            msg = f"Market volume `{covered_volume}` less than order.volume = `{order.volume}`"
            raise MarketOrderNotExecutableException(msg)

        closed = []
        for contr_order in book:
            # По этой цене пока совершается сделка -
            if order.price == OrderEClass.MARKET:
                price = contr_order.price
            else:
                price = min(contr_order.price, order.price)
            d = contr_order.volume - order.volume
            if d >= 0:
                # Сможем за один контр-ордер из стакана погасить наш новый ордер?
                volume = order.volume
                #  этот ордер частично погашен
                contr_order.set_volume(d)
                contr_order.set_status(OrderEStatus.EXECUTED)
                #  а наш полностью
                order.set_status(OrderEStatus.CLOSED)
                order.set_volume(0)
                closed.append(order)
                if d == 0:
                    # Мы случайно угадали с объемом - закрыли еще и ордер их книги
                    contr_order.set_status(OrderEStatus.CLOSED)
                    closed.append(contr_order)
                self.stock.on_orders_executed(order, contr_order, price, volume)
                break
            else:
                # Не сможем, будем выскребать по нескольку ордеров в стакане
                volume = contr_order.volume
                # Наш ордер частично погашен
                order.set_status(OrderEStatus.EXECUTED)
                order.set_volume(-d)
                # А в стакане - полностью закрыт
                contr_order.set_volume(0)
                contr_order.set_status(OrderEStatus.CLOSED)
                closed.append(contr_order)
                self.stock.on_orders_executed(order, contr_order, price, volume)
        # чистим то, что выполнено
        for del_ordr in closed:
            a = self.delete_order(del_ordr.order_id)
        return True

    def create_order(self, order_dict: dict, player_id) -> Order:
        order = Order(
            order_id=self.get_new_id(),
            player_id=player_id,
            ts=self.stock.t,
            type=order_dict["type"],
            price=order_dict["price"],
            volume=order_dict["volume"],
            volume_start=order_dict["volume"],
            status=OrderEStatus.CREATED,
        )
        self.execute_matching_orders(order)
        # Рыночный ордер исполняется сразу - без добавления
        if order.price == OrderEClass.MARKET:
            return order
        # Если ордер исполнен в руке - в книгу тоже не добавляется
        if order.status in [OrderEStatus.CLOSED, OrderEStatus.ERROR]:
            return order
        storage_to_put = self.bids if order.type == OrderEType.BID else self.asks
        storage_to_put.append(order)
        self._sort_order_book(book=order.type)
        return order

    def select_matching(self, order: Order) -> tuple[list[Order], float]:
        book = self.asks if order.type == OrderEType.BID else self.bids
        selected_volume = 0
        selected_orders = []
        for book_order in book:
            if order.price != OrderEClass.MARKET:
                if (order.type == OrderEType.BID and book_order.price > order.price) or (
                        order.type == OrderEType.ASK and book_order.price < order.price):
                    continue
            selected_volume += book_order.volume
            selected_orders.append(book_order)
            if selected_volume >= order.volume:
                break
        return selected_orders, selected_volume

    def get_order(self, order_id: str) -> Order | bool:
        bids_filter = [bid for bid in self.bids if bid.order_id == order_id]
        if bids_filter:
            return bids_filter[0]
        asks_filter = [ask for ask in self.asks if ask.order_id == order_id]
        if asks_filter:
            return asks_filter[0]
        return False

    def get_order_book(self):
        return {
            "ts": self.stock.t,
            "bids_cnt": len(self.bids),
            "asks_cnt": len(self.asks),
            "bids": self.bids,
            "asks": self.asks
        }

    def delete_order(self, order_id: str) -> bool:
        order = self.get_order(order_id)
        if not bool(order):
            return False
        if order.type == OrderEType.BID:
            self.bids = [bid for bid in self.bids if bid.order_id != order_id]
        elif order.type == OrderEType.ASK:
            self.asks = [ask for ask in self.asks if ask.order_id != order_id]
        self._sort_order_book(book=order.type)
        return True
