from program import Op
from program.OperationBase import OperationBase


class OpAnd(OperationBase):
    def __init__(self):
        super().__init__(Op.AND, None, None)
