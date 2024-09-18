from program import Op
from program.OperationBase import OperationBase


class OpCli(OperationBase):
    def __init__(self):
        super().__init__(Op.CLI, None, None)
