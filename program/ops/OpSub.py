from program import Op
from program.OperationBase import OperationBase


class OpSub(OperationBase):
    def __init__(self):
        super().__init__(Op.SUB, None, None)
