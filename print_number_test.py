import io
import logging
import os
import tempfile

import pytest

from translator import Translator
from machine import Machine

log = logging.getLogger(__name__)

@pytest.mark.parametrize("number", [0, 8, 10, 42, 100, 4613732])
def test_translator_and_machine(number: int):
    source: str = """
            jump main
            ret
    done:   halt
    main:   push done   ; --> A
            push %d     ; --> N A
    print:              
            push 10     ; --> 10 N A
            cmp         ; --> N A ?BF=(10 < N)
            jb next
            jz next

    prev:               ; --> N A
            push 48     ; --> '0' N A
            add         ; --> C A
            push 1      ; --> 1 C A
            out         ; --> A
            ret

    next:
            dup         ; --> N N A0
            push 10     ; --> 10 N N A0
            swap        ; --> N 10 N A0
            mod         ; --> (N mod 10) N A0
            swap        ; --> N (N mod 10) A0
            push 10     ; --> 10 N (N mod 10) A0
            swap        ; --> N 10 (N mod 10) A0
            div         ; --> N/10 (N mod 10) A0
            push prev   ; --> A N/10 (N mod 10) A0
            swap        ; --> N/10 A (N mod 10) A0
            jump print
    """ % number

    with tempfile.TemporaryDirectory() as tmpdir:
        target = os.path.join(tmpdir, "target.o")

        source_file = io.StringIO(source)
        with open(target, "w+b") as destination_file:
            Translator(source_file, destination_file).translate()

        with open(target, "r+b") as target_file:
            stdin = io.StringIO("")
            stdout = io.StringIO()
            Machine(target_file).simulate(stdin, stdout)
            real_stdout = stdout.getvalue()
            expected_stdout = str(number)
            assert real_stdout is not None
            log.debug("expected: %s", ":".join("{:02x}".format(ord(c)) for c in expected_stdout))
            log.debug("real    : %s", ":".join("{:02x}".format(ord(c)) for c in real_stdout))
            assert real_stdout == expected_stdout
