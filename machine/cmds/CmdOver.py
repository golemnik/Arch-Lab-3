from machine.CommandBase import CommandBase
from ..ControlRegisters import ControlRegisters
from ..DataStack import DataStack


class CmdOver(CommandBase):
    def __init__(self, cr: ControlRegisters, stack: DataStack):
        super().__init__(cr)
        self._stack = stack

    def _execute(self, stage: int) -> bool:
        match stage:
            case 0:
                self._cr.av = 1
            case 1:
                self._stack.setPosition(self._cr.av)
            case 2:
                self._cr.av = self._stack.pick()
            case 3:
                self._stack.push(self._cr.av)
        return 3 == stage
