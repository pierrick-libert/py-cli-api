'''Market class for business logic'''
from uuid import UUID
from typing import Dict, Union

from utils.interfaces import ModuleInterface


class Market(ModuleInterface):
    '''Market class'''

    def upsert(self, id: UUID, data: Dict[str, Union[str, int, float, bool]]) -> None:
        '''Upsert a Market'''
        print(f'Upsert a Market: {id}')

    def delete(self, id: UUID) -> None:
        '''Delete a Market'''
        print('Delete a Market')

    def search(self, data: Dict[str, Union[str, int, float, bool]]) -> None:
        '''Search a Market'''
        print('Search a Market')
