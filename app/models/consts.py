from enum import Enum


class OrderEClass(str, Enum):
    MARKET = "MARKET"
    OTHER = "OTHER"

    def __repr__(self):
        return self.value  # pragma: no cover


class OrderEType(str, Enum):
    BID = "BID"
    ASK = "ASK"

    def __repr__(self):
        return self.value  # pragma: no cover


class OrderEStatus(str, Enum):
    CREATED = "CREATED"  # размещен
    EXECUTED = "EXECUTED"  # частично оплачен
    CLOSED = "CLOSED"  # полностью оплачен
    ERROR = "ERROR"  # Не смогли исполнить (нет объема)

    # CANCELED = "CANCELED"

    def __repr__(self):
        return self.value  # pragma: no cover
