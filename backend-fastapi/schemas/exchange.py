# python
from typing import Optional
from enum import Enum
from uuid import UUID
from datetime import datetime


# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import root_validator


class Exchange(BaseModel):

    id: UUID = Field(..., example="00000"),
    name: str = Field(..., example="Binance", min_length=1, max_length=100),
    created_at: Optional[datetime] = Field(
        default=datetime.now(), example="2023-01-29 17:08:55.249278"),
        
    updated_at: Optional[datetime] = Field(
        default=datetime.now(), example="2023-01-29 17:08:55.249278")

    class Config:
        validate_assignment = True

    @root_validator
    def number_validator(cls, values):
        values["updated_at"] = datetime.now()
        return values



class UpdateExchange(Exchange):

    id: UUID = Field(..., example="00000"),
    name: str = Field(..., example="Binance", min_length=1, max_length=c)

    class Config:
        validate_assignment = True

    @root_validator
    def number_validator(cls, values):
        values["updated_at"] = datetime.now()
        return values
