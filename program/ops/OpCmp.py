from program import Op
from program.OperationBase import OperationBase


class OpCmp(OperationBase):
    def __init__(self):
        super().__init__(Op.CMP, None, None)
