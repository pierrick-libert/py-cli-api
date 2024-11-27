"""
Defines the Event class for business logic.

This class implements the required methods for managing events, such as upserting,
deleting, and searching, using the database interface.
"""

from collections.abc import Sequence
from uuid import UUID

from models.event import EventJSON, EventModel
from utils.db import DB
from utils.helper import Helper
from utils.interfaces import ModuleInterface


class Event(ModuleInterface):
    """
    A class for handling business logic related to events.

    This class provides methods to upsert, delete, and search for events in the database.
    """

    def upsert(self, uuid: UUID, data: dict[str, str | int | float | bool]) -> UUID:
        """
        Upserts (inserts or updates) an event in the database.

        Args:
            uuid (UUID): The unique identifier of the event.
            data (dict[str, str | int | float | bool]): The data to be upserted.

        Returns:
            UUID: The unique identifier of the upserted event.
        """
        model = DB.get_instance().get_upsert_data(EventModel(id=uuid), data)
        if data.get("name", None):
            model.slug = Helper.slugify(model.name)
        if data.get("type", None):
            model.type = model.type.upper()
        if data.get("status", None):
            model.status = model.status.upper()

        # Upsert data in DB
        with DB.get_instance().get_session() as session:
            session.merge(model)
        return uuid

    def delete(self, uuid: UUID) -> None:
        """
        Deletes an event from the database.

        Args:
            uuid (UUID): The unique identifier of the event to delete.
        """
        DB.get_instance().delete(EventModel, uuid)

    def search(self, data: list[dict[str, str | int | float | bool]]) -> Sequence[EventJSON]:
        """
        Searches for events in the database based on criteria.

        Args:
            data (list[dict[str, str | int | float | bool]]): A list of search criteria.

        Returns:
            Sequence[EventJSON]: A sequence of event objects in JSON format.
        """
        results = []
        model_keys = EventModel.__table__.columns.keys()
        with DB.get_instance().get_session() as session:
            query = "SELECT DISTINCT e.* FROM event e"
            # Build the where query
            where_query = DB.get_instance().build_where("e", model_keys, data)
            # Apply the where
            if where_query != "":
                query += f" WHERE {where_query}"
            results = session.execute(query).all()

        return [EventModel.obj_to_json(res) for res in results]
