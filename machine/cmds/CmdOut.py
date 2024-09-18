from machine.CommandBase import CommandBase
from ..ControlRegisters import ControlRegisters
from ..DataStack import DataStack
from ..IOPath import IOPath


class CmdOut(CommandBase):
    def __init__(self, cr: ControlRegisters, stack: DataStack, io: IOPath):
        super().__init__(cr)
        self._stack = stack
        self._io = io

    def _execute(self, stage: int) -> bool:
        match stage:
            case 0:
                self._cr.av = self._stack.pop()
            case 1:
                self._cr.bv = self._stack.pop()
            case 2:
                self._io.write(self._cr.av, self._cr.bv)
        return 2 == stage
