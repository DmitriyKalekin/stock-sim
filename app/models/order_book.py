from app.dto.order.res import Order
from app.models.consts import OrderEClass, OrderEType, OrderEStatus


class OrderBook:
    def __init__(self, t):
        self.t = t
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

    def add_order(self, order: Order):
        if order.price == OrderEClass.MARKET:
            raise ValueError(f"cannot add market order to book {order}")
        storage_to_put = self.bids if order.type == OrderEType.BID else self.asks
        storage_to_put.append(order)
        self._sort_order_book(book=order.type)
        return

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
            "ts": self.t,
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
