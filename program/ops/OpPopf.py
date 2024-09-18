from program.Operation import Op
from program.OperationBase import OperationBase


class OpPopf(OperationBase):
    def __init__(self):
        super().__init__(Op.POPF, None, None)
