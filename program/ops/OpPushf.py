from program.Operation import Op
from program.OperationBase import OperationBase


class OpPushf(OperationBase):
    def __init__(self):
        super().__init__(Op.PUSHF, None, None)
