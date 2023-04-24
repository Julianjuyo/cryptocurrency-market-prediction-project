from models import Base
from sqlalchemy import Column, String, ForeignKey, DateTime, Float, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Indicator(Base):

    __tablename__ = "indicators"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # name = Column(String)
    # value = Column(Float)
    gold_price = Column(Float)
    silver_price = Column(Float)
    natural_gas_price = Column(Float)
    cotton_price = Column(Float)
    coffee_price = Column(Float)
    sugar_price = Column(Float)
    cocoa_price = Column(Float)
    rice_price = Column(Float)
    corn_price = Column(Float)
    wheat_price = Column(Float)
    soybean_price = Column(Float)
    oats_price = Column(Float)
    spy500_price = Column(Float)
    dow_jones_price = Column(Float)
    nasdaq_price = Column(Float)
    russell_2000_price = Column(Float)
    us_10_year_treasury_price = Column(Float)
    us_5_year_treasury_price = Column(Float)
    us_2_year_treasury_price = Column(Float)
    usbond_price = Column(Float)

    unix_time = Column(BigInteger)
    date_time_utc = Column(DateTime(timezone=True))
    date_time_gmt_5 = Column(DateTime(timezone=True))

    price_id = Column(UUID(as_uuid=True), ForeignKey("prices.id"))
    price_origin = relationship("Price", back_populates='indicators')