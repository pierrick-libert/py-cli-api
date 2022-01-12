'''Sport class for business logic'''
from uuid import UUID
from typing import Dict, Union

from sqlalchemy.exc import SQLAlchemyError

from utils.db import DB
from utils.helper import Helper
from utils.interfaces import ModuleInterface

from models.sport import SportModel


class Sport(ModuleInterface):
    '''Sport class'''

    def upsert(self, id: UUID, data: Dict[str, Union[str, int, float, bool]]) -> None:
        '''Upsert a sport'''
        try:
            DB.get_instance().upsert(
                DB.get_instance().get_upsert_data(SportModel(id=id), data.keys()))
        except SQLAlchemyError as error:
            print(error)

    def delete(self, id: UUID) -> None:
        '''Delete a sport'''
        print('Delete a sport')

    def search(self, data: Dict[str, Union[str, int, float, bool]]) -> None:
        '''Search a sport'''
        print('Search a sport')
