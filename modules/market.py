"""
Defines the Market class for business logic.

This class implements the required methods for managing markets, such as upserting,
deleting, and searching, using the database interface.
"""

from collections.abc import Sequence
from uuid import UUID

from models.market import MarketJSON, MarketModel
from utils.db import DB
from utils.helper import Helper
from utils.interfaces import ModuleInterface


class Market(ModuleInterface):
    """
    A class for handling business logic related to markets.

    This class provides methods to upsert, delete, and search for markets in the database.
    """

    def upsert(self, uuid: UUID, data: dict[str, str | int | float | bool]) -> UUID:
        """
        Upserts (inserts or updates) a market in the database.

        Args:
            uuid (UUID): The unique identifier of the market.
            data (dict[str, str | int | float | bool]): The data to be upserted.

        Returns:
            UUID: The unique identifier of the upserted market.
        """
        model = DB.get_instance().get_upsert_data(MarketModel(id=uuid), data)
        if data.get("name", None):
            model.slug = Helper.slugify(model.name)

        # Upsert data in DB
        with DB.get_instance().get_session() as session:
            session.merge(model)
        return uuid

    def delete(self, uuid: UUID) -> None:
        """
        Deletes a market from the database.

        Args:
            uuid (UUID): The unique identifier of the market to delete.
        """
        DB.get_instance().delete(MarketModel, uuid)

    def search(self, data: list[dict[str, str | int | float | bool]]) -> Sequence[MarketJSON]:
        """
        Searches for markets in the database based on criteria.

        Args:
            data (list[dict[str, str | int | float | bool]]): A list of search criteria.

        Returns:
            Sequence[MarketJSON]: A sequence of market objects in JSON format.
        """
        results = []
        model_keys = MarketModel.__table__.columns.keys()
        with DB.get_instance().get_session() as session:
            query = "SELECT DISTINCT m.* FROM market m"
            # Build the where query
            where_query = DB.get_instance().build_where("m", model_keys, data)
            # Apply the where
            if where_query != "":
                query += f" WHERE {where_query}"
            results = session.execute(query).all()

        return [MarketModel.obj_to_json(res) for res in results]
