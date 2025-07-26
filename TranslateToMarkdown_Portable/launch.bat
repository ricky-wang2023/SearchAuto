@echo off
title Translate to Markdown - Portable Launcher
color 0A

echo ========================================
echo   Translate to Markdown - Portable
echo ========================================
echo.

REM Check for Python
where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo.
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment.
    pause
    exit /b 1
)
echo ✓ Virtual environment activated
echo.

REM Install/upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo ✓ Pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Fix googletrans compatibility
echo Fixing googletrans compatibility...
python -m pip install httpx==0.13.3 httpcore==0.9.1
echo ✓ Compatibility fixes applied
echo.

echo ========================================
echo   Starting Translate to Markdown GUI
echo ========================================
echo.

REM Run the application
python translate_to_md_gui.py

echo.
echo Application closed.
pause 