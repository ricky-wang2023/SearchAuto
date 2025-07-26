# PowerShell script to run Translate to Markdown GUI in Virtual Environment
Write-Host "Starting Translate to Markdown GUI in Virtual Environment..." -ForegroundColor Green

# Activate virtual environment
& "venv\Scripts\Activate.ps1"

# Run the script
python translate_to_md_gui.py

# Keep window open
Read-Host "Press Enter to exit" 