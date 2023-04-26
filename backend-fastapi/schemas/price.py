

from typing import Optional

# Pydantic
from pydantic import BaseModel
from pydantic import Field


class Price(BaseModel):

    unix_time: int = Field(..., example=1673316847, ge=0,)
    open_price: float = Field(..., example=20000.2134, ge=0)
    close_price: float = Field(..., example=22000.214, ge=0)
    low_price: float = Field(..., example=19500.2, ge=0)
    high_price: float = Field(..., example=22500.3, ge=0)
    volume: float = Field(..., example=72.3, ge=0)
    qav: float = Field(..., example=10)
    num_trades: int = Field(..., example=10)
    taker_base_vol: float = Field(..., example=10)
    taker_quote_vol: float = Field(..., example=10)
    ignore: int = Field(..., example=10)

    class Config:
        orm_mode = True


class UpdatePrice(BaseModel):

    unix_time: Optional[int] = Field(None, example=1673316847, gt=0)
    open_price: Optional[float] = Field(None, example=20000, gt=0)
    close_price: Optional[float] = Field(None, example=22000, gt=0)
    low_price: Optional[float] = Field(None, example=19500, gt=0)
    high_price: Optional[float] = Field(None, example=22500, gt=0)
    volume: Optional[float] = Field(None, example=72372787812, gt=0)
    qav: Optional[float] = Field(None, example=10)
    num_trades: Optional[int] = Field(None, example=10)
    taker_base_vol: Optional[float] = Field(None, example=10)
    taker_quote_vol: Optional[float] = Field(None, example=10)
    ignore: Optional[int] = Field(None, example=10)

    class Config:
        orm_mode = True
