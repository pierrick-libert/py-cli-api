'''Selection class for business logic'''
from uuid import UUID
from typing import Dict, Union

from utils.interfaces import ModuleInterface


class Selection(ModuleInterface):
    '''Selection class'''

    def upsert(self, id: UUID, data: Dict[str, Union[str, int, float, bool]]) -> None:
        '''Upsert a Selection'''
        print(f'Update a Selection: {id}')

    def delete(self, id: UUID) -> None:
        '''Delete a Selection'''
        print('Delete a Selection')

    def search(self, data: Dict[str, Union[str, int, float, bool]]) -> None:
        '''Search a Selection'''
        print('Search a Selection')
