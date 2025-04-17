
@echo off
setlocal

cd /d "%~dp0"


title PSO2 Log Handler


call ".\.venv\Scripts\activate.bat"

python ".\PSO2LogHandler\PSO2LogHandler.py"
