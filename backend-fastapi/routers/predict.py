# Python
from typing import List
from datetime import datetime, timezone



# FastAPI
from fastapi import APIRouter
from fastapi import Query
from fastapi import Path
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import db

from services.price import PriceService
from services.asset import AssetService
from services.indicator import IndicatorService
from services.predict import PredictService


from schemas.price import SimplifiedPrice



predict_router = APIRouter()


@predict_router.get(
    path='/predicts/{asset_id}/future_time/{future_time}',
    tags=['predicts'],
    response_model=List[SimplifiedPrice],

    status_code=status.HTTP_200_OK,
    summary="Predict future price for a given asset")
def predict_(asset_id: str = Path(min_length=36, max_length=36), future_time: str = Path(...,min_length=1, max_length=5))-> List[SimplifiedPrice]:

    unix_time_end = 1684626776

    serach_historic_data = PredictService(db.session).get_indicators_and_merge(asset_id, unix_time_end,future_time)

    try:
        # Convert dataframe to a list of SimplifiedPrice objects
        object_list = []
        for _, row in serach_historic_data.iterrows():
            obj = SimplifiedPrice(**row)
            object_list.append(obj)

        result_json = jsonable_encoder(object_list)
    
    except:
        result_json = jsonable_encoder(serach_historic_data)


    if "error message" in result_json:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

    return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)
