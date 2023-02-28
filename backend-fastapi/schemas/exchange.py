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

    name: str = Field(..., example="Binance", min_length=1, max_length=100)

    class Config:
        orm_mode = True
