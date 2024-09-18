from program.Operation import Op
from program.OperationBase import OperationBase


class OpHalt(OperationBase):
    def __init__(self):
        super().__init__(Op.HALT, None, None)
