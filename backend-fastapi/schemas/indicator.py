from typing import Optional
from datetime import datetime
from uuid import UUID

# Pydantic
from pydantic import BaseModel
from pydantic import Field


class Indicator(BaseModel):

    name: str = Field(..., min_length=1, example="RSI")
    value: float = Field(..., gt=0, example=12212)
    unix_time: int = Field(..., example=1673316847, gt=0)
    price_id: UUID = Field(..., example="00000-00000-00000-00000")

    class Config:
        orm_mode = True


class UpdateIndicator(BaseModel):

    name: Optional[str] = Field(..., min_length=1, example="RSI")
    value: Optional[float] = Field(..., gt=0, example=12212)
    unix_time: Optional[int] = Field(..., example=1673316847, gt=0)
    price_id: Optional[UUID] = Field(..., example="00000-00000-00000-00000")

    class Config:
        orm_mode = True
