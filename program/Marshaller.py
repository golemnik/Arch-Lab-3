import pickle

from .Program import Program


def marshal(program: Program) -> bytes:
    buffer: bytes = pickle.dumps(program)
    return buffer


def unmarshal(buffer: bytes) -> Program:
    program: Program = pickle.loads(buffer)
    return program
