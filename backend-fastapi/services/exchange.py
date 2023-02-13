from models.exchange import Exchange as ExchangeModel
from schemas.exchange import Exchange


class ExchangeService():

    def __init__(self, db) -> None:
        self.db = db

    def get_exchanges(self):

        result = self.db.query(ExchangeModel).all()
        return result

    def get_exchange(self, id: str):
        result = self.db.query(ExchangeModel).filter(
            ExchangeModel.id == id).first()
        return result

    def get_exchange_by_name(self, name):
        result = self.db.query(ExchangeModel).filter(
            ExchangeModel.name == name).all()
        return result

    def create_exchange(self, exchange: Exchange):
        new_exchange = ExchangeModel(**exchange.dict())
        self.db.add(new_exchange)
        self.db.commit()
        return

    def update_exchange(self, id: str, data: Exchange):

        exchange = self.db.query(ExchangeModel).filter(
            ExchangeModel.id == id).first()
        exchange.name = data.name
        self.db.commit()
        return

    def delete_exchange(self, id: str):
        self.db.query(ExchangeModel).filter(ExchangeModel.id == id).delete()
        self.db.commit()
        return
