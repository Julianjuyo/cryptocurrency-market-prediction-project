from models.asset import Asset as AssetModel
from models.price import Price as PriceModel
from services.utils import convert_unix_time

from schemas.price import Price
from schemas.price import UpdatePrice

from sqlalchemy.orm import joinedload
from sqlalchemy import and_


class PriceService():

    def __init__(self, db) -> None:
        self.db = db

    def get_all_prices_by_asset_id(self, asset_id: str):

        asset = self.db.query(AssetModel).filter(
            AssetModel.id == asset_id).first()

        if not asset:
            return {'error message': 'The Asset with the given id was not found'}

        result = self.db.query(PriceModel).filter(
            PriceModel.asset_id == asset_id).all()

        return result

    def get_price_by_asset_id(self, asset_id: str, price_id: str):

        asset = self.db.query(AssetModel).filter(
            AssetModel.id == asset_id).first()

        if not asset:
            return {'error message': 'The Asset with the given id was not found'}

        result = self.db.query(PriceModel).filter(
            PriceModel.id == price_id).first()

        if not result:
            return {'error message': "The Price with the given id was not found"}

        return result

    def get_price_by_unix_time_and_by_asset_id(self,  asset_id: str, unix_time: int):

        asset = self.db.query(AssetModel).filter(
            AssetModel.id == asset_id).first()

        if not asset:
            return {'error message': 'The Asset with the given id was not found'}

        result = self.db.query(PriceModel).filter(and_(
            PriceModel.unix_time == unix_time, PriceModel.asset_id == asset_id)).first()

        if not result:
            return {'error message': 'The Price with the given unix_time was not found'}

        return result

    def get_prices_between_unix_time_and_by_asset_id(self,  asset_id: str, unix_time_start: int,  unix_time_end: int):

        asset = self.db.query(AssetModel).filter(
            AssetModel.id == asset_id).first()

        if not asset:
            return {'error message': 'The Asset with the given id was not found'}

        result = self.db.query(PriceModel).filter(and_(
            PriceModel.unix_time >= unix_time_start, PriceModel.unix_time <= unix_time_end, PriceModel.asset_id == asset_id)).all()

        if not result:
            return {'error message': 'The Prices with the given unix_time time range was not found'}

        return result

    def create_price_to_Asset(self, asset_id: str, price: Price):

        asset = self.db.query(AssetModel).filter(
            AssetModel.id == asset_id).first()

        if not asset:
            return {'error message': 'The Asset with the given id was not found'}

        result = self.db.query(PriceModel).filter(and_(
            PriceModel.unix_time == price.unix_time, PriceModel.asset_id == asset_id)).first()

        if result and result.unix_time == price.unix_time and str(result.asset_id) == asset_id:
            return {'error message': 'The Price in the give unix_time allready exists'}

        new_price = PriceModel(**price.dict())

        new_price.asset_id = asset_id
        utc_datetime, gmt5_datetime = convert_unix_time(new_price.unix_time)
        new_price.date_time_utc = utc_datetime
        new_price.date_time_gmt_5 = gmt5_datetime

        self.db.add(new_price)
        self.db.commit()

        result_new_price = self.db.query(PriceModel).filter(

            PriceModel.id == new_price.id).first()

        return result_new_price

    def update_price_to_asset(self, asset_id: str, price_id: str, price_update: UpdatePrice):

        asset = self.db.query(AssetModel).filter(
            AssetModel.id == asset_id).first()

        if not asset:
            return {'error message': 'The Asset with the given id was not found'}

        price = self.db.query(PriceModel).filter(
            PriceModel.id == price_id).first()

        if not price:
            return {'error message': "The Price with the given id was not found"}

        for key, value in vars(price_update).items():
            setattr(price, key, value) if value else None

        utc_datetime, gmt5_datetime = convert_unix_time(price_update.unix_time)
        price.date_time_utc = utc_datetime
        price.date_time_gmt_5 = gmt5_datetime

        self.db.commit()

        result = self.db.query(PriceModel).filter(

            PriceModel.id == price_id).first()

        return result

    def delete_price_to_asset(self, asset_id: str, price_id: str):

        asset = self.db.query(AssetModel).filter(
            AssetModel.id == asset_id).first()

        if not asset:
            return {'error message': 'The Asset with the given id was not found'}

        price = self.db.query(PriceModel).filter(
            PriceModel.id == price_id).first()

        if not price:
            return {'error message': "The Price with the given id was not found"}

        self.db.query(PriceModel).filter(PriceModel.id == price_id).delete()
        self.db.commit()

        return {"message", "deleted successfully"}
