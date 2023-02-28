from models import Base
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid


class Price(Base):

    __tablename__ = "prices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    unix_time = Column(Integer)
    date_time_utc = Column(DateTime(timezone=True))
    date_time_gmt_5 = Column(DateTime(timezone=True))
    open_price = Column(Float)
    close_price = Column(Float)
    low_price = Column(Float)
    high_price = Column(Float)
    volume = Column(Integer)

    # asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"))
    # asset = relationship("Price", back_populates='assets')
