import logging

from program import Operation
from .Command import Command
from .ControlRegisters import ControlRegisters
from .InstructionMemory import InstructionMemory
from .DataMemory import DataMemory
from .DataStack import DataStack
from .Decoder import Decoder
from .IOPath import IOPath

log = logging.getLogger(__name__)
dumper = logging.getLogger("S")

_MAIN_ENTRY:         int = 0
_INTERRUPTION_ENTRY: int = 1

class ControlUnit(object):
    _tik: int = 0
    _cmd: Command | None = None
    _interrupted: bool = False
    _ignored_interrupts: int = 0

    def __init__(self, cmds: InstructionMemory, data: DataMemory, stack: DataStack, io: IOPath):
        self._cr = ControlRegisters()
        self._io = io
        self._stack = stack
        self._cmds = cmds
        self._decoder = Decoder(self._cr, data, stack, io)
        self.reset()

    def reset(self):
        self._tik = 0
        self._cr.reset(_MAIN_ENTRY)

    def step(self) -> bool:
        if self._io.step(self._tik):
            if self._interrupted:
                self._ignored_interrupts += 1
            else:
                self._interrupted = True
        if self._cmd is None:
            if self._interrupted:
                self._interrupted = False
                if not self._cr.rf:
                    self._stack.push(self._cr.ip)
                    self._cr.ip = _INTERRUPTION_ENTRY
                    self._cr.rf = True
                else:
                    self._ignored_interrupts += 1
            self._cmd = self._decode(self._cr.ip)
        if self._cmd.execute():
            self._cmd = None
        self._tik += 1
        return self._cr.isHalt()

    def isHalt(self):
        return self._cr.isHalt()

    def isInsideCommand(self):
        return self._cmd is not None

    def _decode(self, ip) -> Command:
        op: Operation = self._cmds.read(ip)
        return self._decoder.decode(op)

    def logState(self):
        dumper.debug(
            "  Control Unit: tik=%d HLT=%s IP=%d  AV=%d BV=%d CV=%d  ZF=%s BF=%s RF=%s  ignored INTs=%d",
            self._tik, self._cr.isHalt(),
            self._cr.ip,
            self._cr.av, self._cr.bv, self._cr.cv,
            self._cr.zf, self._cr.bf, self._cr.rf,
            self._ignored_interrupts
        )
