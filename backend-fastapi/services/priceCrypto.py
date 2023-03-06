# from models.asset import Asset as AssetModel
# from models.priceCrypto import PriceCrypto as PriceCryptoModel
# from schemas.priceCrypto import PriceCrypto
# from schemas.priceCrypto import UpdateCrypto
# from sqlalchemy.orm import joinedload
# from sqlalchemy import and_


# class PriceCryptoService():

#     def __init__(self, db) -> None:
#         self.db = db

#     def get_price_cryptos_by_asset_id(self, asset_id: str):

#         asset = self.db.query(AssetModel).filter(
#             AssetModel.id == asset_id).first()

#         if (asset == None):
#             return {'error message': 'The asset with the given id was not found'}

#         result = self.db.query(PriceCryptoModel).filter(
#             PriceCryptoModel.asset_id == asset_id).all()

#         return result

#     def create_price_crypto_to_asset(self, asset_id: str,  price_crypto: PriceCrypto):

#         asset = self.db.query(AssetModel).filter(
#             AssetModel.id == asset_id).first()


#         if (asset == None):
#             return {'error message': 'The asset with the given id was not found'}

#         result = self.db.query(PriceCrypto).filter(and_(
#             AssetModel.unix_time == price_crypto.unix_time, AssetModel.asset_id == asset_id)).first()

#         if result and result.unix_time == price_crypto.unix_time and str(result.asset_id) == asset_id:
#             return {'error message': 'The Price allready exists'}

#         new_price_crypto = AssetModel(**price_crypto.dict())

#         new_price_crypto.asset_id = asset_id

#         self.db.add(new_price_crypto)
#         self.db.commit()

#         return price_crypto
