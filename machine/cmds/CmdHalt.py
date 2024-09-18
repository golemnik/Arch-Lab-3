from machine.CommandBase import CommandBase
from ..ControlRegisters import ControlRegisters


class CmdHalt(CommandBase):
    def __init__(self, cr: ControlRegisters):
        super().__init__(cr)

    def _execute(self, stage: int) -> bool:
        self._cr.halt()
        return True
