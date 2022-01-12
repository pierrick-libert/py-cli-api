'''Selection Model'''
from uuid import uuid4
from enum import Enum
from datetime import datetime

from sqlalchemy import Column, func, ForeignKey
from sqlalchemy.types import String, DateTime, Numeric, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ENUM, UUID

from .market import MarketModel


class SelectionOutcome(Enum):
    '''Enum for selection outcome'''
    win = 'win'
    void = 'void'
    lose = 'lose'
    place = 'place'
    unsettled = 'unsettled'


class SelectionModel(declarative_base()):
    '''Selection table'''
    __tablename__ = 'selection'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # FK
    market_id = Column(
        UUID(as_uuid=True),
        ForeignKey(MarketModel.id, ondelete='CASCADE'),
        nullable=False
    )
    # Columns
    name = Column(String(100), nullable=False)
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
