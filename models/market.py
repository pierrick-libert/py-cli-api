"""
Market Model.

Defines the database schema, JSON structure, and helper methods for the Market entity.
"""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, DateTime, SmallInteger, String

from utils import BaseModel

from . import JSON
from .event import EventModel


class MarketJSON(JSON):
    """
    JSON structure for Market objects.

    Attributes:
        id (str): Unique identifier of the market.
        event_id (str): Unique identifier of the associated event.
        name (str): Name of the market.
        display_name (str): Display name of the market.
        slug (str): Slugified version of the market name.
        order (int): Display order of the market.
        schema (int): Schema version for the market.
        columns (int): Number of columns for the market.
        is_active (bool): Whether the market is active.
        created_at (str): Timestamp of when the market was created.
        updated_at (str): Timestamp of when the market was last updated.
    """

    id: str
    event_id: str
    name: str
    display_name: str
    slug: str
    order: int
    schema: int
    columns: int
    is_active: bool
    created_at: str
    updated_at: str


class MarketModel(BaseModel):
    """
    SQLAlchemy model for the Market table.

    Attributes:
        id (UUID): Primary key of the market.
        event_id (UUID): Foreign key referencing the Event table.
        name (str): Name of the market.
        display_name (str): Display name of the market.
        slug (str): Slugified version of the market name.
        order (int): Display order of the market.
        schema (int): Schema version for the market.
        columns (int): Number of columns for the market.
        is_active (bool): Whether the market is active.
        created_at (datetime): Timestamp of when the market was created.
        updated_at (datetime): Timestamp of when the market was last updated.
    """

    __tablename__ = "market"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # FK
    event_id = Column(
        UUID(as_uuid=True), ForeignKey(EventModel.id, name="market_event_id", ondelete="CASCADE"), nullable=False
    )
    event = relationship("EventModel", lazy="subquery", back_populates="markets")
    selections = relationship("SelectionModel", lazy="joined", back_populates="market")
    # Columns
    name = Column(String(100), nullable=False)
    display_name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    order = Column(SmallInteger, nullable=False)
    schema = Column(SmallInteger, nullable=False)
    columns = Column(SmallInteger, nullable=False)
    is_active = Column(Boolean, default=False)
    # Default columns
    # pylint: disable=not-callable
    created_at = Column(DateTime(timezone=datetime.now(timezone.utc)), default=func.now(), nullable=False)
    # pylint: disable=not-callable
    updated_at = Column(
        DateTime(timezone=datetime.now(timezone.utc)), default=func.now(), onupdate=func.now(), nullable=False
    )

    @classmethod
    def obj_to_json(cls, obj) -> MarketJSON:
        """
        Converts a SQLAlchemy market object to JSON format.

        Args:
            obj (MarketModel): The market object to convert.

        Returns:
            MarketJSON: The JSON representation of the market.
        """
        return {
            "id": str(obj.id),
            "event_id": str(obj.event_id),
            "name": obj.name,
            "display_name": obj.display_name,
            "slug": obj.slug,
            "order": obj.order,
            "schema": obj.schema,
            "columns": obj.columns,
            "is_active": obj.is_active,
            "created_at": obj.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at": obj.updated_at.strftime("%Y-%m-%d %H:%M"),
        }

    def to_json(self) -> MarketJSON:
        """
        Converts the current market instance to JSON format.

        Returns:
            MarketJSON: The JSON representation of the market.
        """
        return {
            "id": str(self.id),
            "event_id": str(self.event_id),
            "name": self.name,
            "display_name": self.display_name,
            "slug": self.slug,
            "order": self.order,
            "schema": self.schema,
            "columns": self.columns,
            "is_active": self.is_active,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M"),
        }

    def __str__(self) -> str:
        """
        Returns a string representation of the market instance.

        Returns:
            str: The string representation of the market.
        """
        return f"{str(self.id)} - {self.name}"
