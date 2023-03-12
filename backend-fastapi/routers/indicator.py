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

from schemas.indicator import Indicator
from schemas.indicator import UpdateIndicator
from services.indicator import IndicatorService
from models.indicator import Indicator as IndicatorModel


indicator_router = APIRouter()


@indicator_router.post(

    path='/prices/{price_id}/indicators/',
    tags=['indicators'],
    response_model=Indicator,
    status_code=status.HTTP_201_CREATED,
    summary="Create a indicator to an Price"
)
def create_indicator_to_Price(indicator: Indicator, price_id: str = Path(min_length=36,max_length=36)) -> Indicator:

    result = IndicatorService(
        db.session).create_indicator_to_Price(price_id, indicator)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result_json)


@indicator_router.get(
    path='/prices/{price_id}/indicators_unix/',
    tags=['indicators'],
    response_model=List[Indicator],
    status_code=status.HTTP_200_OK,
    summary="Get a Indicator with a given unixTime of an Price")
def get_indicator_by_unix_time_and_by_price_id(price_id: str = Path(min_length=36,max_length=36), unix_time: str = Query(min_length=2)) -> Indicator:

    result = IndicatorService(db.session).get_indicator_by_unix_time_and_by_price_id(
        price_id, unix_time)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)


@indicator_router.get(
    path='/prices/{price_id}/indicators_unix_between/',
    tags=['indicators'],
    response_model=List[Indicator],
    status_code=status.HTTP_200_OK,
    summary="Get all the indicators between Dates of an price")
def get_indicators_between_unix_time_and_by_price_id(price_id: str = Path(min_length=36,max_length=36), unix_time_start: str = Query(min_length=2), unix_time_end: str = Query(min_length=2)) -> Indicator:

    result = IndicatorService(db.session).get_indicators_between_unix_time_and_by_price_id(
        price_id, unix_time_start, unix_time_end)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)


@indicator_router.get(
    path='/prices/{price_id}/indicators/',
    tags=['indicators'],
    response_model=List[Indicator],
    status_code=status.HTTP_200_OK,
    summary="Get all the indicators of an price")
def get_all_indicators_by_price_id(price_id: str = Path(min_length=36,max_length=36)) -> List[Indicator]:

    result = IndicatorService(
        db.session).get_all_indicators_by_price_id(price_id)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)


@indicator_router.get(
    path='/prices/{price_id}/indicators/{indicator_id}',
    tags=['indicators'],
    response_model=List[Indicator],
    status_code=status.HTTP_200_OK,
    summary="Get One Inidicator of an price")
def get_indicator_by_price_id(price_id: str = Path(min_length=36,max_length=36), indicator_id: str = Path(min_length=36,max_length=36)) -> Indicator:

    result = IndicatorService(db.session).get_indicator_by_price_id(
        price_id, indicator_id)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)


@indicator_router.put(
    path='/prices/{price_id}/indicators/{indicator_id}',
    tags=['indicators'],
    response_model=List[Indicator],
    status_code=status.HTTP_200_OK,
    summary="Update a indicator of an price")
def update_exchange(indicator: UpdateIndicator, price_id: str = Path(min_length=36,max_length=36), indicator_id: str = Path(min_length=36,max_length=36)) -> Indicator:

    result = IndicatorService(db.session).update_indicator_to_price(
        price_id, indicator_id, indicator)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))


@indicator_router.delete(
    path='/prices/{price_id}/indicators/{indicator_id}',
    tags=['indicators'],
    response_model=List[Indicator],
    status_code=status.HTTP_200_OK,
    summary="Delete a indicator of an price")
def update_exchange(price_id: str = Path(min_length=36,max_length=36), indicator_id: str = Path(min_length=36,max_length=36)) -> Indicator:

    result = IndicatorService(db.session).delete_indicator_to_price(
        price_id, indicator_id)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
