from program.Operation import Op
from program.OperationBase import OperationBase


class OpPush(OperationBase):
    def __init__(self, val: int):
        super().__init__(Op.PUSH, val, None)

    def __repr__(self):
        return "%s{ %s }" % (self._op, self._val)
