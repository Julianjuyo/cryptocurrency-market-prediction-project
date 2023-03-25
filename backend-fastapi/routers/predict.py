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


predict_router = APIRouter()


@predict_router.get(
    path='/predicts/{asset_id}',
    tags=['predicts'],
    status_code=status.HTTP_200_OK,
    summary="Get all the prices of an asset")
def get_all_prices_by_asset_id(asset_id: str = Path(min_length=36, max_length=36)) :

    # result = PriceService(db.session).get_all_prices_by_asset_id(asset_id)

    result = {"date":"2023-03-12T17:44:00.673514+00:00","close_price": 35000}

    


    result_json = jsonable_encoder(result)

    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)
