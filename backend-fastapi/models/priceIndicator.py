from models import Base
# from models.indicator import Indicator
# from models.price import Prie

from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID


class PriceIndicator(Base):
        
    __tablename__ = "PriceIndicator"

    # price_id = Column(UUID(as_uuid=True), ForeignKey('prices.id'), primary_key=True)
    Column('price_id', ForeignKey('prices.id'),primary_key=True)

    Column('indicator_id', ForeignKey('indicators.id'), primary_key=True)


# priceIndicator = Table('priceIndicator', Base.metadata,
#     Column('price_id', UUID(as_uuid=True), ForeignKey('prices.id'), primary_key=True),
#     Column('indicator_id', UUID(as_uuid=True), ForeignKey('indicators.id'), primary_key=True)
# )

