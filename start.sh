#!/bin/bash

echo "Checking Python version..."

if command -v python3 &>/dev/null; then
    echo "Found Python 3"
    python3 -m venv ./venv


    if [ $? -eq 0 ]; then
        echo OK
	echo Starting virtual environment
        source venv/bin/activate
        pip install -r requirements.txt
        python3 HIPA.py
    else
        echo "Could not execute python -m venv ./venv"
        echo "Edit the script. Change the 'python' command to the one calling python3."
    fi

else
    echo "Python 3 is not installed."
    echo "Aborting"
fi

