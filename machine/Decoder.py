import logging
from typing import cast

from .Command import Command
from .ControlRegisters import ControlRegisters
from .DataMemory import DataMemory
from .DataStack import DataStack
from .Errors import NotImplementedOperation
from .IOPath import IOPath
from .cmds import *  # noqa: F403
from program import Operation, Op
from program.ops import *  # noqa: F403

log = logging.getLogger(__name__)

class Decoder(object):
    def __init__(self, cr: ControlRegisters, data: DataMemory, stack: DataStack, io: IOPath):
        self._cr = cr
        self._data = data
        self._stack = stack
        self._io = io

    def decode(self, op: Operation) -> Command:
        log.debug("decode: %s", op)
        cmd: Command
        match op.getOp():
            case Op.PUSH:
                cmd = CmdPush(cast(OpPush, op), self._cr, self._stack)
            case Op.SWAP:
                cmd = CmdSwap(self._cr, self._stack)
            case Op.OVER:
                cmd = CmdOver(self._cr, self._stack)
            case Op.DUP:
                cmd = CmdDup(self._cr, self._stack)
            case Op.ROL:
                cmd = CmdRol(self._cr, self._stack)
            case Op.DROP:
                cmd = CmdDrop(self._cr, self._stack)
            case Op.PUSHF:
                cmd = CmdPushf(self._cr, self._stack)
            case Op.POPF:
                cmd = CmdPopf(self._cr, self._stack)

            case Op.ADD:
                cmd = CmdAdd(self._cr, self._stack)
            case Op.SUB:
                cmd = CmdSub(self._cr, self._stack)
            case Op.MUL:
                cmd = CmdMul(self._cr, self._stack)
            case Op.DIV:
                cmd = CmdDiv(self._cr, self._stack)
            case Op.MOD:
                cmd = CmdMod(self._cr, self._stack)

            case Op.AND:
                cmd = CmdAnd(self._cr, self._stack)

            case Op.CMP:
                cmd = CmdCmp(self._cr, self._stack)

            case Op.JUMP:
                cmd = CmdJump(cast(OpJump, op), self._cr)
            case Op.JUMP_IF_ZERO:
                cmd = CmdJumpIfZero(cast(OpJumpIfZero, op), self._cr)
            case Op.JUMP_IF_BELOW:
                cmd = CmdJumpIfBelow(cast(OpJumpIfBelow, op), self._cr)
            case Op.RET:
                cmd = CmdRet(self._cr, self._stack)

            case Op.LOAD:
                cmd = CmdLoad(self._cr, self._stack, self._data)
            case Op.SAVE:
                cmd = CmdSave(self._cr, self._stack, self._data)

            case Op.OUT:
                cmd = CmdOut(self._cr, self._stack, self._io)
            case Op.IN:
                cmd = CmdIn(self._cr, self._stack, self._io)

            case Op.CLI:
                cmd = CmdCli(self._cr)
            case Op.STI:
                cmd = CmdSti(self._cr)

            case Op.HALT:
                cmd = CmdHalt(self._cr)
            case _:
                raise NotImplementedOperation(op)
        return cmd
