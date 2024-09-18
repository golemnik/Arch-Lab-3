from typing import BinaryIO, TextIO

from program import Program, marshal
from .Parser import Parser
from .Tokenizer import Tokenizer, Token


class Translator(object):
    def __init__(self, source: TextIO, destination: BinaryIO):
        self._source = source
        self._destination = destination

    def translate(self):
        tokens: list[Token] = Tokenizer(self._source).tokenize()
        program: Program = Parser(tokens).parse()
        buffer: bytes = marshal(program)
        self._destination.write(buffer)
