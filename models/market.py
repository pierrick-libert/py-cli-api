'''Market Model'''
from uuid import uuid4
from datetime import datetime

from sqlalchemy import Column, func, ForeignKey
from sqlalchemy.types import String, SmallInteger, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

from .event import EventModel


class MarketModel(declarative_base()):
    '''Market table'''
    __tablename__ = 'market'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # FK
    event_id = Column(
        UUID(as_uuid=True),
        ForeignKey(EventModel.id, ondelete='CASCADE'),
        nullable=False
    )
    # Columns
    name = Column(String(100), nullable=False)
    display_name = Column(String(100), nullable=False)
    order = Column(SmallInteger, nullable=False)
    schema = Column(SmallInteger, nullable=False)
    columns = Column(SmallInteger, nullable=False)
    is_active = Column(Boolean, default=False)
    # Default columns
    created_at = Column(
        DateTime(timezone=datetime.utcnow),
        default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=datetime.utcnow),
        default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
