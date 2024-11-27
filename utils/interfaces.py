"""
Defines an interface to enforce the implementation of required methods for modules.

This ensures that any module using this interface implements methods for upserting,
deleting, and searching objects in the database.
"""

from abc import ABCMeta, abstractmethod
from collections.abc import Sequence
from uuid import UUID

from models import JSON


class ModuleInterface(metaclass=ABCMeta):
    """
    An abstract base class that defines the required methods for database operations.

    Classes implementing this interface must provide concrete implementations for
    upserting, deleting, and searching objects.
    """

    @abstractmethod
    def upsert(self, uuid: UUID, data: dict[str, str | int | float | bool]) -> UUID:
        """
        Inserts or updates an object in the database.

        Args:
            uuid (UUID): The unique identifier of the object to upsert.
            data (dict[str, Union[str, int, float, bool]]): The data to insert or update.

        Returns:
            UUID: The unique identifier of the upserted object.
        """

    @abstractmethod
    def delete(self, uuid: UUID) -> None:
        """
        Removes an object from the database.

        Args:
            uuid (UUID): The unique identifier of the object to delete.
        """

    @abstractmethod
    def search(self, data: list[dict[str, str | int | float | bool]]) -> Sequence[JSON]:
        """
        Retrieves object(s) from the database based on search criteria.

        Args:
            data (list[dict[str, Union[str, int, float, bool]]]): A list of search criteria.

        Returns:
            Sequence[JSON]: A sequence of JSON objects matching the search criteria.
        """
