from pydantic import BaseModel, Field, validator, condecimal
from app.models.consts import EnumOrderType


class MessageError(BaseModel):
    message: str




