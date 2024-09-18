class NegativeStackPositionError(Exception):
    def __init__(self, pos: int):
        self._pos = pos

class OutOfStackError(Exception):
    pass

class WrongAddressError(Exception):
    pass

class NotImplementedOperation(Exception):
    pass

class UndefinedAddressError(Exception):
    pass

class WrongInputPortError(Exception):
    pass

class WrongOutputPortError(Exception):
    pass
