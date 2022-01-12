'''Sport Model'''
from uuid import uuid4
from datetime import datetime

from sqlalchemy import Column, func
from sqlalchemy.types import String, SmallInteger, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID


class SportModel(declarative_base()):
    '''Sport table'''
    __tablename__ = 'sport'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # Columns
    name = Column(String(100), nullable=False)
    display_name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
    order = Column(SmallInteger, nullable=False)
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

    def to_json(self):
        '''To json method'''
        return {
            'id': str(self.id),
            'name': self.name,
            'display_name': self.display_name,
            'slug': self.slug,
            'order': self.order,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }