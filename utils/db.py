'''DB connection'''
import sys
import enum

from uuid import UUID
from typing import Dict, List, Union

from contextlib import contextmanager

from sqlalchemy import Table, create_engine, inspect, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, DeclarativeMeta
from sqlalchemy.engine import Engine
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

from settings.base import DATABASE

from .decorators import Singleton


@Singleton
class DB:
    '''DB for connections purpose'''
    __engine = None
    __base = declarative_base()

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

    # pylint: disable=no-self-use
    def get_operators(self, operator: str) -> str:
        '''Get the list of basic allowed operators'''
        sql_operator = None
        if operator in ['=', '>', '<', '>=', '<=', 'like', 'ilike', 'in']:
            sql_operator = operator
        elif operator.startswith('not') is True:
            sql_operator = f'not {operator[3:]}'
        elif 'regex' in operator:
            sql_operator = '~'
            if 'not' in operator:
                sql_operator = '!~'
            if 'i' in operator:
                sql_operator += '*'

        return sql_operator

    def get_condition(self, operator: str, field: str, prefix: str, value) -> str:
        '''Return the condition we need to use in a where'''
        query = ''
        operator = self.get_operators(operator)
        if operator is None:
            return query

        # Apply some verifications
        if 'in' in operator:
            if isinstance(value, list) is True and len(value) > 0:
                query = f'{prefix}.{field} {operator} (' + '\'' + '\',\''.join(value) + '\')'
            else:
                query = f'{prefix}.{field} {operator} (' + '\'' + str(value) + '\')'
        elif 'like' in operator:
            query = f'{prefix}.{field} {operator} ' + '\'%' + str(value) + '%\''
        else:
            query = f'{prefix}.{field} {operator} ' + '\'' + str(value) + '\''
        return query

    # pylint: disable=no-self-use
    def build_where(
            self, prefix: str, model_keys: List[str],
            data: List[Dict[str, Union[str, int, float, bool]]]
        ) -> str:
        '''Build the where condition for search on models'''
        where_query = ''
        for obj in data:
            if obj.get('field', None) not in model_keys or obj.get('value', None) is None:
                continue
            where_condition = DB.get_instance().get_condition(
                obj.get('operator', None), obj.get('field'), prefix, obj.get('value'))
            if where_condition == '':
                continue
            if where_query != '':
                where_query += ' AND '
            where_query += where_condition
        return where_query

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

    def get_base(self) -> DeclarativeMeta:
        '''Return the base object for all models'''
        return self.__base

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

    # pylint: disable=no-self-use
    def get_upsert_data(
            self, model: DeclarativeMeta,
            data: Dict[str, Union[str, int, float, bool]]
        ) -> DeclarativeMeta:
        '''Only fill data we received'''
        # Isolate the column name
        data_keys = data.keys()
        model_keys = model.__table__.columns.keys()
        # Fill the model
        for key in model_keys:
            if key not in data_keys or key == 'id':
                continue
            setattr(model, key, data[key])
        return model

    def delete(self, model: DeclarativeMeta, uuid: UUID) -> None:
        '''Delete a resource'''
        with self.get_session() as session:
            session.execute(delete(model).where(
                model.id == uuid).execution_options(synchronize_session='fetch'))
