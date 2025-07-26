# PowerShell script to run Translate to Markdown GUI in virtual environment

Write-Host "Starting Translate to Markdown GUI in virtual environment..." -ForegroundColor Green

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Run the translate script
python translate_to_md_gui.py

# Keep window open if there's an error
if ($LASTEXITCODE -ne 0) {
    Write-Host "Script exited with error code $LASTEXITCODE" -ForegroundColor Red
    Read-Host "Press Enter to continue"
} 