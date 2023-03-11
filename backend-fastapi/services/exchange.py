from models.exchange import Exchange as ExchangeModel
from schemas.exchange import Exchange
from sqlalchemy.orm import joinedload


class ExchangeService():

    def __init__(self, db) -> None:
        self.db = db

    def get_exchanges(self):

        result = self.db.query(ExchangeModel).all()

        if (result == None):
            return {'error message': 'Theres no exchanges created'}

        return result

    def get_exchange(self, id: str):
        result = self.db.query(ExchangeModel).filter(
            ExchangeModel.id == id).first()

        if (result == None):
            return {'error message': "The exchange with the given id was not found"}

        return result

    def get_exchange_by_name(self, name):
        result = self.db.query(ExchangeModel).filter(
            ExchangeModel.name == name).options(joinedload(ExchangeModel.assets)).all()

        if (result == None):
            return {'error message': "The exchange with the given name was not found"}

        return result

    def create_exchange(self, exchange: Exchange):

        result = self.db.query(ExchangeModel).filter(
            ExchangeModel.name == exchange.name).all()

        if result:
            return {'error message': 'The Exchange allready exists'}

        new_exchange = ExchangeModel(**exchange.dict())
        self.db.add(new_exchange)
        self.db.commit()

        result = self.db.query(ExchangeModel).filter(
            ExchangeModel.id == new_exchange.id).first()

        return result

    def update_exchange(self, id: str, data: Exchange):

        exchange = self.db.query(ExchangeModel).filter(
            ExchangeModel.id == id).first()

        if (exchange == None):
            return {'error message': 'The exchange with the given id was not found'}

        exchange.name = data.name
        self.db.commit()

        result = self.db.query(ExchangeModel).filter(
            ExchangeModel.id == exchange.id).first()

        return result

    def delete_exchange(self, id: str):
        self.db.query(ExchangeModel).filter(ExchangeModel.id == id).delete()
        self.db.commit()
        return
