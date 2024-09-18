from machine.CommandBase import CommandBase
from ..ControlRegisters import ControlRegisters
from ..DataStack import DataStack


class CmdCmp(CommandBase):
    def __init__(self, cr: ControlRegisters, stack: DataStack):
        super().__init__(cr)
        self._stack = stack

    def _execute(self, stage: int) -> bool:
        match stage:
            case 0:
                self._cr.av = self._stack.pop()
            case 1:
                self._cr.bv = 0
            case 2:
                self._stack.setPosition(self._cr.bv)
            case 3:
                self._cr.bv = self._stack.pick()
            case 4:
                self._cr.zf = (self._cr.av == self._cr.bv)
                self._cr.bf = (self._cr.av < self._cr.bv)
        return 4 == stage
