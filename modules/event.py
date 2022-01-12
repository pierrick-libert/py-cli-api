'''Event class for business logic'''
from uuid import UUID
from typing import Dict, Union

from utils.interfaces import ModuleInterface


class Event(ModuleInterface):
    '''Event class'''

    def upsert(self, id: UUID, data: Dict[str, Union[str, int, float, bool]]) -> None:
        '''Upsert a Event'''
        print(f'Upsert a Event: {id}')

    def delete(self, id: UUID) -> None:
        '''Delete a Event'''
        print('Delete a Event')

    def search(self, data: Dict[str, Union[str, int, float, bool]]) -> None:
        '''Search a Event'''
        print('Search a Event')
