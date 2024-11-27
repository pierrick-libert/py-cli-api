"""
Defines the Sport class for business logic.

This class implements the required methods for managing sports, such as upserting,
deleting, and searching, using the database interface.
"""

from collections.abc import Sequence
from uuid import UUID

from models.sport import SportJSON, SportModel
from utils.db import DB
from utils.helper import Helper
from utils.interfaces import ModuleInterface


class Sport(ModuleInterface):
    """
    A class for handling business logic related to sports.

    This class provides methods to upsert, delete, and search for sports in the database.
    """

    def upsert(self, uuid: UUID, data: dict[str, str | int | float | bool]) -> UUID:
        """
        Upserts (inserts or updates) a sport in the database.

        Args:
            uuid (UUID): The unique identifier of the sport.
            data (dict[str, str | int | float | bool]): The data to be upserted.

        Returns:
            UUID: The unique identifier of the upserted sport.
        """
        model = DB.get_instance().get_upsert_data(SportModel(id=uuid), data)
        if data.get("name", None) is not None:
            model.slug = Helper.slugify(model.name)

        # Upsert data in DB
        with DB.get_instance().get_session() as session:
            session.merge(model)
        return uuid

    def delete(self, uuid: UUID) -> None:
        """
        Deletes a sport from the database.

        Args:
            uuid (UUID): The unique identifier of the sport to delete.
        """
        DB.get_instance().delete(SportModel, uuid)

    def search(self, data: list[dict[str, str | int | float | bool]]) -> Sequence[SportJSON]:
        """
        Searches for sports in the database based on criteria.

        Args:
            data (list[dict[str, str | int | float | bool]]): A list of search criteria.

        Returns:
            Sequence[SportJSON]: A sequence of sport objects in JSON format.
        """
        results = []
        model_keys = SportModel.__table__.columns.keys()
        with DB.get_instance().get_session() as session:
            query = "SELECT DISTINCT s.* FROM sport s"
            # Build the where query
            where_query = DB.get_instance().build_where("s", model_keys, data)
            # Apply the where
            if where_query != "":
                query += f" WHERE {where_query}"
            results = session.execute(query).all()

        return [SportModel.obj_to_json(res) for res in results]
