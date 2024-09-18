from program import Op
from program.OperationBase import OperationBase


class OpRet(OperationBase):
    def __init__(self):
        super().__init__(Op.RET, None, None)
