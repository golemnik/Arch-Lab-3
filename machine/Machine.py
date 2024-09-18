import logging
from typing import BinaryIO, TextIO

from .ControlUnit import ControlUnit
from program import unmarshal
from .DataMemory import DataMemory
from .DataStack import DataStack
from .IOPath import IOPath
from .InstructionMemory import InstructionMemory


log = logging.getLogger(__name__)
dumper = logging.getLogger("S")

class Machine(object):
    def __init__(self, source: BinaryIO):
        self._source = source

    def simulate(self, stdin: TextIO, stdout: TextIO) -> None:
        buffer = self._source.read()
        program = unmarshal(buffer)
        instruction_memory = InstructionMemory(program.getOperations())
        data_memory = DataMemory(program.getData())
        stack = DataStack()
        io = IOPath(stdin, stdout)

        cu = ControlUnit(instruction_memory, data_memory, stack, io)
        while not cu.isHalt():
            if True:  # not cu.isInsideCommand():
                dumper.debug("----------------")
                cu.logState()
                stack.logState()
                data_memory.logState()
                io.logState()
            cu.step()

        log.debug("---------------- HALT")
