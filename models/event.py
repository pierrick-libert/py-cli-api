"""
Event Model.

Defines the database schema, enumerations, and helper methods for the Event entity.
"""

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, DateTime, String

from utils import BaseModel

from . import JSON
from .sport import SportModel


class EventType(Enum):
    """
    Enumeration for event types.

    Attributes:
        INPLAY: The event is currently in play.
        PREPLAY: The event is scheduled to start.
    """

    INPLAY = "INPLAY"
    PREPLAY = "PREPLAY"


class EventStatus(Enum):
    """
    Enumeration for event statuses.

    Attributes:
        INPLAY: The event is currently in play.
        PREPLAY: The event is scheduled to start.
        ENDED: The event has ended.
    """

    INPLAY = "INPLAY"
    PREPLAY = "PREPLAY"
    ENDED = "ENDED"


class EventJSON(JSON):
    """
    JSON structure for Event objects.

    Attributes:
        id (str): Unique identifier of the event.
        sport_id (str): Unique identifier of the associated sport.
        name (str): Name of the event.
        display_name (str): Display name of the event.
        slug (str): Slugified version of the event name.
        type (EventType): Type of the event.
        status (EventStatus): Status of the event.
        is_active (bool): Whether the event is active.
        created_at (str): Timestamp of when the event was created.
        updated_at (str): Timestamp of when the event was last updated.
    """

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


class EventModel(BaseModel):
    """
    SQLAlchemy model for the Event table.

    Attributes:
        id (UUID): Primary key of the event.
        sport_id (UUID): Foreign key referencing the Sport table.
        name (str): Name of the event.
        display_name (str): Display name of the event.
        slug (str): Slugified version of the event name.
        type (EventType): Type of the event.
        status (EventStatus): Status of the event.
        is_active (bool): Whether the event is active.
        created_at (datetime): Timestamp of when the event was created.
        updated_at (datetime): Timestamp of when the event was last updated.
    """

    __tablename__ = "event"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # FK
    sport_id = Column(
        UUID(as_uuid=True), ForeignKey(SportModel.id, name="event_sport_id", ondelete="CASCADE"), nullable=False
    )
    sport = relationship("SportModel", lazy="subquery", back_populates="events")
    markets = relationship("MarketModel", lazy="joined", back_populates="event")
    # Columns
    name = Column(String(100), nullable=False)
    display_name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    type = Column(ENUM(EventType))
    status = Column(ENUM(EventStatus))
    is_active = Column(Boolean, default=False)
    # Default columns
    # pylint: disable=not-callable
    created_at = Column(DateTime(timezone=datetime.now(timezone.utc)), default=func.now(), nullable=False)
    # pylint: disable=not-callable
    updated_at = Column(
        DateTime(timezone=datetime.now(timezone.utc)), default=func.now(), onupdate=func.now(), nullable=False
    )

    @classmethod
    def obj_to_json(cls, obj) -> EventJSON:
        """
        Converts a SQLAlchemy event object to JSON format.

        Args:
            obj (EventModel): The event object to convert.

        Returns:
            EventJSON: The JSON representation of the event.
        """
        return {
            "id": str(obj.id),
            "sport_id": str(obj.sport_id),
            "name": obj.name,
            "display_name": obj.display_name,
            "slug": obj.slug,
            "type": obj.type,
            "status": obj.status,
            "is_active": obj.is_active,
            "created_at": obj.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at": obj.updated_at.strftime("%Y-%m-%d %H:%M"),
        }

    def to_json(self) -> EventJSON:
        """
        Converts the current event instance to JSON format.

        Returns:
            EventJSON: The JSON representation of the event.
        """
        return {
            "id": str(self.id),
            "sport_id": str(self.sport_id),
            "name": self.name,
            "display_name": self.display_name,
            "slug": self.slug,
            "type": self.type,
            "status": self.status,
            "is_active": self.is_active,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M"),
        }

    def __str__(self) -> str:
        """
        Returns a string representation of the event instance.

        Returns:
            str: The string representation of the event.
        """
        return f"{str(self.id)} - {self.name}"
