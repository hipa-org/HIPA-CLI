#!/bin/bash

echo "Checking Python version..."

if command -v python3 &>/dev/null; then
    echo "Found Python 3"
    python3 -m venv ./venv


    if [ $? -eq 0 ]; then
        echo Creating sql files...
        cp ./SQL/Base/00_mysql_user.sql.dist ./SQL/Base/00_mysql_user.sql
        cp ./SQL/Base/01_create_schema.sql.dist ./SQL/Base/01_create_schema.sql
        cp ./SQL/Base/02_create_tables.sql.dist ./SQL/Base/02_create_tables.sql

	      echo Starting virtual environment
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r ./src/requirements.txt
        python3 ./src/HIPA.py -s $2 $3 $4 $5
    else
        echo "Could not execute python -m venv ./venv"
        echo "Edit the script. Change the 'python' command to the one calling python3."
    fi

else
    echo "Python 3 is not installed."
    echo "Aborting"
fi

