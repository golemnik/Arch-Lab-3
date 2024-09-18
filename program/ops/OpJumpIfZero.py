from program.Operation import Op, Address
from program.OperationBase import OperationBase


class OpJumpIfZero(OperationBase):
    def __init__(self, addr: Address):
        super().__init__(Op.JUMP_IF_ZERO, None, addr)

    def __repr__(self):
        return "%s{ %s }" % (self._op, self.getAddr())
