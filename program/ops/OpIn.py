from program import Op
from program.OperationBase import OperationBase


class OpIn(OperationBase):
    def __init__(self):
        super().__init__(Op.IN, None, None)
