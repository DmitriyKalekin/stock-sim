from pydantic import BaseModel, Field, validator, condecimal
from app.models.consts import OrderEClass, OrderEType


class OrderBase(BaseModel):
    player_id: str
    type: OrderEType
    price: condecimal(gt=0, decimal_places=2) | OrderEClass = OrderEClass.MARKET
    volume: condecimal(gt=0, decimal_places=6)

    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "player_id": "0001",
                "type": OrderEType.BID,
                "price": 35.04,
                "volume": 13.02,
            }
        }
