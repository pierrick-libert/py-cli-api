"""
A collection of helper classes and functions for the project.

This module provides utilities to perform common tasks like string manipulation.
"""

import re


# pylint: disable=too-few-public-methods
class Helper:
    """
    A helper class providing utility methods for string manipulation and other common tasks.
    """

    @classmethod
    def slugify(cls, text: str) -> str | None:
        """
        Converts a string into a slug format suitable for URLs or file names.

        The function:
        - Converts the input text to lowercase.
        - Replaces non-alphanumeric characters and underscores with hyphens.
        - Strips leading or trailing hyphens.

        Args:
            text (str): The input string to slugify.

        Returns:
            str | None: A slugified version of the input string, or None if the input is not a string.
        """
        if isinstance(text, str) is False:
            return None
        return re.sub(r"[\W_]+", "-", text.strip().lower()).strip("-")
