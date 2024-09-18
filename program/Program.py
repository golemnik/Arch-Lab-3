from .Operation import Operation


class Program(object):
    def __init__(self, ops: list[Operation], data: list[int]):
        self._ops = ops
        self._data = data

    def getOperations(self) -> list[Operation]:
        return self._ops

    def getData(self) -> list[int]:
        return self._data
