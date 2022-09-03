from pydantic import BaseModel, Field, validator, condecimal
from app.models.consts import OrderEClass, OrderEType, OrderEStatus


class OrderId(BaseModel):
    order_id: str = Field(..., alias="order_id")


class Order(BaseModel):
    order_id: str = Field(..., alias="order_id")
    player_id: str
    ts: int
    type: OrderEType
    price: condecimal(gt=0, decimal_places=2) | OrderEClass = OrderEClass.MARKET
    volume: condecimal(ge=0, decimal_places=6)
    volume_start: condecimal(gt=0, decimal_places=6) = 0
    status: OrderEStatus = OrderEStatus.CREATED

    def __repr__(self):  # pragma: no cover
        return f"Order(T={self.type} P={self.price} sV={self.volume_start} cV={self.volume} S={self.status})"

    def __str__(self):  # pragma: no cover
        return f"Order(T={self.type} P={self.price} sV={self.volume_start} cV={self.volume} S={self.status})"

    def set_volume(self, volume):
        self.volume = volume

    def set_status(self, status):
        self.status = status

    class Config:
        orm_mode = True
        use_enum_values = True
        schema_extra = {
            "example": {
                "order_id": "000000000001",
                "player_id": "0001",
                "ts": 12314134133,
                "type": OrderEType.BID,
                "price": 35.04,
                "volume": 13.02,
                "status": OrderEStatus.CREATED
            }
        }


class OrderCollection(BaseModel):
    ts: int
    bids_cnt: int
    asks_cnt: int
    bids: list[Order]
    asks: list[Order]
