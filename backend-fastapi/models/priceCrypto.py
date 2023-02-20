from models.price import Price
from sqlalchemy import Column, Integer, Float


class PriceCrypto(Price):

    __tablename__ = "pricesCrypto"

    qav = Column(Float)
    num_trades = Column(Integer)
    taker_base_vol = Column(Float)
    taker_quote_vol = Column(Float)
    ignore = Column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": "pricesCrypto",
    }
