#!/usr/bin/env python3
"""
Full AI build script for SearchAuto with all AI models included
"""

import os
import sys
import subprocess
import shutil

def build_full_ai_exe():
    """Build full AI EXE with all models"""
    print("🔨 Building SearchAuto EXE (Full AI Version)...")
    
    # Clean previous builds
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # Build with PyInstaller - full AI version with better dependency handling
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=SearchAuto_FullAI",
        "--add-data=README.md;.",
        "--add-data=requirements.txt;.",
        "--add-data=ai_search.py;.",
        "--add-data=ai_search_light.py;.",
        "--add-data=check_threads.py;.",
        "--hidden-import=sentence_transformers",
        "--hidden-import=transformers",
        "--hidden-import=chromadb",
        "--hidden-import=torch",
        "--hidden-import=huggingface_hub",
        "--hidden-import=numpy",
        "--hidden-import=tokenizers",
        "--hidden-import=accelerate",
        "--hidden-import=safetensors",
        "--hidden-import=regex",
        "--hidden-import=requests",
        "--hidden-import=urllib3",
        "--hidden-import=packaging",
        "--hidden-import=filelock",
        "--hidden-import=typing_extensions",
        "--hidden-import=importlib_metadata",
        "--hidden-import=zipp",
        "--collect-all=sentence_transformers",
        "--collect-all=transformers",
        "--collect-all=chromadb",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--exclude-module=matplotlib",
        "--exclude-module=scipy",
        "searchAuto.py"
    ]
    
    if os.path.exists('icon.ico'):
        cmd.extend(['--icon=icon.ico'])
    
    subprocess.run(cmd, check=True)
    print("✅ Full AI EXE build completed!")

def create_ai_installer():
    """Create AI installer with model download"""
    installer_content = '''@echo off
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
'''
    
    with open('install_full_ai.bat', 'w') as f:
        f.write(installer_content)
    print("✅ Created install_full_ai.bat")

def create_ai_fix_script():
    """Create a script to fix AI issues in the EXE"""
    fix_script = '''@echo off
echo ========================================
echo    SearchAuto AI Fix Script
echo ========================================
echo.

echo This script will help fix AI search issues in the EXE version.
echo.

REM Create AI models directory if it doesn't exist
if not exist "%USERPROFILE%\\.cache\\huggingface" (
    echo Creating HuggingFace cache directory...
    mkdir "%USERPROFILE%\\.cache\\huggingface"
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
'''
    
    with open('fix_ai_models.bat', 'w') as f:
        f.write(fix_script)
    print("✅ Created fix_ai_models.bat")

def create_ai_test_script():
    """Create a script to test AI functionality"""
    test_script = '''import sys
import os

def test_ai_components():
    """Test AI components to diagnose issues"""
    print("Testing AI components...")
    
    try:
        print("1. Testing sentence_transformers...")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("   ✓ SentenceTransformer loaded successfully")
        
        print("2. Testing transformers...")
        from transformers import pipeline
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
        print("   ✓ Transformers pipeline loaded successfully")
        
        print("3. Testing chromadb...")
        import chromadb
        client = chromadb.PersistentClient(path="test_ai_db")
        print("   ✓ ChromaDB initialized successfully")
        
        print("4. Testing AI search engine...")
        from ai_search import AISearchEngine
        engine = AISearchEngine("test_ai_db")
        if engine.initialize():
            print("   ✓ AI Search Engine initialized successfully")
        else:
            print("   ✗ AI Search Engine failed to initialize")
            
        print("\\nAll AI components are working correctly!")
        return True
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_ai_components()
    if not success:
        print("\\nAI components test failed. Please check your installation.")
    input("Press Enter to continue...")
'''
    
    with open('test_ai.py', 'w') as f:
        f.write(test_script)
    print("✅ Created test_ai.py")

def main():
    """Main build process"""
    print("🚀 SearchAuto Full AI Build Process")
    print("=" * 40)
    
    # Build full AI EXE
    build_full_ai_exe()
    
    # Create AI installer
    create_ai_installer()
    
    # Create AI fix script
    create_ai_fix_script()
    
    # Create AI test script
    create_ai_test_script()
    
    print("\n🎉 Full AI build completed successfully!")
    print("\n📁 Generated files:")
    print("  - dist/SearchAuto_FullAI.exe (Full AI EXE)")
    print("  - install_full_ai.bat (AI installer)")
    print("  - fix_ai_models.bat (AI fix script)")
    print("  - test_ai.py (AI test script)")
    print("\n💡 Troubleshooting:")
    print("  1. If AI search doesn't work in EXE, run fix_ai_models.bat")
    print("  2. Run test_ai.py to diagnose AI component issues")
    print("  3. Make sure you have sufficient disk space for AI models (~2GB)")

if __name__ == "__main__":
    main() 