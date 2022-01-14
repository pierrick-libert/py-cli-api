'''Create an interface to force module to implement the needed method for this program to work'''
from abc import ABCMeta, abstractmethod
from uuid import UUID
from typing import Dict, Union


class ModuleInterface(metaclass=ABCMeta):
    '''Module interface'''

    @abstractmethod
    def upsert(self, uuid: UUID, data: Dict[str, Union[str, int, float, bool]]) -> None:
        '''Implement an upsert method to insert or update an object in DB'''

    @abstractmethod
    def delete(self, uuid: UUID) -> None:
        '''Implement a delete method to remove an object in DB'''

    @abstractmethod
    def search(self, data: Dict[str, Union[str, int, float, bool]]) -> None:
        '''Implement a search method to get object(s) from the DB'''
