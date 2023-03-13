from typing import Optional

# Pydantic
from pydantic import BaseModel
from pydantic import Field


class Indicator(BaseModel):

    name: str = Field(..., min_length=1, example="RSI")
    value: float = Field(..., gt=0, example=12212)
    unix_time: int = Field(..., example=1673316847, gt=0)

    class Config:
        orm_mode = True


class UpdateIndicator(BaseModel):

    name: Optional[str] = Field(None, min_length=1, example="RSI")
    value: Optional[float] = Field(None, gt=0, example=12212)
    unix_time: Optional[int] = Field(None, example=1673316847, gt=0)

    class Config:
        orm_mode = True
