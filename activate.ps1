# Activate environment and prepare for running scripts

function Invoke-MyraTTSCommand {
    param (
        [Parameter(Mandatory=$true)]
        [string]$ScriptName,
        
        [Parameter(ValueFromRemainingArguments=$true)]
        $ScriptArgs
    )
    
    $projectRoot = $PSScriptRoot
    $scriptPath = Join-Path -Path $projectRoot -ChildPath "scripts\$ScriptName.py"
    
    if (-not (Test-Path $scriptPath)) {
        Write-Host "Error: Script '$ScriptName.py' not found in scripts directory." -ForegroundColor Red
        return
    }
    
    # Activate virtual environment if not active
    if (-not ($env:VIRTUAL_ENV -like "*myra_tts*")) {
        $activateScript = Join-Path -Path $projectRoot -ChildPath "myra_tts\Scripts\Activate.ps1"
        if (Test-Path $activateScript) {
            Write-Host "Activating virtual environment..." -ForegroundColor Yellow
            & $activateScript
        }
        else {
            Write-Host "Virtual environment not found. Please run 'python scripts\init_project.py' first." -ForegroundColor Red
            return
        }
    }
    
    # Set working directory to project root
    Set-Location -Path $projectRoot
    
    # Run the script
    Write-Host "Running $ScriptName.py..." -ForegroundColor Cyan
    $argString = if ($ScriptArgs) { $ScriptArgs -join ' ' } else { "" }
    Invoke-Expression "python `"$scriptPath`" $argString"
}

# If script is sourced (dot-sourced), export function
if ($MyInvocation.InvocationName -eq '.') {
    Write-Host "MyraTTS development environment activated." -ForegroundColor Green
    Write-Host "You can run scripts with: Invoke-MyraTTSCommand <script-name> [arguments]" -ForegroundColor Cyan
    Write-Host "Available scripts:"
    Get-ChildItem -Path (Join-Path -Path $PSScriptRoot -ChildPath "scripts") -Filter "*.py" | ForEach-Object {
        Write-Host ("  - " + $_.BaseName) -ForegroundColor Green
    }
}
else {
    Write-Host "This script should be dot-sourced to use its functions." -ForegroundColor Yellow
    Write-Host "Example: . .\activate.ps1" -ForegroundColor Yellow
}
