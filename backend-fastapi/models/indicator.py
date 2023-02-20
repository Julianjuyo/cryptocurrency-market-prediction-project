from models import Base

from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Float
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
    unix_time = Column(Integer)

    price_id = Column(UUID(as_uuid=True), ForeignKey("prices.id"))
    price = relationship("prices")
