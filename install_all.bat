@echo off
echo ========================================
echo SearchAuto - Complete Installation
echo ========================================
echo.

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Available tools:
echo 1. Main Search Tool: run_search.bat
echo 2. Unified Converter: run_converter.bat
echo 3. Individual Converters:
echo    - python doc_to_docx_converter.py
echo    - python markdown_converter.py
echo.
echo Optional: Install LibreOffice for better DOC to DOCX conversion
echo Download from: https://www.libreoffice.org/
echo.
pause 