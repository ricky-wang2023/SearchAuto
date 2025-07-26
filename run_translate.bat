@echo off
echo Starting Translate to Markdown GUI in virtual environment...

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the translate script
python translate_to_md_gui.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Script exited with error code %errorlevel%
    pause
) 