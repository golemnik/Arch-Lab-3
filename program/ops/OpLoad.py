from program import Op
from program.OperationBase import OperationBase


class OpLoad(OperationBase):
    def __init__(self):
        super().__init__(Op.LOAD, None, None)
