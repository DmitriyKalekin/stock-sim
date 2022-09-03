from app.models.order_book import OrderBook
from app.models.players_crowd import PlayersCrowd
from app.dto.order.res import Order
from app.models.consts import OrderEType, OrderEClass, OrderEStatus
from pydantic import BaseModel, Field, validator, condecimal
import decimal


# instance of stock
stock_sigleton = None



class PlayerNotExistException(Exception):
    pass


# Singleton!!!!
class Stock:
    def __init__(self):
        self.t = 0
        self.order_book = OrderBook(self)  # Composition
        self.players_crowd = PlayersCrowd(self.t)
        self.price = 0
        self.volume = 0
        self.min_bet_usdt = 10
        self.ohlc_history = dict()
        self.volume_history = dict()
        self.fee = 0.05 * 0.01
        self.earn = 0

    @classmethod
    def get_singleton_instance(cls):
        global stock_sigleton
        if not stock_sigleton:
            stock_sigleton = Stock()
        return stock_sigleton

    # def on_tick(self, t):
    #     self.t = t

    def on_orders_executed(self, order1: Order, order2: Order, price, volume):
        player1 = self.players_crowd.get_player_by_id(order1.player_id)
        player2 = self.players_crowd.get_player_by_id(order2.player_id)

        money = volume * price
        self.earn = money * decimal.Decimal(self.fee)
        self.price = price
        self.volume = volume + decimal.Decimal(self.volume)
        money -= self.earn

        if order1.type == OrderEType.BID:
            player1.asset += volume
            player1.money -= money
            player2.asset -= volume
            player2.money += money
        elif order1.type == OrderEType.ASK:
            player1.asset -= volume
            player1.money += money
            player2.asset += volume
            player2.money -= money

        self.update_ohlc_history(price)
        self.update_volume_history(volume)

    def update_ohlc_history(self, price):
        if self.t not in self.ohlc_history:
            self.ohlc_history[self.t] = {"t": self.t, "Open": price, "High": price, "Low": price, "Close": price}
        self.ohlc_history[self.t]["Close"] = price
        self.ohlc_history[self.t]["High"] = max(price, self.ohlc_history[self.t]["High"])
        self.ohlc_history[self.t]["Low"] = min(price, self.ohlc_history[self.t]["High"])

    def update_volume_history(self, volume):
        if self.t not in self.volume_history:
            self.volume_history[self.t] = {"t": self.t, "Volume": 0}
        self.volume_history[self.t]["Volume"] += volume

    # ------- Order book Composition methods (Delegation) -------------
    def create_order(self, order_dict: dict) -> Order:
        # Игрок, для которого делается ордер - должен быть на бирже
        player_id = order_dict["player_id"]
        player = self.players_crowd.get_player_by_id(player_id)
        if not bool(player):
            raise PlayerNotExistException(f"Can't place order. Unknown Player with player_id=`{player_id}` not found")
        return self.order_book.create_order(order_dict, player_id)

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
