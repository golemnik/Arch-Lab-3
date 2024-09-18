from ..CommandBase import CommandBase
from ..ControlRegisters import ControlRegisters
from ..DataMemory import DataMemory
from ..DataStack import DataStack


class CmdSave(CommandBase):
    def __init__(self, cr: ControlRegisters, stack: DataStack, data: DataMemory):
        super().__init__(cr)
        self._stack = stack
        self._data = data

    def _execute(self, stage: int) -> bool:
        match stage:
            case 0:
                self._cr.av = self._stack.pop()
            case 1:
                self._cr.bv = self._stack.pop()
            case 2:
                self._data.setAddress(self._cr.av)
            case 3:
                self._data.write(self._cr.bv)
        return 3 == stage
