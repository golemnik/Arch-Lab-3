import pytest
import io

from machine.IOPath import IOPath

_STDIN_PORT = 0
_STDOUT_PORT = 1
_READY_PORT = 2
_EOF_PORT = 3

@pytest.mark.parser
def test_empty_stdin():
    stdin = io.StringIO("")
    stdout = io.StringIO()
    iop = IOPath(stdin, stdout)
    assert 1 == iop.read(_EOF_PORT)

@pytest.mark.parser
def test_empty_lines_stdin():
    stdin = io.StringIO("\n\n\n\n")
    stdout = io.StringIO()
    iop = IOPath(stdin, stdout)
    assert 1 == iop.read(_EOF_PORT)

@pytest.mark.parser
def test_ignore_rest_of_line_stdin():
    stdin = io.StringIO("0 11 sdkfhkjsdhfkjds\n")
    stdout = io.StringIO()
    iop = IOPath(stdin, stdout)
    assert 0 == iop.read(_EOF_PORT)
    assert iop.step(0)
    assert 1 == iop.read(_EOF_PORT)
    assert 1 == iop.read(_READY_PORT)
    assert 11 == iop.read(_STDIN_PORT)


@pytest.mark.parser
def test_valid_stdin():
    stdin = io.StringIO("12 32\n 14 43\n20 54")
    stdout = io.StringIO()
    iop = IOPath(stdin, stdout)
    assert 0 == iop.read(_EOF_PORT)
    assert not iop.step(0)
    assert 0 == iop.read(_EOF_PORT)
    assert 0 == iop.read(_READY_PORT)
    assert not iop.step(1)
    assert 0 == iop.read(_EOF_PORT)
    assert 0 == iop.read(_READY_PORT)
    assert iop.step(12)
    assert 0 == iop.read(_EOF_PORT)
    assert 1 == iop.read(_READY_PORT)
    assert 32 == iop.read(_STDIN_PORT)
    assert not iop.step(12)
    assert 0 == iop.read(_EOF_PORT)
    assert 1 == iop.read(_READY_PORT)
    assert 32 == iop.read(_STDIN_PORT)

    # stdin port is not unlocked, input have to be ignored
    assert iop.step(14)
    assert 0 == iop.read(_EOF_PORT)
    assert 1 == iop.read(_READY_PORT)
    assert 32 == iop.read(_STDIN_PORT)
    iop.write(_READY_PORT, 765)
    assert 0 == iop.read(_READY_PORT)

    # stdin port is unlocked, input have to be accepted
    assert iop.step(20)
    assert 1 == iop.read(_EOF_PORT)
    assert 1 == iop.read(_READY_PORT)
    assert 54 == iop.read(_STDIN_PORT)
