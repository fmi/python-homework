class BiDict(dict):
    ''' Bidirectional mapping data structure '''

    def __init__(self, plain_dict):
        self.update(plain_dict)

    def __setitem__(self, key, value):
        hash(value)
        self.pop(self._get_key_by_value(value), None)
        super().__setitem__(key, value)

    def __repr__(self):
        return 'BiDict(' + super().__repr__() + ')'

    def _get_key_by_value(self, value):
        ''' Returns key by given value '''
        for k, v in self.items():
            if v == value:
                return k

    def copy(self):
        return BiDict(super().copy())

    def update(self, plain_dict):
        for key, value in plain_dict.items():
            self.__setitem__(key, value)

    def inverse(self):
        inversed_dict = {value: key for key, value in self.items()}
        self.clear()
        self.update(inversed_dict)
