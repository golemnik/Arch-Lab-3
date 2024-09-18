import logging

from .Errors import NegativeStackPositionError, OutOfStackError

log = logging.getLogger(__name__)
dumper = logging.getLogger("S")


class DataStack(object):
    _pos: int
    _stack: list[int]

    def __init__(self):
        self.reset()

    def reset(self):
        self._pos = 0
        self._stack = []

    def push(self, val: int) -> None:
        self._stack.append(val)

    def pop(self) -> int:
        if 0 == len(self._stack):
            raise OutOfStackError()
        return self._stack.pop()

    # 0 1 2 3 4
    # top ... bottom
    def setPosition(self, pos: int):
        if pos < 0:
            raise NegativeStackPositionError(pos)
        self._pos = pos

    def pick(self) -> int:
        if self._pos >= len(self._stack):
            raise OutOfStackError()
        return self._stack[-self._pos - 1]

    def logState(self):
        stack = self._stack.copy()
        stack.reverse()
        dumper.debug("    Data stack: PR=%d top[ %s ]bottom", self._pos, " ".join(map(str, stack)))
