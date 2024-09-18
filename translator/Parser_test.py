import pytest

from program import Program
from program.ops import OpHalt, OpJump
from translator.Errors import UndefinedLabelError
from translator.Parser import Parser
from translator.Tokenizer import Token, OrdinaryToken, EolToken, EofToken


@pytest.mark.parser
def test_unknown_label():
    tokens: list[Token] = [
        OrdinaryToken("jump"),
        OrdinaryToken("done"),
        EolToken(),
        EofToken()
    ]
    with pytest.raises(UndefinedLabelError):
        Parser(tokens).parse()


@pytest.mark.parser
def test_forward_label():
    tokens: list[Token] = [
        OrdinaryToken("jump"),
        OrdinaryToken("done"),
        EolToken(),
        OrdinaryToken("done:"),
        OrdinaryToken("halt"),
        EolToken(),
        EofToken()
    ]
    p: Program = Parser(tokens).parse()
    ops = p.getOperations()
    assert len(ops) == 2
    assert isinstance(ops[0], OpJump)
    assert ops[0].getAddr() == 1
    assert isinstance(ops[1], OpHalt)


@pytest.mark.parser
def test_backward_label():
    tokens: list[Token] = [
        OrdinaryToken("done:"),
        EolToken(),
        OrdinaryToken("halt"),
        EolToken(),
        OrdinaryToken("jump"),
        OrdinaryToken("done"),
        EolToken(),
        EofToken()
    ]
    p: Program = Parser(tokens).parse()
    ops = p.getOperations()
    assert len(ops) == 2
    assert isinstance(ops[0], OpHalt)
    assert isinstance(ops[1], OpJump)
    assert ops[1].getAddr() == 0
