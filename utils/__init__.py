"""
Initialize the base model for database operations.

This module provides a shared SQLAlchemy declarative base for all models in the project.
"""

from sqlalchemy.orm import DeclarativeMeta

from utils.db import DB

# Define the base model for all database models
BaseModel: DeclarativeMeta = DB.get_instance().get_base()
