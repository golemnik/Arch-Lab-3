from machine.Errors import WrongAddressError
from program import Operation


class InstructionMemory(object):
    _operation: list[Operation]

    def __init__(self, operations: list[Operation]):
        self._operations = operations

    def read(self, address: int) -> Operation:
        if address < 0 or address >= len(self._operations):
            raise WrongAddressError(address)

        return self._operations[address]
