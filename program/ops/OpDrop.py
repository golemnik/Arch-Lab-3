from program import Op
from program.OperationBase import OperationBase


class OpDrop(OperationBase):
    def __init__(self):
        super().__init__(Op.DROP, None, None)
