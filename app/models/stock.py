from app.models.order_book import OrderBook
from app.models.players_crowd import PlayersCrowd
from app.dto.order.res import Order
from app.models.consts import OrderEType, OrderEClass, OrderEStatus

# instance of stock
stock_sigleton = None


class PlayerNotExistException(Exception):
    pass


class MarketOrderNotExecutableException(Exception):
    pass


# Singleton!!!!
class Stock:
    def __init__(self):
        self.t = 0
        self.order_book = OrderBook(self.t)  # Composition
        self.players_crowd = PlayersCrowd(self.t)
        self.price = 20_000
        self.volume = 0
        self.min_bet_usdt = 10

    @classmethod
    def get_singleton_instance(cls):
        global stock_sigleton
        if not stock_sigleton:
            stock_sigleton = Stock()
        return stock_sigleton

    # def on_tick(self, t):
    #     self.t = t

    def execute_matching_orders(self, order: Order) -> bool:
        book, covered_volume = self.order_book.select_matching(order)
        if order.price == OrderEClass.MARKET and covered_volume < order.volume:
            order.set_status(OrderEStatus.ERROR)
            msg = f"Market volume `{covered_volume}` less than order.volume = `{order.volume}`"
            raise MarketOrderNotExecutableException(msg)

        closed = []
        for contr_order in book:
            # По этой цене пока совершается сделка -
            if order.price == OrderEClass.MARKET:
                self.price = contr_order.price
            else:
                self.price = min(contr_order.price, order.price)
            d = contr_order.volume - order.volume
            if d >= 0:
                # Сможем за один контр-ордер из стакана погасить наш новый ордер?
                self.volume += order.volume
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
                break
            else:
                # Не сможем, будем выскребать по нескольку ордеров в стакане
                self.volume += contr_order.volume
                # Наш ордер частично погашен
                order.set_status(OrderEStatus.EXECUTED)
                order.set_volume(-d)
                # А в стакане - полностью закрыт
                contr_order.set_volume(0)
                contr_order.set_status(OrderEStatus.CLOSED)
                closed.append(contr_order)
        # чистим то, что выполнено
        for del_ordr in closed:
            a = self.delete_order(del_ordr.order_id)
        return True

    # ------- Order book Composition methods (Delegation) -------------
    def create_order(self, order_dict: dict) -> Order:
        # Игрок, для которого делается ордер - должен быть на бирже
        player_id = order_dict["player_id"]
        player = self.players_crowd.get_player_by_id(player_id)
        if not bool(player):
            raise PlayerNotExistException(f"Can't place order. Unknown Player with player_id=`{player_id}` not found")
        order = Order(
            order_id=self.order_book.get_new_id(),
            player_id=player.player_id,
            ts=self.t,
            type=order_dict["type"],
            price=order_dict["price"],
            volume=order_dict["volume"],
            volume_start=order_dict["volume"],
            status=OrderEStatus.CREATED,
        )
        self.execute_matching_orders(order)
        # Рыночные ордера мы не можем добавить в книгу
        if order.price == OrderEClass.MARKET:
            return order
        # Если ордер исполнен в руке - в книгу тоже не добавляется
        if order.status not in [OrderEStatus.CREATED, OrderEStatus.EXECUTED]:
            return order
        self.order_book.add_order(order)
        return order

    def get_order(self, order_id: str):
        return self.order_book.get_order(order_id)

    def get_order_book(self):
        return self.order_book.get_order_book()

    def delete_order(self, order_id: str) -> bool:
        return self.order_book.delete_order(order_id)

    # ------- PlayersCrowd Composition methods (Delegation) -------------
    def add_player(self, player: dict):
        return self.players_crowd.add_player(player)

    def get_player_by_id(self, player_id: str):
        return self.players_crowd.get_player_by_id(player_id)

    def get_players(self):
        return self.players_crowd.get_players()

    def delete_player(self, player_id: str) -> bool:
        return self.players_crowd.delete_player(player_id)
