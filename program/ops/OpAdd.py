from program import Op
from program.OperationBase import OperationBase


class OpAdd(OperationBase):
    def __init__(self):
        super().__init__(Op.ADD, None, None)
