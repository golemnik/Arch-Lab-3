from abc import abstractmethod


class Command(object):
    @abstractmethod
    def execute(self) -> bool:
        raise NotImplementedError()

