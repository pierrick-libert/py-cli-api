"""
Initialization module for JSON typing.

This module defines the base `JSON` type used throughout the project for consistent typing.
"""

from typing import TypedDict


class JSON(TypedDict):
    """
    A base class representing a JSON object with proper typing.

    This class is intended to be extended by more specific JSON structures
    used in the application.
    """
