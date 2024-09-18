from program.ops import OpPush
from machine.CommandBase import CommandBase
from ..ControlRegisters import ControlRegisters
from ..DataStack import DataStack


class CmdPush(CommandBase):
    def __init__(self, op: OpPush, cr: ControlRegisters, stack: DataStack):
        super().__init__(cr)
        self._stack = stack
        self._val = op.getVal()

    def _execute(self, stage: int) -> bool:
        self._stack.push(self._val)
        return True
