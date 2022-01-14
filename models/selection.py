'''Selection Model'''
from uuid import uuid4
from enum import Enum
from datetime import datetime
from typing import TypedDict

from sqlalchemy import Column, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import String, DateTime, Numeric, Boolean
from sqlalchemy.dialects.postgresql import ENUM, UUID

from utils.db import DB

from .market import MarketModel


class SelectionOutcome(Enum):
    '''Enum for selection outcome'''
    WIN = 'WIN'
    VOID = 'VOID'
    LOSE = 'LOSE'
    PLACE = 'PLACE'
    UNSETTLED = 'UNSETTLED'


class SelectionJSON(TypedDict):
    '''JSON for selection'''
    id: str
    market_id: str
    name: str
    display_name: str
    slug: str
    price: float
    outcome: SelectionOutcome
    is_active: bool
    created_at: str
    updated_at: str


class SelectionModel(DB.get_instance().get_base()):
    '''Selection table'''
    __tablename__ = 'selection'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # FK
    market_id = Column(
        UUID(as_uuid=True),
        ForeignKey(MarketModel.id, name='selection_market_id', ondelete='CASCADE'),
        nullable=False
    )
    market = relationship('MarketModel', lazy='subquery', back_populates='selections')
    # Columns
    name = Column(String(100), nullable=False)
    display_name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    price = Column(Numeric(10, 2))
    outcome = Column(ENUM(SelectionOutcome))
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
    def obj_to_json(cls, obj) -> SelectionJSON:
        '''Obj to json'''
        return {
            'id': str(obj.id),
            'market_id': str(obj.market_id),
            'name': obj.name,
            'display_name': obj.display_name,
            'slug': obj.slug,
            'price': obj.price,
            'outcome': obj.outcome,
            'is_active': obj.is_active,
            'created_at': obj.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': obj.updated_at.strftime('%Y-%m-%d %H:%M')
        }

    def to_json(self) -> SelectionJSON:
        '''To json method'''
        return {
            'id': str(self.id),
            'market_id': str(self.market_id),
            'name': self.name,
            'display_name': self.display_name,
            'slug': self.slug,
            'price': self.price,
            'outcome': self.outcome,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M')
        }

    def __str__(self) -> str:
        '''Return string'''
        return f'{str(self.id)} - {self.name}'
