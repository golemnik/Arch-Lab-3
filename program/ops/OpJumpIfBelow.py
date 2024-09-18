from program.Operation import Op, Address
from program.OperationBase import OperationBase


class OpJumpIfBelow(OperationBase):
    def __init__(self, addr: Address):
        super().__init__(Op.JUMP_IF_BELOW, None, addr)

    def __repr__(self):
        return "%s{ %s }" % (self._op, self.getAddr())
