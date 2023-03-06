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
