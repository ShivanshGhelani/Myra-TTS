@echo off
REM Run generate_samples.py from the project root directory
cd %~dp0\..
python scripts\generate_samples.py
pause
