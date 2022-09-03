from pydantic import BaseModel, Field, validator, condecimal
from app.models.consts import OrderEType


class MessageError(BaseModel):
    message: str




