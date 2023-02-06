# python
from typing import Optional
from enum import Enum
from uuid import UUID
from datetime import datetime

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import root_validator

# FastAPI
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query
from fastapi import Path
from fastapi import status
from fastapi import HTTPException

# App
# from middlewares.error_handler import ErrorHandler
# from config.database import engine, Base
# from routers.exchange import exchange_router

app = FastAPI()
app.title = "Crypto currency market prediction Tesis"
app.version = "0.0.1"


@app.get(path="/", tags=['home'])
async def home():
    return {"Cripto currency trading": "working"}
