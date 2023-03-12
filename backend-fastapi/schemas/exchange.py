
# Pydantic
from pydantic import BaseModel
from pydantic import Field


class Exchange(BaseModel):

    name: str = Field(..., example="Binance", min_length=1, max_length=100)

    class Config:
        orm_mode = True
