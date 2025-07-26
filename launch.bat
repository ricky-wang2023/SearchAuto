@echo off
echo ========================================
echo   Translate to Markdown GUI Launcher
echo ========================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import docx, PyPDF2, openai, googletrans, deepl" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    python -m pip install --upgrade pip
    python -m pip install python-docx PyPDF2 openai googletrans==4.0.0-rc1 deepl
    python -m pip install httpx==0.13.3 httpcore==0.9.1
)

REM Run the application
echo Starting GUI...
python translate_to_md_gui.py

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
) 