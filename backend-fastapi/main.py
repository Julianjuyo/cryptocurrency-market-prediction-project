# python
from dotenv import load_dotenv
import os

# Pydantic
from fastapi_sqlalchemy import DBSessionMiddleware, db

# FastAPI
from fastapi import FastAPI

# App
from routers.exchange import exchange_router
from routers.asset import asset_router
from routers.price import price_router

app = FastAPI()
app.title = "Crypto currency market prediction Tesis"
app.version = "0.0.1"

# Include all the routers
app.include_router(exchange_router)
app.include_router(asset_router)
app.include_router(price_router)


# connect to the database
load_dotenv(".env")
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.get(path="/", tags=['home'])
async def home():
    return {"Cripto currency trading": "working"}




