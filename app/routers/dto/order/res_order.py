from pydantic import BaseModel, Field, validator, condecimal
from app.models.consts import EnumOrderClass, EnumOrderType, EnumOrderStatus

class OrderId(BaseModel):
    order_id: str = Field(..., alias="order_id")


class Order(BaseModel):
    order_id: str = Field(..., alias="order_id")
    player_id: str
    ts: int
    cls: EnumOrderClass = EnumOrderClass.LIMIT
    type: EnumOrderType
    price: condecimal(gt=0, decimal_places=2)
    volume: condecimal(gt=0, decimal_places=6)
    status: EnumOrderStatus = EnumOrderStatus.ACTIVE

    class Config:
        orm_mode = True
        use_enum_values = True
        schema_extra = {
            "example": {
                "order_id": "000000000001",
                "player_id": "0001",
                "ts": 12314134133,
                "cls": EnumOrderClass.LIMIT,
                "type": EnumOrderType.BID,
                "price": 35.04,
                "volume": 13.02,
                "status": EnumOrderStatus.ACTIVE
            }
        }


class OrderCollection(BaseModel):
    ts: int
    bids_cnt: int
    asks_cnt: int
    bids: list[Order]
    asks: list[Order]
