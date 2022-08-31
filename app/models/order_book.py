from app.models.dao.dao_order import Order
from app.models.consts import EnumOrderClass, EnumOrderType, EnumOrderStatus
import numpy as np


class OrderBook:
    def __init__(self, t):
        self.t = t
        self.last_id = 0
        self.market: list[Order] = []
        self.bids: list[Order] = []  # OrderedDict better
        self.asks: list[Order] = []  # OrderedDict better

    def get_new_id(self):
        self.last_id += 1
        return str(self.last_id).zfill(12)

    def _sort_order_book(self, page=None):
        if not page or page == EnumOrderType.BID:
            self.bids = sorted(self.bids, key=lambda order: (-order.price, order.ts))

        if not page or page == EnumOrderType.BID:
            self.asks = sorted(self.asks, key=lambda order: (order.price, order.ts))
        return

    def add_order(self, order_dict: dict) -> Order:
        order = Order(
            order_id=self.get_new_id(),
            ts=self.t,
            **order_dict,
        )
        # if order.cls == EnumOrderClass.MARKET:
        #     self.market.append(order)
        #     return order

        if order.cls == EnumOrderClass.LIMIT:
            storage_to_put = self.bids if order.type == EnumOrderType.BID else self.asks
            storage_to_put.append(order)
            self._sort_order_book(page=order.type)
        return order

    def get_order(self, order_id: str) -> Order | bool:
        # markets_filter = [m for m in self.market if m.order_id == order_id]
        # if markets_filter:
        #     return markets_filter[0]
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
        # if order.cls == EnumOrderClass.MARKET:
        #     self.market = [m for m in self.market if m.order_id != order_id]
        #     return True
        # -- LIMIT orders must be sorted ----
        if order.type == EnumOrderType.BID:
            self.bids = [bid for bid in self.bids if bid.order_id != order_id]
        elif order.type == EnumOrderType.ASK:
            self.asks = [ask for ask in self.asks if ask.order_id != order_id]
        self._sort_order_book(page=order.type)
        return True
