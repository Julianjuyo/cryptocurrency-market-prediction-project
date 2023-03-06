# Python
from typing import List
import json


# FastAPI
from fastapi import APIRouter
from fastapi import Body
from fastapi import Query
from fastapi import Path
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from fastapi_sqlalchemy import db


# From the app
from schemas.price import Price
from schemas.price import UpdatePrice
from services.price import PriceService
from models.price import Price as PriceModel


price_router = APIRouter()


@price_router.post(

    path='/assets/{asset_id}/prices/',
    tags=['prices'],
    response_model=Price,
    status_code=status.HTTP_201_CREATED,
    summary="Create a price to an Asset",
)
def create_price_to_Asset(price: Price, asset_id: str = Path()) -> Price:

    result = PriceService(db.session).create_price_to_Asset(asset_id, price)

    result_json = jsonable_encoder(result)

    if "error message" in result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result_json)
