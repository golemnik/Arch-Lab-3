from machine.CommandBase import CommandBase
from ..ControlRegisters import ControlRegisters
from ..DataStack import DataStack


class CmdSwap(CommandBase):
    def __init__(self, cr: ControlRegisters, stack: DataStack):
        super().__init__(cr)
        self._stack = stack

    def _execute(self, stage: int) -> bool:
        match stage:
            case 0:
                self._cr.av = self._stack.pop()
            case 1:
                self._cr.bv = self._stack.pop()
            case 2:
                self._stack.push(self._cr.av)
            case 3:
                self._stack.push(self._cr.bv)
        return 3 ==stage
