@echo off
echo ========================================
echo    SearchAuto Installer
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

echo Installing SearchAuto...
echo.

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Create desktop shortcut
echo Creating desktop shortcut...
echo @echo off > "%USERPROFILE%\Desktop\SearchAuto.bat"
echo cd /d "%~dp0" >> "%USERPROFILE%\Desktop\SearchAuto.bat"
echo python searchAuto.py >> "%USERPROFILE%\Desktop\SearchAuto.bat"
echo pause >> "%USERPROFILE%\Desktop\SearchAuto.bat"

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo SearchAuto has been installed successfully.
echo You can now run it by:
echo 1. Double-clicking SearchAuto.bat on your desktop
echo 2. Running: python searchAuto.py
echo.
echo Note: AI features will download models on first use.
echo.
pause
