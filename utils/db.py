'''DB connection'''
import sys
import enum

from typing import List, Union

from contextlib import contextmanager

from sqlalchemy import Table, create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, DeclarativeMeta
from sqlalchemy.engine import Engine
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy_utils import database_exists, create_database

from settings.base import DATABASE

from .decorators import Singleton


@Singleton
class DB:
    '''DB for connections purpose'''
    __engine = None

    def __init__(self,
        uri: str = DATABASE['URI'],
        verbose: bool = False,
    ):
        '''Create the connection to the DB'''
        try:
            self.__engine = create_engine(uri, echo = verbose)
            if not database_exists(self.__engine.url):
                create_database(self.__engine.url)
        except SQLAlchemyError as error:
            print(f'An error occurred while connecting to the DB; {error}')
            sys.exit(1)

    # pylint: disable=no-method-argument
    def get_instance():
        '''To avoid decorator error with pylint'''

    @contextmanager
    # pylint: disable=unused-argument
    def get_session(self, *args, **kwargs) -> Session:
        '''Create a session for handling transactions'''
        session = Session(self.__engine)
        try:
            yield session
        except:
            session.rollback()
            raise
        else:
            session.commit()

    def get_engine(self) -> Engine:
        '''Return the engine object created in the constructor'''
        return self.__engine

    def create_table_from_model(self, model: DeclarativeMeta) -> Union[Table, bool]:
        '''Create the table based on parameters'''
        if inspect(self.__engine).has_table(model.__table__.name):
            return model.__table__, False

        with self.get_session() as session:
            # Create the table
            table_creation_sql = CreateTable(model.__table__)
            session.execute(table_creation_sql)
        return model.__table__, True

    def create_enum(self, obj: enum.Enum, name: str) -> None:
        '''Create an enum in DB'''
        ENUM(obj, name=name).create(bind=self.__engine)

    def get_upsert_data(self, model: DeclarativeMeta, data_keys: List[str]) -> DeclarativeMeta:
        '''Only fill data we received'''
        # Isolate the column name
        model_keys = model.__dict__.keys()
        # Fill the model
        for key in model_keys:
            if key not in data_keys or key == 'id':
                continue
            setattr(model, key, data[key])
        return model

    def upsert(self, model: DeclarativeMeta) -> None:
        '''Upsert the data for a model'''
        with self.get_session() as session:
            session.merge(model)
