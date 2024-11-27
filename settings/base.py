"""
Settings for the project.

This module defines configuration variables for the database and environment settings.
"""

import os

DATABASE = {
    "NAME": os.environ.get("POSTGRESQL_ADDON_DB", "888_assignment"),
    "USER": os.environ.get("POSTGRESQL_ADDON_USER", "postgres"),
    "PASSWORD": os.environ.get("POSTGRESQL_ADDON_PASSWORD", "toto42"),
    "HOST": os.environ.get("POSTGRESQL_ADDON_HOST", "localhost"),
    "PORT": os.environ.get("POSTGRESQL_ADDON_PORT", 5432),
    "URI": os.environ.get("POSTGRESQL_ADDON_URI", ""),
}

ENV = os.environ.get("ENV", "local")
