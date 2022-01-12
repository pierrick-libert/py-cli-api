'''Type checking object'''
import json
import uuid

from argparse import ArgumentTypeError


class TypeParser:
    '''Type parser object'''

    @classmethod
    def check_uuid(cls, uuid_str: str) -> uuid.UUID:
        '''Check if the data is an uuid'''
        try:
            return uuid.UUID(f'{uuid_str.strip()}')
        except (TypeError, ValueError) as error:
            raise ArgumentTypeError('Invalid uuid') from error

    @classmethod
    def check_json(cls, json_str: str):
        '''Check if the data is a proper JSON format'''
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as error:
            raise ArgumentTypeError('Invalid JSON data') from error

    @classmethod
    def check_type(cls, arg_type: str) -> str:
        '''Check if the type is within our scope'''
        if arg_type not in ['sport', 'event', 'selection', 'market']:
            raise ArgumentTypeError('Invalid type')
        return arg_type
