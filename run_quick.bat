@echo off
echo Starting Translate to Markdown GUI (Quick Mode)...
python -c "import docx, PyPDF2, openai, googletrans, deepl; print('✓ All packages available')" 2>nul
if %errorlevel% equ 0 (
    echo Starting GUI...
    python translate_to_md_gui.py
) else (
    echo Running with environment check...
    python translate_to_md_gui.py
)
pause 