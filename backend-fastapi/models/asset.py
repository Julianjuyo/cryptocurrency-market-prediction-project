from models import Base

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Asset(Base):

    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    symbol = Column(String)
    base_asset = Column(String)
    quote_asset = Column(String)
    interval = Column(String)
    asset_type = Column(String)
    exchange_id = Column(String, ForeignKey("exchanges.id"))

    exchange = relationship("exchanges")
