from pydantic import BaseModel, Field, validator, condecimal
from app.models.consts import EnumOrderType

class PlayerId(BaseModel):
    player_id: str = Field(..., alias="player_id")


class Player(BaseModel):
    player_id: str = Field(..., alias="player_id")
    name: str

    class Config:
        orm_mode = True
        use_enum_values = True
        schema_extra = {
            "example": {
                "player_id": "Player001",
                "name": "John Doe",
            }
        }


class PlayersCollection(BaseModel):
    ts: int
    count: int
    players: list[Player]
