
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
from schemas.exchange import Exchange
from services.exchange import ExchangeService
from models.exchange import Exchange as ExchangeModel


exchange_router = APIRouter()


@exchange_router.post(
    path='/exchanges',
    tags=['exchanges'],
    response_model=Exchange,
    status_code=status.HTTP_201_CREATED,
    summary="Create a Exchange",
)
def create_exchange(exchange: Exchange) -> Exchange:

    result = ExchangeService(db.session).create_exchange(exchange)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result_json)


@exchange_router.get(
    path='/exchanges/',
    tags=['exchanges'],
    response_model=List[Exchange],

    status_code=status.HTTP_200_OK,
    summary="Get all the exchanges in the app")
def get_exchanges() -> List[Exchange]:

    result = ExchangeService(db.session).get_exchanges()

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)


@exchange_router.get(
    path='/exchanges/name/',
    tags=['exchanges'],
    response_model=List[Exchange],
    status_code=status.HTTP_200_OK,
    summary="Get exchanges by the name")
def get_exchange_by_name(name: str = Query(min_length=2, max_length=100)) -> List[Exchange]:

    result = ExchangeService(db.session).get_exchange_by_name(name)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)


@exchange_router.get(
    path='/exchanges/{id}',
    tags=['exchanges'],
    response_model=Exchange,
    status_code=status.HTTP_200_OK,
    summary="Get one Exchange by the id")
def get_exchange(id: str = Path(min_length=36, max_length=36)) -> Exchange:

    result = ExchangeService(db.session).get_exchange(id)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)


@exchange_router.put(
    path='/exchanges/{id}',
    tags=['exchanges'],
    response_model=Exchange,
    status_code=status.HTTP_200_OK,
    summary="Update a Exchange")
def update_exchange(id: str, exchange: Exchange) -> Exchange:

    result = ExchangeService(db.session).update_exchange(id, exchange)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)


@exchange_router.delete(
    path='/exchanges/{id}',
    tags=['exchanges'],
    response_model=Exchange,
    status_code=status.HTTP_200_OK,
    summary="Delete a Exchange")
def delete_exchange(id: str) -> Exchange:

    result = ExchangeService(db.session).get_exchange(id)

    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)
