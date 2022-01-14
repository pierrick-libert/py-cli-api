'''Sport class for business logic'''
from uuid import UUID
from typing import Dict, List, Union

from utils.db import DB
from utils.helper import Helper
from utils.interfaces import ModuleInterface

from models.sport import SportModel, SportJSON


class Sport(ModuleInterface):
    '''Sport class'''

    def upsert(self, uuid: UUID, data: Dict[str, Union[str, int, float, bool]]) -> UUID:
        '''Upsert a sport'''
        model = DB.get_instance().get_upsert_data(SportModel(id=uuid), data)
        if data.get('name', None) is not None:
            model.slug = Helper.slugify(model.name)

        # Upsert data in DB
        with DB.get_instance().get_session() as session:
            session.merge(model)
        return uuid

    def delete(self, uuid: UUID) -> None:
        '''Delete a sport'''
        DB.get_instance().delete(SportModel, uuid)

    def search(self, data: List[Dict[str, Union[str, int, float, bool]]]) -> List[SportJSON]:
        '''Search a sport'''
        results = []
        model_keys = SportModel.__table__.columns.keys()
        with DB.get_instance().get_session() as session:
            query = 'SELECT DISTINCT s.* FROM sport s'
            # Build the where query
            where_query = DB.get_instance().build_where('s', model_keys, data)
            # Apply the where
            if where_query != '':
                query += f' WHERE {where_query}'
            results = session.execute(query).all()

        return [SportModel.obj_to_json(res) for res in results]
