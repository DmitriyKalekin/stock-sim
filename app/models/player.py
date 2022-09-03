import random
from pydantic import BaseModel, Field, validator, condecimal
from app.models.consts import OrderEType

# class AgentsCollection:
#     def __init__(self, stock):
#         self.players = []
#         self.stock: Stock = stock
#         self.last_player_id = 0
#
#     def add_random_player(self):
#         self.last_player_id += 1
#         name = "Player#" + str(self.last_player_id).zfill(5)
#         p = Player(name, self.stock)
#         self.players.append(p)
#
#     def on_tick(self, t):
#         # clean bankrupts
#         self.players = [p for p in self.players if not p.can_buy() and not p.can_sell()]
#
#         for p in self.players:
#             p.on_tick(t)


class Player(BaseModel):
    player_id: str
    name: str
    asset: float = 0
    money: float = 0



    # def __init__(self, name, stock):
    #     self.name = name
    #     self.stock: Stock = stock
    #     self.orders_idx = []
    #     self.btc = 0.0
    #     self.usdt = 0.0
    #     self.forecast = (self.stock.price, self.stock.t)
    #     c = random.choice(["BTC", "USDT"])
    #     if c == "BTC":
    #         self.btc += 1
    #     if c == "USDT":
    #         self.usdt += 1000
    #     self.make_forecast(self.stock.t)
    #     return
    #
    # def __repr__(self):
    #     return f"Player<name={self.name}, btc={self.btc}, usdt={self.usdt}>"
    #
    # def make_forecast(self, t):
    #     horizon = random.choice(range(1, 20))
    #     way = random.choice([-1, 1])
    #     delta_percent = random.choice(range(1, 60)) / 100
    #     predicted_price = round(self.stock.price * (1 + delta_percent * way), 2)
    #     self.forecast = (predicted_price, t + horizon)
    #
    #     # Цена меньше его ожидания - значит, по большей цене лучше продавать - НАМЕРЕНИЕ
    #     if self.stock.price < predicted_price and self.can_sell():
    #         self.stock.add_order({
    #             "type": "ASK",
    #             "price": round(predicted_price, 2),
    #             "volume": self.btc
    #         })
    #
    #     # Сейчас цена больше его ожидания - значит по меньше цене готов покупать - НАМЕРЕНИЕ
    #     if self.stock.price > predicted_price and self.can_buy():
    #         self.stock.add_order({
    #             "type": "BID",
    #             "price": round(predicted_price, 2),
    #             "volume": self.btc
    #         })
    #     return
    #
    # def can_buy(self):
    #     return bool(self.usdt > self.stock.min_bet_usdt)
    #
    # def can_sell(self):
    #     return bool(self.btc * self.stock.price > self.stock.min_bet_usdt)
    #
    # def make_decision(self):
    #     predicted_price, predicted_t = self.forecast
    #
    #     if self.stock.price < predicted_price and self.can_buy():
    #         # time to buy
    #         rnd = random.random()
    #         want_spent_money = (self.usdt - self.stock.min_bet_usdt) * rnd + self.stock.min_bet_usdt
    #         if want_spent_money < 0 or want_spent_money > self.usdt:
    #             return
    #         wanted_volume = want_spent_money / self.stock.price
    #         self.stock.add_order({
    #             "type": "BID",
    #             "price": self.stock.price - 0.05,  # Хочу немного дешевле, чтобы продать по курсу
    #             "volume": round(wanted_volume, 6)
    #         })
    #
    #     elif self.stock.price > predicted_price and self.can_sell():
    #         # time to sell
    #         rnd = random.random()
    #         min_bet_btc = self.stock.min_bet_usdt / self.stock.price
    #         wanted_volume = (self.btc - 1) * rnd + min_bet_btc
    #         if wanted_volume > self.btc:
    #             wanted_volume = self.btc
    #         if wanted_volume < 0:
    #             return
    #         self.stock.add_order({
    #             "type": "ASK",
    #             "price": self.stock.price + 0.05,  # Хочу немного дороже, чтобы продать по курсу
    #             "volume": round(wanted_volume, 6)
    #         })
    #
    # def on_tick(self, t):
    #     predicted_price, predicted_t = self.forecast
    #     if t >= predicted_t:
    #         self.make_forecast(t)
