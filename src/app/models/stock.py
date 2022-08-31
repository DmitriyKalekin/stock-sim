from app.models.order_book import OrderBook
from app.models.players_crowd import PlayersCrowd
from app.models.dao.dao_order import Order
from app.models.consts import EnumOrderType, EnumOrderClass, EnumOrderStatus
import numpy as np

# instance of stock
stock_sigleton = None


class PlayerNotExistException(Exception):
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

    def execute_matching_orders(self, order: Order):
        book = self.order_book.asks if order.type == EnumOrderType.BID else self.order_book.bids
        sign = 1 if order.type == EnumOrderType.BID else -1
        closed = []
        for contr_order in book:
            if np.sign(contr_order.price - order.price) == sign:
                break
            # По этой цене пока совершается сделка -
            self.price = min(contr_order.price, order.price)
            d = contr_order.volume - order.volume
            if d >= 0:
                # Сможем за один контр-ордер из стакана погасить наш новый ордер?
                self.volume += order.volume
                contr_order.set_volume(d)
                order.set_status(EnumOrderStatus.CLOSED)
                order.set_volume(0)
                closed.append(order)
                if d == 0:
                    # Мы случайно угадали с объемом - закрыли еще и ордер их книги
                    contr_order.set_status(EnumOrderStatus.CLOSED)
                    closed.append(contr_order)
                break
            else:
                # Не сможем, будем выскребать по нескольку ордеров в стакане
                self.volume += contr_order.volume
                order.set_volume(-d)
                contr_order.set_volume(0)
                contr_order.set_status(EnumOrderStatus.CLOSED)
                closed.append(contr_order)
        # чистим то, что выполнено
        for del_ordr in closed:
            a = self.delete_order(del_ordr.order_id)
        return

    # ------- Order book Composition methods (Delegation) -------------
    def add_order(self, order: dict):
        # Игрок, для которого делается ордер - должен быть на бирже
        player_id = order["player_id"]
        player = self.players_crowd.get_player_by_id(player_id)
        if not bool(player):
            raise PlayerNotExistException(f"Can't place order. Unknown Player with player_id=`{player_id}` not found")
        order_obj = self.order_book.add_order(order)
        self.execute_matching_orders(order_obj)
        return order_obj

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
