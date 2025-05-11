# Generate sample audio files for MyraTTS
# This script runs the sample generator from the project root directory

Write-Host "Generating sample audio files for MyraTTS..." -ForegroundColor Cyan

# Check if virtual environment is activated
if (-not ($env:VIRTUAL_ENV -like "*myra_tts*")) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    try {
        if (Test-Path "myra_tts\Scripts\Activate.ps1") {
            & "myra_tts\Scripts\Activate.ps1"
        }
        else {
            Write-Host "Virtual environment not found. Please run 'python scripts\init_project.py' first." -ForegroundColor Red
            exit 1
        }
    }
    catch {
        Write-Host "Failed to activate virtual environment. Please activate it manually." -ForegroundColor Red
        exit 1
    }
}

# Run the sample generator script
Write-Host "Running sample generator..." -ForegroundColor Green
python scripts\generate_samples.py

# Check result
if ($LASTEXITCODE -eq 0) {
    Write-Host "Sample audio files generated successfully!" -ForegroundColor Green
    Write-Host "You can find them in the 'audio\samples' directory." -ForegroundColor Green
}
else {
    Write-Host "Failed to generate sample audio files." -ForegroundColor Red
}
