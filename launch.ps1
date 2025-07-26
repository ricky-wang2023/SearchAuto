# PowerShell launcher for Translate to Markdown GUI
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Translate to Markdown GUI Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to create virtual environment!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "Virtual environment created successfully!" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import docx, PyPDF2, openai, googletrans, deepl" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Dependencies missing"
    }
    Write-Host "All dependencies are available!" -ForegroundColor Green
} catch {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    python -m pip install --upgrade pip
    python -m pip install python-docx PyPDF2 openai googletrans==4.0.0-rc1 deepl
    python -m pip install httpx==0.13.3 httpcore==0.9.1
}

# Run the application
Write-Host "Starting GUI..." -ForegroundColor Green
python translate_to_md_gui.py

# Keep window open if there was an error
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Application exited with an error." -ForegroundColor Red
    Read-Host "Press Enter to exit"
} 