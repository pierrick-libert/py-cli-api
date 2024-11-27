"""
Type checking utility.

Provides methods to validate UUIDs, JSON strings, and specific argument types.
"""

import json
from argparse import ArgumentTypeError
from uuid import UUID


class TypeParser:
    """
    A utility class for parsing and validating various types of input data.
    """

    @classmethod
    def check_uuid(cls, uuid_str: str) -> UUID:
        """
        Validates whether a string is a valid UUID.

        Args:
            uuid_str (str): The input string to validate as a UUID.

        Returns:
            uuid.UUID: A valid UUID object.

        Raises:
            ArgumentTypeError: If the input string is not a valid UUID.
        """
        try:
            return UUID(f"{uuid_str.strip()}")
        except (TypeError, ValueError) as error:
            raise ArgumentTypeError("Invalid uuid") from error

    @classmethod
    def check_json(cls, json_str: str) -> dict | list:
        """
        Validates whether a string is a valid JSON format.

        Args:
            json_str (str): The input string to validate as JSON.

        Returns:
            Any: The parsed JSON object (dict, list, etc.).

        Raises:
            ArgumentTypeError: If the input string is not a valid JSON format.
        """
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as error:
            raise ArgumentTypeError("Invalid JSON data") from error

    @classmethod
    def check_type(cls, arg_type: str) -> str:
        """
        Validates whether the input type is within the allowed scope.

        Args:
            arg_type (str): The input type to validate.

        Returns:
            str: The validated type if it is allowed.

        Raises:
            ArgumentTypeError: If the type is not in the allowed scope.
        """
        if arg_type not in ["sport", "event", "selection", "market"]:
            raise ArgumentTypeError("Invalid type")
        return arg_type
