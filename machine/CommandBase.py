from abc import abstractmethod

from .Command import Command
from .ControlRegisters import ControlRegisters


class CommandBase(Command):
    _stage: int = 0

    def __init__(self, cr: ControlRegisters):
        self._cr = cr

    def execute(self) -> bool:
        if self._stage == 0:
            self._cr.ip += 1
        finished = self._execute(self._stage)
        self._stage += 1
        return finished

    @abstractmethod
    def _execute(self, stage: int) -> bool:
        raise NotImplementedError()
