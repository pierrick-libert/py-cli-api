'''Event Model'''
from uuid import uuid4
from enum import Enum
from datetime import datetime

from sqlalchemy import Column, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import String, SmallInteger, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID, ENUM

from .sport import SportModel


class EventType(Enum):
    inplay = 'inplay'
    preplay = 'preplay'


class EventStatus(Enum):
    inplay = 'inplay'
    preplay = 'preplay'
    ended = 'ended'


class EventModel(declarative_base()):
    '''Event table'''
    __tablename__ = 'event'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # FK
    sport_id = Column(
        UUID(as_uuid=True),
        ForeignKey(SportModel.id, ondelete='CASCADE'),
        nullable=False
    )
    # Columns
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
    type = Column(ENUM(EventType))
    status = Column(ENUM(EventStatus))
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
