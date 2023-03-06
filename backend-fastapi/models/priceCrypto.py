from models.price import Price
from models.indicator import Indicator
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid


class PriceCrypto(Price):

    __tablename__ = "pricesCrypto"

    id = Column(UUID(as_uuid=True), ForeignKey('prices.id'),
                primary_key=True, default=uuid.uuid4)

    qav = Column(Float)
    num_trades = Column(Integer)
    taker_base_vol = Column(Float)
    taker_quote_vol = Column(Float)
    ignore = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'prices_crypto',
        'inherit_condition': (id == Price.id),
    }
