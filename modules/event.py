'''Event class for business logic'''
from uuid import UUID
from typing import Dict, List, Union

from utils.db import DB
from utils.helper import Helper
from utils.interfaces import ModuleInterface

from models.event import EventModel, EventJSON


class Event(ModuleInterface):
    '''Event class'''

    def upsert(self, uuid: UUID, data: Dict[str, Union[str, int, float, bool]]) -> None:
        '''Upsert a Event'''
        model = DB.get_instance().get_upsert_data(EventModel(id=uuid), data)
        if data.get('name', None):
            model.slug = Helper.slugify(model.name)
        if data.get('type', None):
            model.type = model.type.upper()
        if data.get('status', None):
            model.status = model.status.upper()

        # Upsert data in DB
        with DB.get_instance().get_session() as session:
            session.merge(model)
        return uuid

    def delete(self, uuid: UUID) -> None:
        '''Delete a Event'''
        DB.get_instance().delete(EventModel, uuid)

    def search(self, data: Dict[str, Union[str, int, float, bool]]) -> List[EventJSON]:
        '''Search a Event'''
        results = []
        model_keys = EventModel.__table__.columns.keys()
        with DB.get_instance().get_session() as session:
            query = 'SELECT DISTINCT e.* FROM event e'
            # Build the where query
            where_query = DB.get_instance().build_where('e', model_keys, data)
            # Apply the where
            if where_query != '':
                query += f' WHERE {where_query}'
            results = session.execute(query).all()

        return [EventModel.obj_to_json(res) for res in results]
