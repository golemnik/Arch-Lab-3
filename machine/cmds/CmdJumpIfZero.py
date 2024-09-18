from program.ops.OpJumpIfZero import OpJumpIfZero
from machine.CommandBase import CommandBase
from ..ControlRegisters import ControlRegisters
from ..Errors import UndefinedAddressError


class CmdJumpIfZero(CommandBase):
    def __init__(self, op: OpJumpIfZero, cr: ControlRegisters):
        super().__init__(cr)
        if op.getAddr() is None:
            raise UndefinedAddressError()
        self._address = op.getAddr()

    def _execute(self, stage: int) -> bool:
        if self._cr.zf:
            self._cr.ip = self._address
        return True
