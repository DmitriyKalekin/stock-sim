from enum import Enum


class EnumOrderClass(str, Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"

    def __repr__(self):
        return self.value  # pragma: no cover


class EnumOrderType(str, Enum):
    BID = "BID"
    ASK = "ASK"

    def __repr__(self):
        return self.value  # pragma: no cover


class EnumOrderStatus(str, Enum):
    ACTIVE = "ACTIVE"  # размещен
    PAID = "PAID"  # частично оплачен
    CLOSED = "CLOSED"  # полностью оплачен

    # CANCELED = "CANCELED"

    def __repr__(self):
        return self.value  # pragma: no cover
