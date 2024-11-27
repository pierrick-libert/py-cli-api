"""
Sport Model.

Defines the database schema, JSON structure, and helper methods for the Sport entity.
"""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Column, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, DateTime, SmallInteger, String

from utils import BaseModel

from . import JSON


class SportJSON(JSON):
    """
    JSON structure for Sport objects.

    Attributes:
        id (str): Unique identifier of the sport.
        name (str): Name of the sport.
        display_name (str): Display name of the sport.
        slug (str): Slugified version of the sport name.
        order (int): Display order of the sport.
        is_active (bool): Whether the sport is active.
        created_at (str): Timestamp of when the sport was created.
        updated_at (str): Timestamp of when the sport was last updated.
    """

    id: str
    name: str
    display_name: str
    slug: str
    order: int
    is_active: bool
    created_at: str
    updated_at: str


class SportModel(BaseModel):
    """
    SQLAlchemy model for the Sport table.

    Attributes:
        id (UUID): Primary key of the sport.
        name (str): Name of the sport.
        display_name (str): Display name of the sport.
        slug (str): Slugified version of the sport name.
        order (int): Display order of the sport.
        is_active (bool): Whether the sport is active.
        created_at (datetime): Timestamp of when the sport was created.
        updated_at (datetime): Timestamp of when the sport was last updated.
    """

    __tablename__ = "sport"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # FK
    events = relationship("EventModel", lazy="joined", back_populates="sport")
    # Columns
    name = Column(String(100), nullable=False)
    display_name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    order = Column(SmallInteger, nullable=False)
    is_active = Column(Boolean, default=False)
    # Default columns
    # pylint: disable=not-callable
    created_at = Column(DateTime(timezone=datetime.now(timezone.utc)), default=func.now(), nullable=False)
    # pylint: disable=not-callable
    updated_at = Column(
        DateTime(timezone=datetime.now(timezone.utc)), default=func.now(), onupdate=func.now(), nullable=False
    )

    @classmethod
    def obj_to_json(cls, obj) -> SportJSON:
        """
        Converts a SQLAlchemy sport object to JSON format.

        Args:
            obj (SportModel): The sport object to convert.

        Returns:
            SportJSON: The JSON representation of the sport.
        """
        return {
            "id": str(obj.id),
            "name": obj.name,
            "display_name": obj.display_name,
            "slug": obj.slug,
            "order": obj.order,
            "is_active": obj.is_active,
            "created_at": obj.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at": obj.updated_at.strftime("%Y-%m-%d %H:%M"),
        }

    def to_json(self) -> SportJSON:
        """
        Converts the current sport instance to JSON format.

        Returns:
            SportJSON: The JSON representation of the sport.
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "display_name": self.display_name,
            "slug": self.slug,
            "order": self.order,
            "is_active": self.is_active,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M"),
        }

    def __str__(self):
        """
        Returns a string representation of the sport instance.

        Returns:
            str: The string representation of the sport.
        """
        return f"{str(self.id)} - {self.name}"
