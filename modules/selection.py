"""
Defines the Selection class for business logic.

This class implements the required methods for managing selections, such as upserting,
deleting, and searching, using the database interface.
"""

from collections.abc import Sequence
from uuid import UUID

from models.selection import SelectionJSON, SelectionModel
from utils.db import DB
from utils.helper import Helper
from utils.interfaces import ModuleInterface


class Selection(ModuleInterface):
    """
    A class for handling business logic related to selections.

    This class provides methods to upsert, delete, and search for selections in the database.
    """

    def upsert(self, uuid: UUID, data: dict[str, str | int | float | bool]) -> UUID:
        """
        Upserts (inserts or updates) a selection in the database.

        Args:
            uuid (UUID): The unique identifier of the selection.
            data (dict[str, str | int | float | bool]): The data to be upserted.

        Returns:
            UUID: The unique identifier of the upserted selection.
        """
        model = DB.get_instance().get_upsert_data(SelectionModel(id=uuid), data)
        if data.get("name", None):
            model.slug = Helper.slugify(model.name)
        if data.get("outcome", None):
            model.outcome = model.outcome.upper()

        # Upsert data in DB
        with DB.get_instance().get_session() as session:
            session.merge(model)
        return uuid

    def delete(self, uuid: UUID) -> None:
        """
        Deletes a selection from the database.

        Args:
            uuid (UUID): The unique identifier of the selection to delete.
        """
        DB.get_instance().delete(SelectionModel, uuid)

    def search(self, data: list[dict[str, str | int | float | bool]]) -> Sequence[SelectionJSON]:
        """
        Searches for selections in the database based on criteria.

        Args:
            data (list[dict[str, str | int | float | bool]]): A list of search criteria.

        Returns:
            Sequence[SelectionJSON]: A sequence of selection objects in JSON format.
        """
        results = []
        model_keys = SelectionModel.__table__.columns.keys()
        with DB.get_instance().get_session() as session:
            query = "SELECT DISTINCT s.* FROM selection s"
            # Build the where query
            where_query = DB.get_instance().build_where("s", model_keys, data)
            # Apply the where
            if where_query != "":
                query += f" WHERE {where_query}"
            results = session.execute(query).all()

        return [SelectionModel.obj_to_json(res) for res in results]
