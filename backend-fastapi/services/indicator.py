from models.price import Price as PriceModel
from models.indicator import Indicator as IndicatorModel

from services.utils import convert_unix_time


from schemas.indicator import Indicator
from schemas.indicator import UpdateIndicator

from sqlalchemy.orm import joinedload
from sqlalchemy import and_
from sqlalchemy import desc


class IndicatorService():

    def __init__(self, db) -> None:
        self.db = db

    def get_all_indicators_by_price_id(self, price_id: str):

        price = self.db.query(PriceModel).filter(
            PriceModel.id == price_id).first()

        if not price:
            return {'error message': "The Price with the given id was not found"}

        result = self.db.query(IndicatorModel).filter(
            IndicatorModel.price_id == price_id).all()

        return result

    def get_indicator_by_unix_time_and_by_price_id(self, price_id: str, unix_time: int):

        price = self.db.query(PriceModel).filter(
            PriceModel.id == price_id).first()

        if not price:
            return {'error message': "The Price with the given id was not found"}

        result = self.db.query(IndicatorModel).filter(and_(
            IndicatorModel.unix_time == unix_time, IndicatorModel.price_id == price_id)).first()

        if not result:
            return {'error message': "The Indicator with the given unixTIme was not found"}

        return result

    def get_indicators_between_unix_time_and_by_price_id(self,  price_id: str, unix_time_start: int,  unix_time_end: int):

        price = self.db.query(PriceModel).filter(
            PriceModel.id == price_id).first()

        if not price:
            return {'error message': "The Price with the given id was not found"}

        result = self.db.query(IndicatorModel).filter(and_(
            IndicatorModel.unix_time >= unix_time_start, IndicatorModel.unix_time <= unix_time_end, IndicatorModel.price_id == price_id)).all()

        if not result:
            return {'error message': 'The Indicatorse with the given unix_time time range was not found'}

        return result

    def get_indicator_by_price_id(self, price_id: str, indicator_id: str):

        price = self.db.query(PriceModel).filter(
            PriceModel.id == price_id).first()

        if not price:
            return {'error message': "The Price with the given id was not found"}

        result = self.db.query(IndicatorModel).filter(
            IndicatorModel.id == indicator_id).first()

        if not result:
            return {'error message': "The Indicator with the given id was not found"}

        return result

    def get_last_indicator_by_price_id(self, price_id: str):

        price = self.db.query(PriceModel).filter(
            PriceModel.id == price_id).first()

        if not price:
            return {'error message': "The Price with the given id was not found"}

        result = self.db.query(IndicatorModel).filter(
            IndicatorModel.price_id == price_id).order_by(desc(IndicatorModel.unix_time)).first()

        if not result:
            return {'error message': "The Indicator with the given id was not found"}

        return result

    def create_indicator_to_price(self, price_id: str, indicator: Indicator):

        price = self.db.query(PriceModel).filter(
            PriceModel.id == price_id).first()

        if not price:
            return {'error message': "The Price with the given id was not found"}
        
        if price.unix_time != indicator.unix_time:

            return {'error message': 'The Price unixTime and the indicator UnixTime are not the same'}
        

        result = self.db.query(IndicatorModel).filter(and_(
            IndicatorModel.unix_time == price.unix_time, IndicatorModel.price_id == price_id)).first()

        if result and result.unix_time == indicator.unix_time and result.price_id == price_id:

            return {'error message': 'The unixTime with the given indicator already exists'}


        new_indicator = IndicatorModel(**indicator.dict())
        new_indicator.price_id = price_id
        utc_datetime, gmt5_datetime = convert_unix_time(
            new_indicator.unix_time)
        new_indicator.date_time_utc = utc_datetime
        new_indicator.date_time_gmt_5 = gmt5_datetime

        self.db.add(new_indicator)
        self.db.commit()

        result_new_indicator = self.db.query(IndicatorModel).filter(

            IndicatorModel.id == new_indicator.id).first()

        return result_new_indicator

    def update_indicator_to_price(self, price_id: str, indicator_id: str, indicator_update: UpdateIndicator):

        price = self.db.query(PriceModel).filter(
            PriceModel.id == price_id).first()

        if not price:
            return {'error message': "The Price with the given id was not found"}

        indicator = self.db.query(IndicatorModel).filter(
            IndicatorModel.id == indicator_id).first()

        if not indicator:
            return {'error message': "The Indicator with the given id was not found"}

        for key, value in vars(indicator_update).items():
            setattr(indicator, key, value) if value else None

        utc_datetime, gmt5_datetime = convert_unix_time(
            indicator_update.unix_time)
        indicator.date_time_utc = utc_datetime
        indicator.date_time_gmt_5 = gmt5_datetime

        self.db.commit()

        result = self.db.query(IndicatorModel).filter(

            IndicatorModel.id == indicator_id).first()

        return result

    def delete_indicator_to_price(self, price_id: str, indicator_id: str):

        price = self.db.query(PriceModel).filter(
            PriceModel.id == price_id).first()

        if not price:
            return {'error message': "The Price with the given id was not found"}

        indicator = self.db.query(IndicatorModel).filter(
            IndicatorModel.id == indicator_id).first()

        if not indicator:
            return {'error message': "The Indicator with the given id was not found"}

        self.db.query(IndicatorModel).filter(
            IndicatorModel.id == indicator_id).delete()
        self.db.commit()

        return {"message", "deleted successfully"}
