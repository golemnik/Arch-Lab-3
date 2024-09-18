import logging
from typing import TextIO

from machine.Errors import WrongInputPortError, WrongOutputPortError

log = logging.getLogger(__name__)
dumper = logging.getLogger("S")

# ports:
# 0 - in     - stdin
# 1 - out    - stdout
# 2 - in/out - stdin blocked/ready flag
# 3 - in     - closed stdin flag

class IOPath(object):
    _nextTik: int = -1
    _nextValue: int = -1
    _inPortValue: int = 0
    _inPortLockedFlag: int = 0
    _outPortValue: int = 0

    def __init__(self, inp: TextIO, outp: TextIO):
        self._input = inp
        self._output = outp
        self._readNextEvent()

    def step(self, tik: int) -> bool:
        time_to_interrupt = (tik == self._nextTik)
        if time_to_interrupt:
            if 0 == self._inPortLockedFlag:
                self._inPortValue = self._nextValue
                self._inPortLockedFlag = 1
            self._readNextEvent()
        return time_to_interrupt

    def read(self, port: int) -> int:
        match port:
            case 0:  # stdin port
                return self._inPortValue
            case 2:  # stdin port locked flag
                return self._inPortLockedFlag
            case 3:  # closed stdin flag
                return self._getClosedInputFlag()
        raise WrongInputPortError(port)

    def _getClosedInputFlag(self):
        return 1 if self._nextTik < 0 else 0

    def write(self, port: int, val: int) -> None:
        match port:
            case 1:  # stdout port
                self._outPortValue = val
                self._output.write(chr(self._outPortValue))
                return
            case 2:  # stdin port locked flag, unlocking
                self._inPortLockedFlag = 0
                return
        raise WrongOutputPortError(port)

    def _readNextEvent(self):
        while True:
            line = self._input.readline()  # <tik> <val>
            if line is None or 0 == len(line):
                self._nextTik = -1
                self._nextValue = -1
                return

            line = line.strip()
            if len(line) > 0:
                parts = line.split(" ")
                self._nextTik = int(parts[0])
                self._nextValue = int(parts[1])
                return

    def logState(self):
        nextIntr = "next interruption at tik=%d with val=%s" % (self._nextTik, self._nextValue) \
            if self._nextTik >= 0 else ""
        dumper.debug(
            "       I/O path: ports=[%d %d %d %d] %s",
            self._inPortValue, self._outPortValue, self._inPortLockedFlag, self._getClosedInputFlag(), nextIntr
        )
