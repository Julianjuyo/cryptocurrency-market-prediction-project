# python
from typing import Optional
from enum import Enum
from uuid import UUID
from datetime import datetime


# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import root_validator


class IntervalAsset(Enum):
    minute = "minute",
    hour = "hour",
    day = "day"


class Asset_type(Enum):
    Cryptocurrency = "Cryptocurrency",
    stock = "stock",
    bond = "bond",
    comodity = "comodity",
    etf = "etf"

#TODO Revisar si si tengo que pasar la fecha ahí


class Asset(BaseModel):

    id: UUID = Field(..., example="00000"),
    created_at: datetime = Field(
        default=datetime.now(), example="2023-01-29 17:08:55.249278"),
    updated_at: Optional[datetime] = Field(
        default=None, example="2023-01-29 17:08:55.249278"),
    symbol: str = Field(..., example="BTC/USD", min_length=1, max_length=25),
    base_asset: str = Field(..., example="BTC", min_length=1, max_length=20),
    quote_asset: str = Field(..., example="USD", min_length=1, max_length=20),
    interval: IntervalAsset = Field(..., example=IntervalAsset.minute),
    asset_type: Asset_type = Field(..., example=Asset_type.Cryptocurrency)


    class Config:
        validate_assignment = True

    @root_validator
    def number_validator(cls, values):
        values["updated_at"] = datetime.now()
        return values

class UpdateAsset(Asset):

    id: UUID = Field(..., example="00000"),
    updated_at: Optional[datetime] = Field(
        default=None, example="2023-01-29 17:08:55.249278"),
    symbol: str = Field(..., example="BTC/USD", min_length=1, max_length=25),
    base_asset: str = Field(..., example="BTC", min_length=1, max_length=20),
    quote_asset: str = Field(..., example="USD", min_length=1, max_length=20),
    interval: IntervalAsset = Field(..., example=IntervalAsset.minute),
    asset_type: Asset_type = Field(..., example=Asset_type.Cryptocurrency)


    class Config:
        validate_assignment = True

    @root_validator
    def number_validator(cls, values):
        values["updated_at"] = datetime.now()
        return values

