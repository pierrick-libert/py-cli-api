"""
DB connection module.

Provides database connection utilities, session management, and helper functions
for building queries, creating tables, enums, and performing CRUD operations.
"""

import sys
from contextlib import contextmanager
from enum import Enum
from typing import Generator
from uuid import UUID

from sqlalchemy import Table, create_engine, delete, inspect
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta, Session
from sqlalchemy.schema import CreateTable
from sqlalchemy_utils import create_database, database_exists

from settings.base import DATABASE

from .decorators import Singleton


@Singleton
class DB:
    """Singleton class for managing database connections and operations."""

    __engine: Engine | None = None
    __base: DeclarativeMeta = declarative_base()

    def __init__(
        self,
        uri: str = str(DATABASE["URI"]),
        verbose: bool = False,
    ):
        """
        Initializes the database connection.

        Args:
            uri (str): Database URI for connection.
            verbose (bool): Flag for enabling verbose output for SQLAlchemy.

        Raises:
            SystemExit: If the database connection fails.
        """
        try:
            self.__engine = create_engine(uri, echo=verbose)
            if not database_exists(self.__engine.url):
                create_database(self.__engine.url)
        except SQLAlchemyError as error:
            print(f"An error occurred while connecting to the DB; {error}")
            sys.exit(1)

    @staticmethod
    def get_instance():
        """
        Returns the singleton instance of the DB class.

        Returns:
            DB: The singleton instance.
        """

    # pylint: disable=no-self-use
    def get_operators(self, operator: str) -> str | None:
        """
        Gets the SQL operator corresponding to the given string.

        Args:
            operator (str): The input operator.

        Returns:
            str | None: The SQL operator if valid, otherwise None.
        """
        sql_operator = None
        if operator in ["=", ">", "<", ">=", "<=", "like", "ilike", "in"]:
            sql_operator = operator
        elif operator.startswith("not") is True:
            sql_operator = f"not {operator[3:]}"
        elif "regex" in operator:
            sql_operator = "~"
            if "not" in operator:
                sql_operator = "!~"
            if "i" in operator:
                sql_operator += "*"

        return sql_operator

    def get_condition(self, operator: str, field: str, prefix: str, value: list | str | int | float | bool) -> str:
        """
        Constructs a SQL condition for a WHERE clause.

        Args:
            operator (str): The operator to use.
            field (str): The field name.
            prefix (str): The table prefix.
            value (list | str | int | float | bool): The value to compare.

        Returns:
            str: The SQL condition string.
        """
        query = ""
        operator_allowed = self.get_operators(operator)
        if operator_allowed is None:
            return query

        # Apply some verifications
        if "in" in operator:
            if isinstance(value, list) and len(value) > 0:
                query = f"{prefix}.{field} {operator} (" + "'" + "','".join(value) + "')"
            else:
                query = f"{prefix}.{field} {operator} (" + "'" + str(value) + "')"
        elif "like" in operator:
            query = f"{prefix}.{field} {operator} " + "'%" + str(value) + "%'"
        else:
            query = f"{prefix}.{field} {operator} " + "'" + str(value) + "'"
        return query

    # pylint: disable=no-self-use
    def build_where(self, prefix: str, model_keys: list[str], data: list[dict[str, str | int | float | bool]]) -> str:
        """
        Builds a WHERE clause for a SQL query.

        Args:
            prefix (str): The table prefix.
            model_keys (list[str]): The list of valid model keys.
            data (list[dict]): The data to filter by.

        Returns:
            str: The WHERE clause string.
        """
        where_query = ""
        for obj in data:
            if obj.get("field", None) not in model_keys or obj.get("value", None) is None:
                continue
            where_condition = DB.get_instance().get_condition(
                obj.get("operator", None), obj.get("field"), prefix, obj.get("value")
            )
            if where_condition == "":
                continue
            if where_query != "":
                where_query += " AND "
            where_query += where_condition
        return where_query

    @contextmanager
    # pylint: disable=unused-argument
    def get_session(self, *args, **kwargs) -> Generator[Session, None, None]:
        """
        Context manager for handling database sessions.

        Yields:
            Session: The SQLAlchemy session.
        """
        session = Session(self.__engine)
        try:
            yield session
        except:
            session.rollback()
            raise
        else:
            session.commit()

    def get_base(self) -> DeclarativeMeta:
        """
        Returns the declarative base object for SQLAlchemy models.

        Returns:
            DeclarativeMeta: The base class.
        """
        return self.__base

    def get_engine(self) -> Engine:
        """
        Returns the SQLAlchemy engine.

        Returns:
            Engine: The SQLAlchemy engine.
        """
        return self.__engine

    def create_table_from_model(self, model: DeclarativeMeta) -> Table | bool:
        """
        Creates a table for the given SQLAlchemy model.

        Args:
            model (DeclarativeMeta): The SQLAlchemy model.

        Returns:
            Table | bool: The table object and a flag indicating creation success.
        """
        if inspect(self.__engine).has_table(model.__table__.name):
            return model.__table__, False

        with self.get_session() as session:
            # Create the table
            table_creation_sql = CreateTable(model.__table__)
            session.execute(table_creation_sql)
        return model.__table__, True

    def create_enum(self, obj: Enum, name: str) -> None:
        """
        Creates an ENUM type in the database.

        Args:
            obj (enum.Enum): The enum class.
            name (str): The name of the ENUM in the database.
        """
        ENUM(obj, name=name).create(bind=self.__engine)

    # pylint: disable=no-self-use
    def get_upsert_data(self, model: DeclarativeMeta, data: dict[str, str | int | float | bool]) -> DeclarativeMeta:
        """
        Populates model fields with given data for upsert operations.

        Args:
            model (DeclarativeMeta): The SQLAlchemy model.
            data (dict): The data to populate.

        Returns:
            DeclarativeMeta: The updated model.
        """
        # Isolate the column name
        data_keys = data.keys()
        model_keys = model.__table__.columns.keys()
        # Fill the model
        for key in model_keys:
            if key not in data_keys or key == "id":
                continue
            setattr(model, key, data[key])
        return model

    def delete(self, model: DeclarativeMeta, uuid: UUID) -> None:
        """
        Deletes a resource by its UUID.

        Args:
            model (DeclarativeMeta): The SQLAlchemy model.
            uuid (UUID): The UUID of the resource to delete.
        """
        with self.get_session() as session:
            session.execute(delete(model).where(model.id == uuid).execution_options(synchronize_session="fetch"))
