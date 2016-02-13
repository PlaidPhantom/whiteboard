#!/bin/sh

if [[ $(shell python --version | sed -e 's/Python\s\([0-9]\).*/\1/') = 3 ]]; then
    PYTHON=python
else
    PYTHON=python3
endif

source ./venv/*/activate

$PYTHON whiteboard.py $@

deactivate
