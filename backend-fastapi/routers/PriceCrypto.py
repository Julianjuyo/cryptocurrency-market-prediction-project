# # Python
# from typing import List
# import json


# # FastAPI
# from fastapi import APIRouter
# from fastapi import Body
# from fastapi import Query
# from fastapi import Path
# from fastapi import status
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse

# from fastapi_sqlalchemy import db


# # From the app
# from schemas.priceCrypto import PriceCrypto
# from schemas.priceCrypto import UpdateCrypto
# from services.priceCrypto import PriceCryptoService
# from models.priceCrypto import PriceCrypto as PriceCryptoModel


# price_crypto_router = APIRouter()


# @price_crypto_router.post(
#     path='/assets/{asset_id}/pricesCrypto',
#     tags=['pricesCrypto'],
#     response_model=PriceCrypto,
#     status_code=status.HTTP_201_CREATED,
#     summary="Create an Price Crypto to an Asset",

# )
# def create_price_crypto_to_asset(price_crypto: PriceCrypto, asset_id: str = Path()) -> PriceCrypto:


#     print("HOLAAAA")

#     result = PriceCryptoService(db.session).create_price_crypto_to_asset(
#         asset_id, price_crypto)

#     result_json = jsonable_encoder(result)

#     if "error message" in result:
#         return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

#     return JSONResponse(status_code=status.HTTP_201_CREATED, content=result_json)




# @price_crypto_router.get(
#     path='/assets/{asset_id}/pricesCrypto/',
#     tags=['pricesCrypto'],
#     response_model=List[PriceCrypto],
#     status_code=status.HTTP_200_OK,
#     summary=" get all the Prices from an asset"
# )
# def get_prices_crypto_by_asset_id(asset_id: str = Path()) -> List[PriceCrypto]:


#     print("HOLAAAA")

#     result = PriceCryptoService(
#         db.session).get_price_cryptos_by_asset_id(asset_id)

#     result_json = jsonable_encoder(result)

#     if "error message" in result:
#         return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result_json)

#     return JSONResponse(status_code=status.HTTP_200_OK, content=result_json)
