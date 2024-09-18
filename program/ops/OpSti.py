from program import Op
from program.OperationBase import OperationBase


class OpSti(OperationBase):
    def __init__(self):
        super().__init__(Op.STI, None, None)
