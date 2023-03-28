# Python
from typing import List

# FastAPI
from fastapi import APIRouter
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
    summary="Create a price to an Asset"
)
def create_price_to_Asset(price: Price, asset_id: str = Path()) -> Price:

    result = PriceService(db.session).create_price_to_Asset(asset_id, price)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result_json)


@price_router.get(
    path='/assets/{asset_id}/prices/',
    tags=['prices'],
    response_model=List[Price],
    status_code=status.HTTP_200_OK,
    summary="Get all the prices of an asset")
def get_all_prices_by_asset_id(asset_id: str = Path(min_length=36, max_length=36)) -> List[Price]:

    result = PriceService(db.session).get_all_prices_by_asset_id(asset_id)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)


@price_router.get(
    path='/assets/{asset_id}/last_price/',
    tags=['prices'],
    response_model=Price,
    status_code=status.HTTP_200_OK,
    summary="Get the last price of an asset")
def get_last_price_by_asset_id(asset_id: str = Path(min_length=36, max_length=36)) -> Price:

    result = PriceService(db.session).get_last_price_by_asset_id(asset_id)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)


@price_router.get(
    path='/assets/{asset_id}/indicators_unix/',
    tags=['prices'],
    response_model=List[Price],
    status_code=status.HTTP_200_OK,
    summary="Get a Price with a given unixTime of an Asset")
def get_price_by_unix_time_and_by_asset_id(asset_id: str = Path(), unix_time: str = Query(min_length=2)) -> Price:

    result = PriceService(db.session).get_price_by_unix_time_and_by_asset_id(
        asset_id, unix_time)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)


@price_router.get(
    path='/assets/{asset_id}/indicators_unix_between/',
    tags=['prices'],
    response_model=List[Price],
    status_code=status.HTTP_200_OK,
    summary="Get all the prices between Dates of an asset")
def get_prices_between_unix_time_and_by_asset_id(asset_id: str = Path(), unix_time_start: str = Query(min_length=2), unix_time_end: str = Query(min_length=2)) -> Price:

    result = PriceService(db.session).get_prices_between_unix_time_and_by_asset_id(
        asset_id, unix_time_start, unix_time_end)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)


@price_router.get(
    path='/assets/{asset_id}/prices/{price_id}',
    tags=['prices'],
    response_model=List[Price],
    status_code=status.HTTP_200_OK,
    summary="Get One price of an asset")
def get_price_by_asset_id(asset_id: str = Path(), price_id: str = Path()) -> Price:

    result = PriceService(db.session).get_price_by_asset_id(
        asset_id, price_id)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)


@price_router.put(
    path='/assets/{asset_id}/prices/{price_id}',
    tags=['prices'],
    response_model=List[Price],
    status_code=status.HTTP_200_OK,
    summary="Update a price of an asset")
def update_exchange(price: UpdatePrice, asset_id: str = Path(), price_id: str = Path()) -> Price:

    result = PriceService(db.session).update_price_to_asset(
        asset_id, price_id, price)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))


@price_router.delete(
    path='/assets/{asset_id}/prices/{price_id}',
    tags=['prices'],
    response_model=List[Price],
    status_code=status.HTTP_200_OK,
    summary="Delete a price of an asset")
def update_exchange(asset_id: str = Path(), price_id: str = Path()) -> Price:

    result = PriceService(db.session).delete_price_to_asset(asset_id, price_id)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
