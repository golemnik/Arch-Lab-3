from typing import cast

from .Errors import MissedAddressError, MissedValueError
from .Operation import Operation, Address, Op


class OperationBase(Operation):
    _op: Op
    _val: int | None
    _addr: Address | None

    def __init__(self, op: Op, val: int | None, addr: Address | None):
        self._op = op
        self._val = val
        self._addr = addr

    def getOp(self) -> Op:
        return self._op

    def getVal(self) -> int:
        if self._val is None:
            raise MissedValueError(self._op)
        return self._val

    def getAddr(self) -> int:
        if self._addr is None or self._addr.getAddress() is None:
            raise MissedAddressError(self._op, self._addr)
        return cast(int, self._addr.getAddress())

    def __repr__(self):
        return "%s" % self._op
