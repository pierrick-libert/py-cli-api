'''Define decorators here'''

class Singleton:
    '''Singleton decorator'''

    def __init__(self, cls):
        '''Init method'''
        self._cls = cls

    # pylint: disable=attribute-defined-outside-init
    def get_instance(self):
        '''Getter for the instance'''
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        '''Do not allow a direct call'''
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        '''Check if that's correct instance'''
        return isinstance(inst, self._cls)
