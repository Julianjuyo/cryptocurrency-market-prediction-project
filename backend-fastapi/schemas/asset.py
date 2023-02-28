# python
from typing import Optional
from enum import Enum
from uuid import UUID
from datetime import datetime

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import root_validator


class IntervalAsset(str, Enum):
    minute = "minute",
    hour = "hour",
    day = "day"


class Asset_type(str, Enum):
    Cryptocurrency = "Cryptocurrency",
    stock = "stock",
    bond = "bond",
    comodity = "comodity",
    etf = "etf"


class Asset(BaseModel):

    symbol: str = Field(..., example="BTC/USD", min_length=1, max_length=25)
    base_asset: str = Field(..., example="BTC", min_length=1, max_length=20)
    quote_asset: str = Field(..., example="USD", min_length=1, max_length=20)
    interval: IntervalAsset = Field(..., example=IntervalAsset.minute)
    asset_type: Asset_type = Field(..., example=Asset_type.Cryptocurrency)

    class Config:
        orm_mode = True


class UpdateAsset(BaseModel):

    symbol: Optional[str] = Field(None, example="BTC/USD",
                                  min_length=1, max_length=25)
    base_asset: Optional[str] = Field(None,
                                      example="BTC", min_length=1, max_length=20)
    quote_asset: Optional[str] = Field(None,
                                       example="USD", min_length=1, max_length=20)
    interval: Optional[IntervalAsset] = Field(None,
                                              example=IntervalAsset.minute)
    asset_type: Optional[Asset_type] = Field(None,
                                             example=Asset_type.Cryptocurrency)
    exchange_id: Optional[UUID] = Field(
        None, example="00000-00000-00000-00000")

    class Config:
        orm_mode = True
