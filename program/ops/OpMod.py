from program import Op
from program.OperationBase import OperationBase


class OpMod(OperationBase):
    def __init__(self):
        super().__init__(Op.MOD, None, None)
