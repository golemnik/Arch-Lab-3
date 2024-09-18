import contextlib
import io
import logging
import os
import tempfile

import pytest
from translator import Translator
from machine import Machine

log = logging.getLogger(__name__)

@pytest.mark.golden_test("golden/*/*.yaml")
def test_translator_and_machine(golden, caplog):
    caplog.set_level(logging.DEBUG)
    source: str = golden["source"]
    input: str = golden["stdin"]

    with tempfile.TemporaryDirectory() as tmpdir:
        target = os.path.join(tmpdir, "target.o")

        with contextlib.redirect_stdout(io.StringIO()) as sys_stdout:
            with open(source, "r+t", encoding="utf-8") as source_file:
                with open(target, "w+b") as destination_file:
                    Translator(source_file, destination_file).translate()

            with open(target, "r+b") as target_file:
                stdin = io.StringIO(input)
                stdout = io.StringIO()
                Machine(target_file).simulate(stdin, stdout)
                real_stdout = stdout.getvalue()
                expected_stdout = golden.out["stdout"]
                assert expected_stdout is not None
                assert real_stdout is not None
                log.debug("expected: %s", ":".join("{:02x}".format(ord(c)) for c in expected_stdout))
                log.debug("real    : %s", ":".join("{:02x}".format(ord(c)) for c in real_stdout))
                assert real_stdout == expected_stdout

        if golden.get("sys_stdout") is not None:
            assert sys_stdout == golden.out["sys_stdout"]

    if golden.get("logs") is not None:
        assert caplog.text == golden.out["logs"]
