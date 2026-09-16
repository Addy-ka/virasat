@echo off
cd /d "%~dp0"
title Virasat
echo Starting Virasat...
python -m pip install -r requirements.txt --quiet --disable-pip-version-check
timeout /t 2 >nul
start "" http://localhost:5000
python app.py
pause
