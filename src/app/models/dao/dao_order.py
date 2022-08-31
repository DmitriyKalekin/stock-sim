from pydantic import BaseModel, Field, validator, condecimal
from app.models.consts import EnumOrderClass, EnumOrderType, EnumOrderStatus


class Order(BaseModel):
    order_id: str = Field(..., alias="order_id")
    player_id: str
    ts: int
    cls: EnumOrderClass
    type: EnumOrderType
    price: condecimal(gt=0, decimal_places=2)
    volume: condecimal(gt=0, decimal_places=6)
    status: EnumOrderStatus = EnumOrderStatus.ACTIVE
    start_volume: condecimal(gt=0, decimal_places=6) = None

    class Config:
        orm_mode = True

    def __repr__(self): # pragma: no cover
        if self.start_volume is None:
            self.start_volume = self.volume
        return f"Order(T={self.type} P={self.price} sV={self.start_volume} cV={self.volume} S={self.status})"

    def __str__(self): # pragma: no cover
        if self.start_volume is None:
            self.start_volume = self.volume
        return f"Order(T={self.type} P={self.price} sV={self.start_volume} cV={self.volume} S={self.status})"

    def set_volume(self, volume):
        if self.start_volume is None:
            self.start_volume = self.volume
        self.volume = volume

    def set_status(self, status):
        self.status = status

