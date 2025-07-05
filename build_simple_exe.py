#!/usr/bin/env python3
"""
Simple build script for SearchAuto EXE without AI models
"""

import os
import sys
import subprocess
import shutil

def build_simple_exe():
    """Build a simple EXE without AI models"""
    print("🔨 Building SearchAuto EXE (Simple Version)...")
    
    # Clean previous builds
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # Build with PyInstaller - simpler version
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=SearchAuto",
        "--add-data=README.md;.",
        "--add-data=requirements.txt;.",
        "--add-data=ai_search.py;.",
        "--add-data=ai_search_light.py;.",
        "--add-data=check_threads.py;.",
        "--exclude-module=torch",
        "--exclude-module=sentence_transformers",
        "--exclude-module=transformers",
        "--exclude-module=chromadb",
        "--exclude-module=huggingface_hub",
        "searchAuto.py"
    ]
    
    if os.path.exists('icon.ico'):
        cmd.extend(['--icon=icon.ico'])
    
    subprocess.run(cmd, check=True)
    print("✅ Simple EXE build completed!")

def create_portable_package():
    """Create portable package"""
    print("📦 Creating portable package...")
    
    portable_dir = "SearchAuto_Portable"
    if os.path.exists(portable_dir):
        shutil.rmtree(portable_dir)
    os.makedirs(portable_dir)
    
    # Copy files
    files_to_copy = [
        'searchAuto.py',
        'ai_search.py',
        'ai_search_light.py',
        'check_threads.py',
        'README.md',
        'requirements.txt'
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, portable_dir)
    
    # Create launcher script
    launcher_content = '''@echo off
echo ========================================
echo    SearchAuto Portable
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

REM Install dependencies if needed
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting SearchAuto...
python searchAuto.py
pause
'''
    
    with open(f'{portable_dir}/launch.bat', 'w') as f:
        f.write(launcher_content)
    
    print(f"✅ Portable package created in {portable_dir}/")

def create_installer():
    """Create simple installer"""
    installer_content = '''@echo off
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
echo @echo off > "%USERPROFILE%\\Desktop\\SearchAuto.bat"
echo cd /d "%~dp0" >> "%USERPROFILE%\\Desktop\\SearchAuto.bat"
echo python searchAuto.py >> "%USERPROFILE%\\Desktop\\SearchAuto.bat"
echo pause >> "%USERPROFILE%\\Desktop\\SearchAuto.bat"

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
'''
    
    with open('install.bat', 'w') as f:
        f.write(installer_content)
    print("✅ Created install.bat")

def main():
    """Main build process"""
    print("🚀 SearchAuto Simple Build Process")
    print("=" * 40)
    
    # Build simple EXE
    build_simple_exe()
    
    # Create portable package
    create_portable_package()
    
    # Create installer
    create_installer()
    
    print("\n🎉 Simple build completed successfully!")
    print("\n📁 Generated files:")
    print("  - dist/SearchAuto.exe (Standalone EXE)")
    print("  - SearchAuto_Portable/ (Portable package)")
    print("  - install.bat (Simple installer)")
    print("\n💡 Note: AI models will download on first use")
    print("   This reduces EXE size and avoids build issues")

if __name__ == "__main__":
    main() 