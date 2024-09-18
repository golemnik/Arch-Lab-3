from program import Op
from program.OperationBase import OperationBase


class OpSave(OperationBase):
    def __init__(self):
        super().__init__(Op.SAVE, None, None)
