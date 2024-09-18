#!/bin/bash

ruff check $(find . -name '*.py' |grep -v venv)