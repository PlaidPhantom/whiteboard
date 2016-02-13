#!/bin/sh

if [[ $(python --version | sed -e 's/Python\s\([0-9]\).*/\1/') = 3 ]]; then
    PYTHON=python
else
    PYTHON=python3
fi

source ./venv/*/activate

$PYTHON site.py $@

deactivate
