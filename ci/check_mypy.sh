#!/bin/bash

mypy --python-version 3.12 \
    --check-untyped-defs --show-error-code-links\
    machine_cli.py \
    translator_cli.py \
    $(find . -name '*_test.py' |grep -v venv)
