from io import StringIO

from machine.InstructionMemory import InstructionMemory
from machine.ControlUnit import ControlUnit
from machine.DataMemory import DataMemory
from machine.DataStack import DataStack
from machine.IOPath import IOPath
from program import Operation
from program.ops import OpHalt


def test_halt():
    ops: list[Operation] = [OpHalt()]
    data: list[int] = []
    pm = InstructionMemory(ops)
    dm = DataMemory(data)
    stack = DataStack()
    stdin = StringIO()
    stdout = StringIO()
    io = IOPath(stdin, stdout)
    cu = ControlUnit(pm, dm, stack, io)
    cu.reset()
    cu.step()
