'''Market class for business logic'''
from uuid import UUID
from typing import Dict, List, Union

from utils.db import DB
from utils.helper import Helper
from utils.interfaces import ModuleInterface

from models.market import MarketModel, MarketJSON


class Market(ModuleInterface):
    '''Market class'''

    def upsert(self, uuid: UUID, data: Dict[str, Union[str, int, float, bool]]) -> UUID:
        '''Upsert a Market'''
        model = DB.get_instance().get_upsert_data(MarketModel(id=uuid), data)
        if data.get('name', None):
            model.slug = Helper.slugify(model.name)

        # Upsert data in DB
        with DB.get_instance().get_session() as session:
            session.merge(model)
        return uuid

    def delete(self, uuid: UUID) -> None:
        '''Delete a Market'''
        DB.get_instance().delete(MarketModel, uuid)

    def search(self, data: Dict[str, Union[str, int, float, bool]]) -> List[MarketJSON]:
        '''Search a Market'''
        results = []
        model_keys = MarketModel.__table__.columns.keys()
        with DB.get_instance().get_session() as session:
            query = 'SELECT DISTINCT m.* FROM market m'
            # Build the where query
            where_query = DB.get_instance().build_where('m', model_keys, data)
            # Apply the where
            if where_query != '':
                query += f' WHERE {where_query}'
            results = session.execute(query).all()

        return [MarketModel.obj_to_json(res) for res in results]
