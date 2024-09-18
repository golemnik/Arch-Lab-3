from program import Op
from program.OperationBase import OperationBase


class OpDup(OperationBase):
    def __init__(self):
        super().__init__(Op.DUP, None, None)
