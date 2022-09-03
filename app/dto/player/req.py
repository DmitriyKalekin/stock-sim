from pydantic import BaseModel, Field, validator, condecimal
from app.models.consts import OrderEType

class PlayerBase(BaseModel):
    name: str

    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "name": "Player001",
            }
        }
