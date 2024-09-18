from program import Op
from program.OperationBase import OperationBase


class OpRol(OperationBase):
    def __init__(self):
        super().__init__(Op.ROL, None, None)
