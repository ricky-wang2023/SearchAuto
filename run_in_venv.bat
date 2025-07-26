@echo off
echo Starting Translate to Markdown GUI in Virtual Environment...

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the script
python translate_to_md_gui.py

REM Keep window open
pause 