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
from schemas.asset import Asset
from schemas.asset import UpdateAsset
from services.asset import AssetService
# from models.asset import Asset as AssetModel


asset_router = APIRouter()


@asset_router.post(
    path='/exchanges/{exchange_id}/asset',
    tags=['assets'],
    response_model=Asset,
    status_code=status.HTTP_201_CREATED,
    summary="Create an Asset to a Exchnage",
)
def create_asset_to_exchange(asset: Asset, exchange_id: str = Path(min_length=36,max_length=36)) -> Asset:

    result = AssetService(db.session).create_asset_to_exchange(
        exchange_id, asset)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result_json)


@asset_router.get(
    path='/exchanges/{exchange_id}/asset/',
    tags=['assets'],
    response_model=List[Asset],

    status_code=status.HTTP_200_OK,
    summary="Get all the assets of a exchange ")
def get_assets_by_exchange_id(exchange_id: str = Path(min_length=36,max_length=36)) -> List[Asset]:

    result = AssetService(db.session).get_assets_by_exchange_id(exchange_id)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)


@asset_router.get(
    path='/exchanges/{exchange_id}/asset_symbol',
    tags=['assets'],
    response_model=Asset,
    status_code=status.HTTP_200_OK,
    summary="Get Assets by the symbol ")
def get_asset_by_symbol(symbol: str = Query(min_length=2)) -> List[Asset]:

    result = AssetService(db.session).get_asset_by_symbol(symbol)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)


@asset_router.get(
    path='/exchanges/{exchange_id}/asset/{asset_id}',
    tags=['assets'],
    response_model=Asset,
    status_code=status.HTTP_200_OK,
    summary="Get One Asset from a exchange ")
def get_asset_by_exchange_id(exchange_id: str = Path(min_length=36,max_length=36), asset_id: str = Path(min_length=36,max_length=36)) -> Asset:

    result = AssetService(db.session).get_asset_by_exchange_id(
        exchange_id, asset_id)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)


@asset_router.put(
    path='/exchanges/{exchange_id}/asset/{asset_id}',
    tags=['assets'],
    response_model=UpdateAsset,
    status_code=status.HTTP_200_OK,
    summary="Update an Asset from a Exchange")
def update_exchange(asset: UpdateAsset, exchange_id: str = Path(min_length=36,max_length=36), asset_id: str = Path(min_length=36,max_length=36)) -> Asset:

    result = AssetService(db.session).update_asset_to_exchange(
        exchange_id, asset_id, asset)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))


@asset_router.delete(
    path='/exchanges/{exchange_id}/asset/{asset_id}',
    tags=['assets'],
    response_model=Asset,
    status_code=status.HTTP_200_OK,
    summary="Delete a Exchange")
def delete_exchange(exchange_id: str = Path(min_length=36,max_length=36), asset_id: str = Path(min_length=36,max_length=36)) -> Asset:

    result = AssetService(db.session).delete_asset_to_exchange(
        exchange_id, asset_id)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)
