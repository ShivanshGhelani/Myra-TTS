@echo off
echo ===================================
echo MyraTTS - Installing Dependencies
echo ===================================
echo.

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists, create if not
if not exist myra_tts\ (
    echo Creating virtual environment...
    python -m venv myra_tts
) else (
    echo Virtual environment found.
)

REM Activate virtual environment
call myra_tts\Scripts\activate.bat

REM Install required packages
echo.
echo Installing required packages...
pip install -r requirements.txt

REM Try to install ffmpeg using pip
echo.
echo Installing ffmpeg-python for audio conversion...
pip install ffmpeg-python

echo.
echo ==================================
echo Installation Complete!
echo ==================================
echo.
echo To generate sample audio files, run:
echo scripts\run_generate_samples.bat
echo.
pause
