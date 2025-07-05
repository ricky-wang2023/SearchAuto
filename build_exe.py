#!/usr/bin/env python3
"""
Build script for creating SearchAuto standalone EXE installer
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller installed successfully")

def create_spec_file():
    """Create PyInstaller spec file for SearchAuto"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['searchAuto.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('README.md', '.'),
        ('requirements.txt', '.'),
        ('ai_search.py', '.'),
        ('ai_search_light.py', '.'),
        ('check_threads.py', '.'),
    ],
    hiddenimports=[
        'sentence_transformers',
        'chromadb',
        'torch',
        'transformers',
        'huggingface_hub',
        'tokenizers',
        'numpy',
        'pandas',
        'openpyxl',
        'PyPDF2',
        'pdfminer',
        'docx',
        'sqlite3',
        'tkinter',
        'threading',
        'json',
        'pickle',
        'datetime',
        're',
        'platform',
        'subprocess',
        'time',
        'os',
        'sys',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SearchAuto',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
    
    with open('SearchAuto.spec', 'w') as f:
        f.write(spec_content)
    print("✅ Created SearchAuto.spec file")

def create_installer_script():
    """Create NSIS installer script"""
    nsis_script = '''!define APPNAME "SearchAuto"
!define COMPANYNAME "SearchAuto"
!define DESCRIPTION "Universal File Content Search Tool with AI"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0
!define HELPURL "https://github.com/your-repo/SearchAuto"
!define UPDATEURL "https://github.com/your-repo/SearchAuto"
!define ABOUTURL "https://github.com/your-repo/SearchAuto"
!define INSTALLSIZE 500000

RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\\${COMPANYNAME}\\${APPNAME}"

Name "${APPNAME}"
Icon "icon.ico"
outFile "SearchAuto_Setup.exe"

!include LogicLib.nsh

Page directory
Page instfiles

!macro VerifyUserIsAdmin
UserInfo::GetAccountType
Pop $0
${If} $0 != "admin"
    messageBox mb_iconstop "Administrator rights required!"
    SetErrorLevel 740 ;ERROR_ELEVATION_REQUIRED
    Quit
${EndIf}
!macroend

function .onInit
    SetShellVarContext all
    !insertmacro VerifyUserIsAdmin
functionEnd

section "install"
    SetOutPath $INSTDIR
    File /r "dist\\SearchAuto\\*.*"
    
    WriteUninstaller "$INSTDIR\\uninstall.exe"
    
    CreateDirectory "$SMPROGRAMS\\${COMPANYNAME}"
    CreateShortCut "$SMPROGRAMS\\${COMPANYNAME}\\${APPNAME}.lnk" "$INSTDIR\\SearchAuto.exe" "" "$INSTDIR\\icon.ico"
    CreateShortCut "$SMPROGRAMS\\${COMPANYNAME}\\Uninstall ${APPNAME}.lnk" "$INSTDIR\\uninstall.exe" "" "$INSTDIR\\icon.ico"
    
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "UninstallString" "$\\"$INSTDIR\\uninstall.exe$\\""
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "QuietUninstallString" "$\\"$INSTDIR\\uninstall.exe$\" /S"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "InstallLocation" "$INSTDIR"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "DisplayIcon" "$INSTDIR\\icon.ico"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "Publisher" "${COMPANYNAME}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "HelpLink" "${HELPURL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "URLUpdateInfo" "${UPDATEURL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "URLInfoAbout" "${ABOUTURL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "VersionMajor" ${VERSIONMAJOR}
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "VersionMinor" ${VERSIONMINOR}
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "NoRepair" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "EstimatedSize" ${INSTALLSIZE}
sectionEnd

section "uninstall"
    Delete "$SMPROGRAMS\\${COMPANYNAME}\\${APPNAME}.lnk"
    Delete "$SMPROGRAMS\\${COMPANYNAME}\\Uninstall ${APPNAME}.lnk"
    RMDir "$SMPROGRAMS\\${COMPANYNAME}"
    
    Delete "$INSTDIR\\uninstall.exe"
    RMDir /r "$INSTDIR"
    
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}"
sectionEnd
'''
    
    with open('installer.nsi', 'w') as f:
        f.write(nsis_script)
    print("✅ Created installer.nsi file")

def create_batch_installer():
    """Create simple batch file installer"""
    batch_content = '''@echo off
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

echo.
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
pause
'''
    
    with open('install.bat', 'w') as f:
        f.write(batch_content)
    print("✅ Created install.bat file")

def build_exe():
    """Build the EXE file using PyInstaller"""
    print("🔨 Building SearchAuto EXE...")
    
    # Clean previous builds
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # Build with PyInstaller
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
        "--hidden-import=sentence_transformers",
        "--hidden-import=chromadb",
        "--hidden-import=torch",
        "--hidden-import=transformers",
        "--hidden-import=huggingface_hub",
        "--hidden-import=tokenizers",
        "searchAuto.py"
    ]
    
    if os.path.exists('icon.ico'):
        cmd.extend(['--icon=icon.ico'])
    
    subprocess.run(cmd, check=True)
    print("✅ EXE build completed successfully!")

def create_portable_package():
    """Create portable package with all dependencies"""
    print("📦 Creating portable package...")
    
    # Create portable directory
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
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    call venv\\Scripts\\activate.bat
    pip install -r requirements.txt
) else (
    call venv\\Scripts\\activate.bat
)

echo Starting SearchAuto...
python searchAuto.py
pause
'''
    
    with open(f'{portable_dir}/launch.bat', 'w') as f:
        f.write(launcher_content)
    
    # Create README for portable
    portable_readme = '''# SearchAuto Portable

This is a portable version of SearchAuto that can run on any Windows machine with Python installed.

## Quick Start:
1. Ensure Python 3.7+ is installed
2. Double-click `launch.bat`
3. The app will automatically install dependencies and start

## Manual Start:
1. Open command prompt in this folder
2. Run: `python searchAuto.py`

## Features:
- AI-powered semantic search
- Document summarization
- Multi-file type support (TXT, DOCX, PDF, XLSX)
- No installation required
'''
    
    with open(f'{portable_dir}/README_Portable.txt', 'w') as f:
        f.write(portable_readme)
    
    print(f"✅ Portable package created in {portable_dir}/")

def main():
    """Main build process"""
    print("🚀 SearchAuto Build Process")
    print("=" * 40)
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Create spec file
    create_spec_file()
    
    # Create installer scripts
    create_installer_script()
    create_batch_installer()
    
    # Build EXE
    build_exe()
    
    # Create portable package
    create_portable_package()
    
    print("\n🎉 Build completed successfully!")
    print("\n📁 Generated files:")
    print("  - dist/SearchAuto.exe (Standalone EXE)")
    print("  - SearchAuto_Portable/ (Portable package)")
    print("  - install.bat (Simple installer)")
    print("  - installer.nsi (NSIS installer script)")
    print("\n💡 Next steps:")
    print("  1. Test the EXE: dist/SearchAuto.exe")
    print("  2. Distribute the portable package")
    print("  3. Use install.bat for simple installation")

if __name__ == "__main__":
    main() 