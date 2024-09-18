from program import Op
from program.OperationBase import OperationBase


class OpOver(OperationBase):
    def __init__(self):
        super().__init__(Op.OVER, None, None)
