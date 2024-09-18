class ControlRegisters(object):
    _halt: bool
    ip: int
    zf: bool
    bf: bool
    rf: bool

    av: int
    bv: int
    cv: int

    def __init__(self):
        self.reset(0)

    def reset(self, ip: int) -> None:
        self._halt = False
        self.zf = False
        self.bf = False
        self.rf = False
        self.ip = ip
        self.av = 0
        self.bv = 0
        self.cv = 0

    def halt(self) -> None:
        self._halt = True

    def isHalt(self) -> bool:
        return self._halt
