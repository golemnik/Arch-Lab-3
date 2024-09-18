from program import Op
from program.OperationBase import OperationBase


class OpSwap(OperationBase):
    def __init__(self):
        super().__init__(Op.SWAP, None, None)
