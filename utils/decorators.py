"""
Define decorators for managing singleton patterns.
"""

from typing import Any, Type, TypeVar

T = TypeVar("T")  # Generic type for the class being decorated


class Singleton:
    """
    A decorator to enforce the Singleton pattern for a class.

    Ensures that only one instance of the class exists and provides a way to access it.
    """

    def __init__(self, cls: Type[T]):
        """
        Initializes the Singleton decorator.

        Args:
            cls (Type[T]): The class to be decorated as a singleton.
        """
        self._cls: Type[T] = cls
        self._instance: T | None = None

    def get_instance(self) -> Any:
        """
        Returns the singleton instance of the decorated class.

        If the instance does not already exist, it will be created.

        Returns:
            T: The singleton instance of the decorated class.
        """
        if self._instance is None:
            self._instance = self._cls()
        return self._instance

    def __call__(self) -> Any:
        """
        Prevents direct instantiation of the singleton class.

        Raises:
            TypeError: Always raises an error to enforce the Singleton pattern.
        """
        raise TypeError("Singletons must be accessed through `Instance()`.")

    def __instancecheck__(self, inst: Any) -> bool:
        """
        Checks if the given instance is of the singleton's class.

        Args:
            inst (Any): The instance to check.

        Returns:
            bool: True if the instance is of the singleton's class, False otherwise.
        """
        return isinstance(inst, self._cls)
