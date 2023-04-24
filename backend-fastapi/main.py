# python
from dotenv import load_dotenv
import os

# Pydantic
from fastapi_sqlalchemy import DBSessionMiddleware, db

# FastAPI
from fastapi import FastAPI  # , Depends
# from fastapi.security import OAuth2PasswordBearer


# App
from routers.exchange import exchange_router
from routers.asset import asset_router
from routers.price import price_router
from routers.indicator import indicator_router
from routers.predict import predict_router

app = FastAPI()
app.title = "Artificial Intelligence Techniques Applied to Cryptocurrency Market Prediction"
app.version = "0.0.1"

# Securiry Auth 2
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Include all the routers
app.include_router(exchange_router)
app.include_router(asset_router)
app.include_router(price_router)
app.include_router(indicator_router)
app.include_router(predict_router)


# connect to the database
load_dotenv(".env")
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.get(path="/", tags=["home"])
async def home():
    return {"Cripto currency trading": "working"}


# @app.get("/items/")
# async def read_items(token: str = Depends(oauth2_scheme)):
#     return {"token": token}

