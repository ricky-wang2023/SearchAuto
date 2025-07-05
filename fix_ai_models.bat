@echo off
echo ========================================
echo    SearchAuto AI Fix Script
echo ========================================
echo.

echo This script will help fix AI search issues in the EXE version.
echo.

REM Create AI models directory if it doesn't exist
if not exist "%USERPROFILE%\.cache\huggingface" (
    echo Creating HuggingFace cache directory...
    mkdir "%USERPROFILE%\.cache\huggingface"
)

REM Download AI models
echo Downloading AI models...
python -c "from sentence_transformers import SentenceTransformer; print('Downloading SentenceTransformer model...'); SentenceTransformer('all-MiniLM-L6-v2')"
python -c "from transformers import pipeline; print('Downloading summarization model...'); pipeline('summarization', model='facebook/bart-large-cnn')"

echo.
echo ========================================
echo    AI Fix Complete!
echo ========================================
echo.
echo AI models have been downloaded.
echo Try running the SearchAuto EXE again.
echo.
pause
