from enum import StrEnum
from typing import cast

from program import Program, Operation, Address
from program.ops import *  # noqa: F403
from .Errors import UnknownOperationError, NotLabelError, UndefinedLabelError, DuplicateLabelError, \
    DuplicateVariableError, WrongVariableDataError, UnexpectedEndOfFileError, GarbageBeforeEndOfLineError, \
    UnexpectedEndOfLineError, NotVariableOrLabelError, UndefinedVariableError, NoMoreTokensError
from .Tokenizer import Token


class ParserState(StrEnum):
    START_OF_LINE = 'sol'
    VARIABLE = 'variable'
    BEFORE_VARIABLE_DATA = 'before_variable_data'
    BEFORE_VARIABLE_DATA_OR_COMMENT = 'before_variable_data_or_comment'
    VARIABLE_DATA = 'variable_data'
    LABEL = 'label'
    BEFORE_OPERATION_OR_COMMENT = 'operation_or_comment'
    OPERATION = 'operation'
    BEFORE_COMMENT = 'comment_only'
    COMMENT = 'comment'
    END_OF_LINE = 'eol'
    END_OF_FILE = 'eof'



class Parser(object):
    def __init__(self, tokens: list[Token]):
        self._tokens = tokens
        self._refs: list[Address] = []
        self._labels: dict[str, Address] = {}
        self._variables: dict[str, Address] = {}

    def parse(self) -> Program:
        token: Token | None = None
        ops: list[Operation] = []
        data: list[int] = []
        state: ParserState = ParserState.START_OF_LINE
        while state != ParserState.END_OF_FILE:
            match state:
                case ParserState.START_OF_LINE:
                    state, token = self._whenStartOfLine()
                case ParserState.BEFORE_OPERATION_OR_COMMENT:
                    state, token = self._whenBeforeOperationOrComment()
                case ParserState.BEFORE_COMMENT:
                    state, token = self._whenBeforeComment()
                case ParserState.BEFORE_VARIABLE_DATA_OR_COMMENT:
                    state, token = self._whenBeforeVariableDataOrComment()
                case ParserState.BEFORE_VARIABLE_DATA:
                    state, token = self._whenBeforeVariableData()

                case ParserState.COMMENT:
                    state = self._whenComment()
                case ParserState.VARIABLE:
                    state = self._whenVariable(cast(Token, token), len(data))
                case ParserState.LABEL:
                    state = self._whenLabel(cast(Token, token), len(ops))
                case ParserState.VARIABLE_DATA:
                    state, val = self._whenVariableData(cast(Token, token))
                    data.append(val)
                case ParserState.OPERATION:
                    state, op = self._whenOperation(cast(Token, token))
                    ops.append(op)

        self._checkAllLabelsAreDefined()
        return Program(ops, data)

    def _checkAllLabelsAreDefined(self):
        for label_name in self._labels:
            label = self._labels[label_name]
            if label.getAddress() is None:
                raise UndefinedLabelError(label_name)

    def _whenOperation(self, token: Token) -> tuple[ParserState, Operation]:
        op = token.getChars()
        return ParserState.START_OF_LINE, self._parseOperation(op)

    def _whenLabel(self, token: Token, address: int) -> ParserState:
        name = token.getChars()
        if name in self._labels:
            label = self._labels[name]
            if label.getAddress() is not None:
                raise DuplicateLabelError(label)
            label.setAddress(address)
        else:
            self._addLabel(name, address)
        return ParserState.START_OF_LINE

    def _whenVariable(self, token: Token, address: int) -> ParserState:
        name = token.getChars()
        if name in self._variables:
            var = self._variables[name]
            if var.getAddress() is not None:
                raise DuplicateVariableError(var)
            var.setAddress(address)
        else:
            self._addVariable(name, address)
        return ParserState.BEFORE_VARIABLE_DATA

    @staticmethod
    def _whenVariableData(token: Token) -> tuple[ParserState, int]:
        if not token.isNumber():
            raise WrongVariableDataError(token)
        val = token.getChars()
        return ParserState.BEFORE_VARIABLE_DATA_OR_COMMENT, int(val)

    def _whenComment(self) -> ParserState:
        while not self._nextToken().isEndOfLine():
            pass
        return ParserState.START_OF_LINE

    def _whenBeforeVariableDataOrComment(self) -> tuple[ParserState, Token]:
        token = self._nextToken()
        state: ParserState
        if token.isEndOfFile():
            raise UnexpectedEndOfFileError(token)
        elif token.isEndOfLine():
            state = ParserState.START_OF_LINE
        elif token.isNumber():
            state = ParserState.VARIABLE_DATA
        elif token.isComment():
            state = ParserState.COMMENT
        else:
            raise GarbageBeforeEndOfLineError(token)
        return state, token

    def _whenBeforeVariableData(self) -> tuple[ParserState, Token]:
        token = self._nextToken()
        state: ParserState
        if token.isEndOfFile():
            raise UnexpectedEndOfFileError(token)
        elif token.isEndOfLine():
            raise UnexpectedEndOfLineError(token)
        elif token.isNumber():
            state = ParserState.VARIABLE_DATA
        else:
            raise GarbageBeforeEndOfLineError(token)
        return state, token

    def _whenBeforeComment(self) -> tuple[ParserState, Token]:
        token = self._nextToken()
        state: ParserState
        if token.isEndOfFile():
            raise UnexpectedEndOfFileError(token)
        elif token.isEndOfLine():
            state = ParserState.START_OF_LINE
        elif token.isComment():
            state = ParserState.COMMENT
        else:
            raise GarbageBeforeEndOfLineError(token)
        return state, token

    def _whenBeforeOperationOrComment(self) -> tuple[ParserState, Token]:
        token = self._nextToken()
        state: ParserState
        if token.isEndOfFile():
            raise UnexpectedEndOfFileError(token)
        elif token.isEndOfLine():
            state = ParserState.START_OF_LINE
        elif token.isComment():
            state = ParserState.COMMENT
        else:
            state = ParserState.OPERATION
        return state, token

    def _whenStartOfLine(self) -> tuple[ParserState, Token]:
        token = self._nextToken()
        state: ParserState
        if token.isEndOfFile():
            state = ParserState.END_OF_FILE
        elif token.isEndOfLine():
            state = ParserState.START_OF_LINE
        elif token.isComment():
            state = ParserState.COMMENT
        elif token.isLabel():
            state = ParserState.LABEL
        elif token.isVariable():
            state = ParserState.VARIABLE
        else:
            state = ParserState.OPERATION
        return state, token

    def _parseOperation(self, op: str) -> Operation:
        operation: Operation
        match op:
            case 'pushf':
                operation = OpPushf()
            case 'popf':
                operation = OpPopf()
            case 'push':
                operation = OpPush(self._nextNumberOrVariableOrLabel(op))
            case 'swap':
                operation = OpSwap()
            case 'over':
                operation = OpOver()
            case 'dup':
                operation = OpDup()
            case 'drop':
                operation = OpDrop()
            case 'rol':
                operation = OpRol()

            case 'add':
                operation = OpAdd()
            case 'sub':
                operation = OpSub()
            case 'mul':
                operation = OpMul()
            case 'div':
                operation = OpDiv()
            case 'mod':
                operation = OpMod()

            case 'and':
                operation = OpAnd()

            case 'cmp':
                operation = OpCmp()

            case 'jump':
                operation = OpJump(self._nextReference(op))
            case 'jz':
                operation = OpJumpIfZero(self._nextReference(op))
            case 'jb':
                operation = OpJumpIfBelow(self._nextReference(op))
            case 'ret':
                operation = OpRet()

            case 'out':
                operation = OpOut()
            case 'in':
                operation = OpIn()

            case 'load':
                operation = OpLoad()
            case 'save':
                operation = OpSave()

            case 'cli':
                operation = OpCli()
            case 'sti':
                operation = OpSti()

            case 'halt':
                operation = OpHalt()
            case _:
                raise UnknownOperationError(op)
        return operation

    def _nextReference(self, op) -> Address:
        token = self._nextToken()
        if token.isComment() or token.isEndOfLine() or token.isEndOfFile():
            raise NotLabelError(op, token)
        label_name = token.getChars() + ':'
        ref = self._labels[label_name] \
            if label_name in self._labels \
            else self._addLabel(label_name, None)
        return ref

    def _nextNumberOrVariableOrLabel(self, op) -> int:
        token = self._nextToken()
        if token.isComment() or token.isEndOfLine() or token.isEndOfFile():
            raise NotVariableOrLabelError(op, token)
        elif token.isNumber():
            return int(token.getChars())
        name = token.getChars() + '='
        if name in self._variables:
            if self._variables[name].getAddress() is None:
                raise UndefinedVariableError(op, token)
            return cast(int, self._variables[name].getAddress())
        name = token.getChars() + ':'
        if name in self._labels:
            if self._labels[name].getAddress() is None:
                raise UndefinedLabelError(op, token)
            return cast(int, self._labels[name].getAddress())
        raise NotVariableOrLabelError(op, token)

    def _addLabel(self, name: str, addr: int | None) -> Address:
        address = Address()
        if addr is not None:
            address.setAddress(addr)
        self._labels[name] = address
        self._refs.append(address)
        return address

    def _addVariable(self, name: str, addr: int | None) -> Address:
        address = Address()
        if addr is not None:
            address.setAddress(addr)
        self._variables[name] = address
        return address


    def _nextToken(self) -> Token:
        if 0 == len(self._tokens):
            raise NoMoreTokensError()
        return self._tokens.pop(0)
