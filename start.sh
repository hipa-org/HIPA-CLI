#!/bin/bash

if command -v python3 &>/dev/null; then
    python3 -m venv ./venv
else
    echo Python 3 is not installed.
    echo Aborting
    return
fi

source venv/bin/activate
pip install -r requirements.txt
python HIPA.py