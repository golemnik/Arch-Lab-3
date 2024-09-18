from machine.CommandBase import CommandBase
from ..ControlRegisters import ControlRegisters
from ..DataStack import DataStack


class CmdPushf(CommandBase):
    def __init__(self, cr: ControlRegisters, stack: DataStack):
        super().__init__(cr)
        self._stack = stack

    def _execute(self, stage: int) -> bool:
        match stage:
            case 0:
                self._stack.push(int(self._cr.zf))
            case 1:
                self._stack.push(int(self._cr.bf))
        return 1 == stage
