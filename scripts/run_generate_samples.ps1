# Run generate_samples.py from the project root directory
$scriptPath = $MyInvocation.MyCommand.Path
$scriptDir = Split-Path -Parent $scriptPath
$projectRoot = Join-Path $scriptDir ".."

# Navigate to project root
Set-Location -Path $projectRoot

# Run the script
python scripts\generate_samples.py

# Wait for user input before closing
Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
