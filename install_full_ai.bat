@echo off
echo ========================================
echo    SearchAuto Full AI Installer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Installing SearchAuto with Full AI...
echo.

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Download AI models
echo Downloading AI models (this may take a while)...
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
python -c "from transformers import pipeline; pipeline('summarization', model='facebook/bart-large-cnn')"

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo SearchAuto Full AI has been installed successfully.
echo AI models have been downloaded and are ready to use.
echo.
pause
