from typing import Optional

# Pydantic
from pydantic import BaseModel
from pydantic import Field


class Indicator(BaseModel):

    # name: str = Field(..., min_length=1, example="RSI")
    # value: Optional[float] = Field(None, example=12212)

    gold_price : Optional[float] = Field(None, example=12212)
    silver_price : Optional[float] = Field(None, example=12212)
    natural_gas_price : Optional[float] = Field(None, example=12212)
    cotton_price : Optional[float] = Field(None, example=12212)
    coffee_price : Optional[float] = Field(None, example=12212)
    sugar_price : Optional[float] = Field(None, example=12212)
    cocoa_price : Optional[float] = Field(None, example=12212)
    rice_price : Optional[float] = Field(None, example=12212)
    corn_price : Optional[float] = Field(None, example=12212)
    wheat_price : Optional[float] = Field(None, example=12212)
    soybean_price : Optional[float] = Field(None, example=12212)
    oats_price : Optional[float] = Field(None, example=12212)
    spy500_price : Optional[float] = Field(None, example=12212)
    dow_jones_price : Optional[float] = Field(None, example=12212)
    nasdaq_price : Optional[float] = Field(None, example=12212)
    russell_2000_price : Optional[float] = Field(None, example=12212)
    us_10_year_treasury_price : Optional[float] = Field(None, example=12212)
    us_5_year_treasury_price : Optional[float] = Field(None, example=12212)
    us_2_year_treasury_price : Optional[float] = Field(None, example=12212)
    usbond_price : Optional[float] = Field(None, example=12212)

    unix_time: int = Field(..., example=1673316847, gt=0)

    class Config:
        orm_mode = True


class UpdateIndicator(BaseModel):

    # name: Optional[str] = Field(None, min_length=1, example="RSI")
    # value: Optional[float] = Field(None, example=12212)

    gold_price : Optional[float] = Field(None, example=12212)
    silver_price : Optional[float] = Field(None, example=12212)
    natural_gas_price : Optional[float] = Field(None, example=12212)
    cotton_price : Optional[float] = Field(None, example=12212)
    coffee_price : Optional[float] = Field(None, example=12212)
    sugar_price : Optional[float] = Field(None, example=12212)
    cocoa_price : Optional[float] = Field(None, example=12212)
    rice_price : Optional[float] = Field(None, example=12212)
    corn_price : Optional[float] = Field(None, example=12212)
    wheat_price : Optional[float] = Field(None, example=12212)
    soybean_price : Optional[float] = Field(None, example=12212)
    oats_price : Optional[float] = Field(None, example=12212)
    spy500_price : Optional[float] = Field(None, example=12212)
    dow_jones_price : Optional[float] = Field(None, example=12212)
    nasdaq_price : Optional[float] = Field(None, example=12212)
    russell_2000_price : Optional[float] = Field(None, example=12212)
    us_10_year_treasury_price : Optional[float] = Field(None, example=12212)
    us_5_year_treasury_price : Optional[float] = Field(None, example=12212)
    us_2_year_treasury_price : Optional[float] = Field(None, example=12212)
    usbond_price : Optional[float] = Field(None, example=12212)


    unix_time: Optional[int] = Field(None, example=1673316847, gt=0)

    class Config:
        orm_mode = True
