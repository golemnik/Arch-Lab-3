from machine.CommandBase import CommandBase
from ..ControlRegisters import ControlRegisters
from ..DataStack import DataStack


class CmdAdd(CommandBase):
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
                self._cr.cv = self._cr.av + self._cr.bv  # TODO: handle overflow
            case 3:
                self._stack.push(self._cr.cv)
        return 3 == stage
