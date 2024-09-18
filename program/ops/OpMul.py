from program import Op
from program.OperationBase import OperationBase


class OpMul(OperationBase):
    def __init__(self):
        super().__init__(Op.MUL, None, None)
