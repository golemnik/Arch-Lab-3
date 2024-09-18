import logging

log = logging.getLogger(__name__)
dumper = logging.getLogger("S")

class DataMemory(object):
    def __init__(self, data: list[int], capacity: int = 1024):
        self._address = 0
        self._data = [0] * capacity
        addr = 0
        for val in data:
            self._data[addr] = val
            addr += 1

    def setAddress(self, address: int):
        self._address = address

    def read(self) -> int:
        return self._data[self._address]

    def write(self, value: int) -> None:
        self._data[self._address] = value

    def logState(self):
        dumper.debug("   Data memory: AR=%d  memory[AR]=%d", self._address, self._data[self._address])
