from models import Base
# from models.indicator import Indicator
from models.priceIndicator import PriceIndicator
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid


class Price(Base):

    __tablename__ = "prices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    unix_time = Column(BigInteger)
    date_time_utc = Column(DateTime(timezone=True))
    date_time_gmt_5 = Column(DateTime(timezone=True))
    open_price = Column(Float)
    close_price = Column(Float)
    low_price = Column(Float)
    high_price = Column(Float)
    volume = Column(Float)
    qav = Column(Float)
    num_trades = Column(BigInteger)
    taker_base_vol = Column(Float)
    taker_quote_vol = Column(Float)
    ignore = Column(Integer)

    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"))
    asset_origin = relationship("Asset", back_populates='prices')


    # indicators = relationship("Indicator",  back_populates="price_origin")

    indicators = relationship('Indicator', secondary='priceIndicator', back_populates='prices')


