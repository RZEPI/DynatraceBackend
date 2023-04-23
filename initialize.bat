@echo off

py -m venv venv

call venv\Scripts\activate.bat

call venv\Scripts\pip3.exe install -r requirements.txt

python app.py