"""
Selection Model.

Defines the database schema, JSON structure, and helper methods for the Selection entity.
"""

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, DateTime, Numeric, String

from utils import BaseModel

from . import JSON
from .market import MarketModel


class SelectionOutcome(Enum):
    """
    Enumeration for selection outcomes.

    Attributes:
        WIN: The selection resulted in a win.
        VOID: The selection was voided.
        LOSE: The selection resulted in a loss.
        PLACE: The selection resulted in a place.
        UNSETTLED: The selection has not been settled yet.
    """

    WIN = "WIN"
    VOID = "VOID"
    LOSE = "LOSE"
    PLACE = "PLACE"
    UNSETTLED = "UNSETTLED"


class SelectionJSON(JSON):
    """
    JSON structure for Selection objects.

    Attributes:
        id (str): Unique identifier of the selection.
        market_id (str): Unique identifier of the associated market.
        name (str): Name of the selection.
        display_name (str): Display name of the selection.
        slug (str): Slugified version of the selection name.
        price (float): Price of the selection.
        outcome (SelectionOutcome): Outcome of the selection.
        is_active (bool): Whether the selection is active.
        created_at (str): Timestamp of when the selection was created.
        updated_at (str): Timestamp of when the selection was last updated.
    """

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


class SelectionModel(BaseModel):
    """
    SQLAlchemy model for the Selection table.

    Attributes:
        id (UUID): Primary key of the selection.
        market_id (UUID): Foreign key referencing the Market table.
        name (str): Name of the selection.
        display_name (str): Display name of the selection.
        slug (str): Slugified version of the selection name.
        price (float): Price of the selection.
        outcome (SelectionOutcome): Outcome of the selection.
        is_active (bool): Whether the selection is active.
        created_at (datetime): Timestamp of when the selection was created.
        updated_at (datetime): Timestamp of when the selection was last updated.
    """

    __tablename__ = "selection"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # FK
    market_id = Column(
        UUID(as_uuid=True), ForeignKey(MarketModel.id, name="selection_market_id", ondelete="CASCADE"), nullable=False
    )
    market = relationship("MarketModel", lazy="subquery", back_populates="selections")
    # Columns
    name = Column(String(100), nullable=False)
    display_name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    price = Column(Numeric(10, 2))
    outcome = Column(ENUM(SelectionOutcome))
    is_active = Column(Boolean, default=False)
    # Default columns
    # pylint: disable=not-callable
    created_at = Column(DateTime(timezone=datetime.now(timezone.utc)), default=func.now(), nullable=False)
    # pylint: disable=not-callable
    updated_at = Column(
        DateTime(timezone=datetime.now(timezone.utc)), default=func.now(), onupdate=func.now(), nullable=False
    )

    @classmethod
    def obj_to_json(cls, obj) -> SelectionJSON:
        """
        Converts a SQLAlchemy selection object to JSON format.

        Args:
            obj (SelectionModel): The selection object to convert.

        Returns:
            SelectionJSON: The JSON representation of the selection.
        """
        return {
            "id": str(obj.id),
            "market_id": str(obj.market_id),
            "name": obj.name,
            "display_name": obj.display_name,
            "slug": obj.slug,
            "price": obj.price,
            "outcome": obj.outcome,
            "is_active": obj.is_active,
            "created_at": obj.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at": obj.updated_at.strftime("%Y-%m-%d %H:%M"),
        }

    def to_json(self) -> SelectionJSON:
        """
        Converts the current selection instance to JSON format.

        Returns:
            SelectionJSON: The JSON representation of the selection.
        """
        return {
            "id": str(self.id),
            "market_id": str(self.market_id),
            "name": self.name,
            "display_name": self.display_name,
            "slug": self.slug,
            "price": self.price,
            "outcome": self.outcome,
            "is_active": self.is_active,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M"),
        }

    def __str__(self) -> str:
        """
        Returns a string representation of the selection instance.

        Returns:
            str: The string representation of the selection.
        """
        return f"{str(self.id)} - {self.name}"
