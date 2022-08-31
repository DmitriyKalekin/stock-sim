from pydantic import BaseModel, Field, validator, condecimal
from app.models.consts import EnumOrderClass, EnumOrderType


class OrderBase(BaseModel):
    player_id: str
    cls: EnumOrderClass
    type: EnumOrderType
    price: condecimal(gt=0, decimal_places=2) = None
    volume: condecimal(gt=0, decimal_places=6)

    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "player_id": "0001",
                "cls": EnumOrderClass.LIMIT,
                "type": EnumOrderType.BID,
                "price": 35.04,
                "volume": 13.02,
            }
        }
