from program import Op
from program.OperationBase import OperationBase


class OpOut(OperationBase):
    def __init__(self):
        super().__init__(Op.OUT, None, None)
