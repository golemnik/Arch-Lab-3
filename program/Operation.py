from abc import abstractmethod
from enum import StrEnum


class Op(StrEnum):
    HALT = 'halt'

    PUSH = 'push'
    DROP = 'drop'
    SWAP = 'swap'
    OVER = 'over'
    DUP = 'dup'
    ROL = 'rol'
    PUSHF = 'pushf'
    POPF = 'popf'

    LOAD = 'load'
    SAVE = 'save'

    ADD = 'add'
    SUB = 'sub'
    MUL = 'mul'
    DIV = 'div'
    MOD = 'mod'

    AND = 'and'

    CMP = 'cmp'

    RET = 'ret'
    JUMP = 'jump'
    JUMP_IF_ZERO = 'jz'
    JUMP_IF_BELOW = 'jb'

    IN = 'in'
    OUT = 'out'

    CLI = 'cli'
    STI = 'sti'


class Address(object):
    _address: int | None = None

    def setAddress(self, address: int):
        self._address = address

    def getAddress(self) -> int | None:
        return self._address


class Operation(object):
    @abstractmethod
    def getOp(self) -> Op:
        raise NotImplementedError

    @abstractmethod
    def getVal(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def getAddr(self) -> int:
        raise NotImplementedError
