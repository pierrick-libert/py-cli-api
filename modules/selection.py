'''Selection class for business logic'''
from uuid import UUID
from typing import Dict, Union

from utils.db import DB
from utils.helper import Helper
from utils.interfaces import ModuleInterface

from models.selection import SelectionModel


class Selection(ModuleInterface):
    '''Selection class'''

    def upsert(self, uuid: UUID, data: Dict[str, Union[str, int, float, bool]]) -> None:
        '''Upsert a Selection'''
        model = DB.get_instance().get_upsert_data(SelectionModel(id=uuid), data)
        if data.get('name', None):
            model.slug = Helper.slugify(model.name)
        if data.get('outcome', None):
            model.outcome = model.outcome.upper()

        # Upsert data in DB
        with DB.get_instance().get_session() as session:
            session.merge(model)
        return uuid

    def delete(self, uuid: UUID) -> None:
        '''Delete a Selection'''
        DB.get_instance().delete(SelectionModel, uuid)

    def search(self, data: Dict[str, Union[str, int, float, bool]]) -> None:
        '''Search a Selection'''
        results = []
        model_keys = SelectionModel.__table__.columns.keys()
        with DB.get_instance().get_session() as session:
            query = 'SELECT DISTINCT s.* FROM selection s'
            # Build the where query
            where_query = DB.get_instance().build_where('s', model_keys, data)
            # Apply the where
            if where_query != '':
                query += f' WHERE {where_query}'
            results = session.execute(query).all()

        return [SelectionModel.obj_to_json(res) for res in results]
