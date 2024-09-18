import re
from typing import TextIO

_COMMENT_PREFIX = ';'
_LABEL_SUFFIX = ':'
_VARIABLE_SUFFIX = '='

_numberPat: re.Pattern = re.compile('^[+-]?\\d+$')

class Token(object):
    def getChars(self) -> str:
        return ''

    def isEndOfFile(self) -> bool:
        return False

    def isEndOfLine(self) -> bool:
        return False

    def isLabel(self) -> bool:
        return False

    def isVariable(self) -> bool:
        return False

    def isComment(self) -> bool:
        return False

    def isNumber(self) -> bool:
        return False

class OrdinaryToken(Token):
    def __init__(self, chars: str):
        self._chars = chars

    def __repr__(self):
        return "OrdinaryToken{'%s'}" % self._chars

    def getChars(self) -> str:
        return self._chars

    def isLabel(self) -> bool:
        return self._chars.endswith(_LABEL_SUFFIX)

    def isVariable(self) -> bool:
        return self._chars.endswith(_VARIABLE_SUFFIX)

    def isComment(self) -> bool:
        return self._chars.startswith(_COMMENT_PREFIX)

    def isNumber(self) -> bool:
        return True if _numberPat.fullmatch(self._chars) else False

class EolToken(Token):
    def isEndOfLine(self):
        return True

class EofToken(Token):
    def isEndOfFile(self) -> bool:
        return True

# text --> T T EOL T T T T EOL ...  T EOL EOF
class Tokenizer(object):
    def __init__(self, file: TextIO):
        self._file = file

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        line = self._file.readline()
        while len(line) > 0:
            tokens += self._tokenizeLine(line)
            line = self._file.readline()
        tokens.append(EofToken())
        return tokens

    @staticmethod
    def _tokenizeLine(line: str) -> list[Token]:
        tokens: list[Token] = []
        for chars in line.strip(' \n\r').split():
            tokens.append(OrdinaryToken(chars))
        if len(tokens) > 0:
            tokens.append(EolToken())
        return tokens
