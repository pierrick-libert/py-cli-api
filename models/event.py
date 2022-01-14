'''Event Model'''
from uuid import uuid4
from enum import Enum
from datetime import datetime
from typing import TypedDict

from sqlalchemy import Column, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID, ENUM

from utils.db import DB

from .sport import SportModel


class EventType(Enum):
    '''Event Type enum'''
    INPLAY = 'INPLAY'
    PREPLAY = 'PREPLAY'


class EventStatus(Enum):
    '''Event Status enum'''
    INPLAY = 'INPLAY'
    PREPLAY = 'PREPLAY'
    ENDED = 'ENDED'


class EventJSON(TypedDict):
    '''JSON for event'''
    id: str
    sport_id: str
    name: str
    display_name: str
    slug: str
    type: EventType
    status: EventStatus
    is_active: bool
    created_at: str
    updated_at: str


class EventModel(DB.get_instance().get_base()):
    '''Event table'''
    __tablename__ = 'event'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # FK
    sport_id = Column(
        UUID(as_uuid=True),
        ForeignKey(SportModel.id, name='event_sport_id', ondelete='CASCADE'),
        nullable=False
    )
    sport = relationship('SportModel', lazy='subquery', back_populates='events')
    markets = relationship('MarketModel', lazy='joined', back_populates='event')
    # Columns
    name = Column(String(100), nullable=False)
    display_name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
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

    @classmethod
    def obj_to_json(cls, obj) -> EventJSON:
        '''Obj to json'''
        return {
            'id': str(obj.id),
            'sport_id': str(obj.sport_id),
            'name': obj.name,
            'display_name': obj.display_name,
            'slug': obj.slug,
            'type': obj.type,
            'status': obj.status,
            'is_active': obj.is_active,
            'created_at': obj.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': obj.updated_at.strftime('%Y-%m-%d %H:%M')
        }

    def to_json(self) -> EventJSON:
        '''To json method'''
        return {
            'id': str(self.id),
            'sport_id': str(self.sport_id),
            'name': self.name,
            'display_name': self.display_name,
            'slug': self.slug,
            'type': self.type,
            'status': self.status,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M')
        }

    def __str__(self) -> str:
        '''Return string'''
        return f'{str(self.id)} - {self.name}'
