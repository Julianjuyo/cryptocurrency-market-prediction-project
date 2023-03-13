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
    name = Column(String)
    value = Column(Float)
    unix_time = Column(BigInteger)
    date_time_utc = Column(DateTime(timezone=True))
    date_time_gmt_5 = Column(DateTime(timezone=True))

    price_id = Column(UUID(as_uuid=True), ForeignKey("prices.id"))
    price_origin = relationship("Price", back_populates='indicators')
