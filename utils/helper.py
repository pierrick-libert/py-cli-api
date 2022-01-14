'''A bunch of classes or functions to help the project'''
import re

from typing import Optional


# pylint: disable=too-few-public-methods
class Helper:
    '''Helper class'''

    @classmethod
    def slugify(cls, text: str) -> Optional[str]:
        '''Slugify a string'''
        if isinstance(text, str) is False:
            return None
        return re.sub(r'[\W_]+', '-', text.strip().lower()).strip('-')
