@echo off
IF EXIST ./venv (
call ./venv/Scripts/activate.bat
pip install -r requirements.txt
python start.py
) ELSE (
python -m venv ./venv
call ./venv/Scripts/activate.bat
pip install -r requirements.txt
python start.py
)


