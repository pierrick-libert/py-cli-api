'''Sport Model'''
from uuid import uuid4
from datetime import datetime

from sqlalchemy import Column, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import String, SmallInteger, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID

from utils.db import DB


class SportModel(DB.get_instance().get_base()):
    '''Sport table'''
    __tablename__ = 'sport'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # FK
    events = relationship('EventModel', lazy='joined', back_populates='sport')
    # Columns
    name = Column(String(100), nullable=False)
    display_name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
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

    @classmethod
    def obj_to_json(cls, obj):
        '''Obj to json'''
        return {
            'id': str(obj.id),
            'name': obj.name,
            'display_name': obj.display_name,
            'slug': obj.slug,
            'order': obj.order,
            'is_active': obj.is_active,
            'created_at': obj.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': obj.updated_at.strftime('%Y-%m-%d %H:%M')
        }

    def to_json(self):
        '''To json method'''
        return {
            'id': str(self.id),
            'name': self.name,
            'display_name': self.display_name,
            'slug': self.slug,
            'order': self.order,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M')
        }

    def __str__(self):
        '''Return string'''
        return f'{str(self.id)} - {self.name}'
