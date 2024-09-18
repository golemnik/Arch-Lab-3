from program import Op
from program.OperationBase import OperationBase


class OpDiv(OperationBase):
    def __init__(self):
        super().__init__(Op.DIV, None, None)
