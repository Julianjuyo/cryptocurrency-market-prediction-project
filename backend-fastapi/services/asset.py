from models.asset import Asset as AssetModel
from models.exchange import Exchange as ExchangeModel
from schemas.asset import Asset
from schemas.asset import UpdateAsset
from sqlalchemy.orm import joinedload
from sqlalchemy import and_


class AssetService():

    def __init__(self, db) -> None:
        self.db = db

    def get_assets_by_exchange_id(self, exchange_id: str):

        exchange = self.db.query(ExchangeModel).filter(
            ExchangeModel.id == exchange_id).first()

        if (exchange == None):
            return {'error message': 'The exchange with the given id was not found'}

        result = self.db.query(AssetModel).filter(
            AssetModel.exchange_id == exchange_id).all()

        return result

    def get_asset_by_exchange_id(self,  exchange_id: str, asset_id: str):

        exchange = self.db.query(ExchangeModel).filter(
            ExchangeModel.id == exchange_id).first()

        if (exchange == None):
            return {'error message': "The exchange with the given id was not found"}

        result = self.db.query(AssetModel).filter(
            AssetModel.id == asset_id).first()

        if (result == None):
            return {'error message': "The exchange with the given id was not found"}

        return result

    def get_asset_by_symbol(self, symbol: str):

        result = self.db.query(AssetModel).filter(
            AssetModel.symbol == symbol).all()
        return result

    def create_asset_to_exchange(self, exchange_id: str,  asset: Asset):

        exchange = self.db.query(ExchangeModel).filter(
            ExchangeModel.id == exchange_id).first()

        if (exchange == None):
            return {'error message': 'The exchange with the given id was not found'}

        result = self.db.query(AssetModel).filter(and_(
            AssetModel.symbol == asset.symbol, AssetModel.exchange_id == exchange_id)).first()

        if result and result.symbol == asset.symbol and str(result.exchange_id) == exchange_id:
            return {'error message': 'The Asset allready exists'}

        new_asset = AssetModel(**asset.dict())

        new_asset.exchange_id = exchange_id

        self.db.add(new_asset)
        self.db.commit()

        result_new_asset = self.db.query(AssetModel).filter(
            AssetModel.id == new_asset.id).first()

        return result_new_asset

    def update_asset_to_exchange(self, exchange_id: str, asset_id: str, asset_update: UpdateAsset):

        exchange = self.db.query(ExchangeModel).filter(
            ExchangeModel.id == exchange_id).first()

        print(exchange)

        if (exchange == None):
            return {'error message': 'The exchange with the given id was not found'}

        asset = self.db.query(AssetModel).filter(
            AssetModel.id == asset_id).first()

        if not asset:
            return {'error message': 'The asset with the given id was not found'}

        for key, value in vars(asset_update).items():
            setattr(asset, key, value) if value else None

        self.db.commit()

        result = self.db.query(AssetModel).filter(
            AssetModel.id == asset_id).first()

        return result

    def delete_asset_to_exchange(self, exchange_id: str, asset_id: str):

        exchange = self.db.query(ExchangeModel).filter(
            ExchangeModel.id == exchange_id).first()

        print(exchange)

        if (exchange == None):
            return {'error message': 'The exchange with the given id was not found'}

        asset = self.db.query(AssetModel).filter(
            AssetModel.id == asset_id).first()

        if not asset:
            return {'error message': 'The asset with the given id was not found'}

        self.db.query(AssetModel).filter(AssetModel.id == asset_id).delete()
        self.db.commit()

        return {"message", "deleted successfully"}
