from typing import Optional
from uuid import UUID

# Pydantic
from pydantic import BaseModel
from pydantic import Field


class PriceCrypto(BaseModel):

    # id: UUID = Field(..., example="00000"),

    unix_time: int = Field(..., example=1673316847, gt=0)
    # date_time_utc: datetime = Field(..., example="2023-01-29 17:08:55.249278"),
    # price_date_gmt_5: datetime = Field(..., example="2023-01-29 12:08:55.249278"),
    open_price: float = Field(..., example=20000, gt=0)
    close_price: float = Field(..., example=22000, gt=0)
    high_price: float = Field(..., example=22500, gt=0)
    low_price: float = Field(..., example=19500, gt=0)
    volume: int = Field(..., example=72372787812, gt=0)
    asset_id: UUID = Field(..., example="00000-00000-00000-00000")

    qav: int = Field(..., example=10)
    num_trades: int = Field(..., example=10)
    taker_base_vol: float = Field(..., example=10)
    taker_quote_vol: float = Field(..., example=10)
    ignore: int = Field(..., example=10)

    class Config:
        orm_mode = True


class UpdateCrypto(BaseModel):

    unix_time: Optional[int] = Field(..., example=1673316847, gt=0)
    open_price: Optional[float] = Field(..., example=20000, gt=0)
    close_price: Optional[float] = Field(..., example=22000, gt=0)
    high_price: Optional[float] = Field(..., example=22500, gt=0)
    low_price: Optional[float] = Field(..., example=19500, gt=0)
    volume: Optional[int] = Field(..., example=72372787812, gt=0)
    asset_id: Optional[UUID] = Field(..., example="00000-00000-00000-00000")
    qav: Optional[int] = Field(..., example=10)
    num_trades: Optional[int] = Field(..., example=10)
    taker_base_vol: Optional[float] = Field(..., example=10)
    taker_quote_vol: Optional[float] = Field(..., example=10)
    ignore: Optional[int] = Field(..., example=10)

    class Config:
        orm_mode = True
