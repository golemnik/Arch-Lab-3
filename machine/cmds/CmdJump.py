from program.ops.OpJump import OpJump
from machine.CommandBase import CommandBase
from ..ControlRegisters import ControlRegisters
from ..Errors import UndefinedAddressError


class CmdJump(CommandBase):
    def __init__(self, op: OpJump, cr: ControlRegisters):
        super().__init__(cr)
        if op.getAddr() is None:
            raise UndefinedAddressError()
        self._address = op.getAddr()

    def _execute(self, stage: int) -> bool:
        self._cr.ip = self._address
        return True
