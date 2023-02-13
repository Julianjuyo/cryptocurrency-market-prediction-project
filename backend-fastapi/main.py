# python
from typing import Optional
from enum import Enum
from uuid import UUID
from datetime import datetime
from dotenv import load_dotenv
import os
import sys


# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import root_validator
from fastapi_sqlalchemy import DBSessionMiddleware, db

# FastAPI
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query
from fastapi import Path
from fastapi import status
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# App
from routers.exchange import exchange_router


app = FastAPI()
app.title = "Crypto currency market prediction Tesis"
app.version = "0.0.1"

# Include all the routers
app.include_router(exchange_router)

# connect to the database
load_dotenv(".env")
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.get(path="/", tags=['home'])
async def home():
    return {"Cripto currency trading": "working"}
