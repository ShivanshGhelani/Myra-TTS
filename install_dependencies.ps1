# MyraTTS - PowerShell Dependency Installer

Write-Host "===================================" -ForegroundColor Cyan
Write-Host "   MyraTTS - Installing Dependencies" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "Found $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to continue..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Check if virtual environment exists, create if not
if (-not (Test-Path "myra_tts")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv myra_tts
}
else {
    Write-Host "Virtual environment found." -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "myra_tts\Scripts\Activate.ps1"

# Install required packages
Write-Host ""
Write-Host "Installing required packages..." -ForegroundColor Yellow
pip install -r requirements.txt

# Try to install ffmpeg using pip
Write-Host ""
Write-Host "Installing ffmpeg-python for audio conversion..." -ForegroundColor Yellow
pip install ffmpeg-python

Write-Host ""
Write-Host "===================================" -ForegroundColor Green
Write-Host "      Installation Complete!" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green
Write-Host ""
Write-Host "To generate sample audio files, run:" -ForegroundColor Cyan
Write-Host ".\scripts\run_generate_samples.ps1" -ForegroundColor White
Write-Host ""

Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
