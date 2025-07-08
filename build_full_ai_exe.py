#!/usr/bin/env python3
"""
Full AI build script for SearchAuto with all AI models included
"""

import os
import sys
import subprocess
import shutil
import re

def remove_emojis_from_line(line):
    # Remove emoji unicode characters and replace with ASCII equivalents if needed
    line = line.replace('\U0001f680', '==>')  # 🚀
    line = line.replace('\U0001f4c1', '[DIR]')  # 📁
    line = line.replace('\U0001f389', '[OK]')  # 🎉
    line = line.replace('\U0001f4cb', '[INFO]')  # 📋
    line = line.replace('\U0001f197', '[OK]')  # 🆗
    line = line.replace('\U0001f6a8', '[WARN]')  # 🚨
    line = line.replace('\U0001f4e6', '[PKG]')  # 📦
    line = line.replace('\U0001f50d', '[CHK]')  # 🔍
    line = line.replace('\U00002705', '[OK]')  # ✅
    line = line.replace('\U0000274c', '[ERR]')  # ❌
    line = line.replace('\U0001f4a1', '[TIP]')  # 💡
    line = line.replace('\U000026a0', '[WARN]')  # ⚠️
    return re.sub(r'[\U00010000-\U0010ffff]', '', line)

def build_full_ai_exe():
    """Build full AI EXE with all models"""
    print("[BUILD] Building SearchAuto EXE (Full AI Version)...")
    
    # Clean previous builds
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # Build with PyInstaller - comprehensive AI version with all dependencies
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=SearchAuto_FullAI",
        "--add-data=README.md;.",
        "--add-data=requirements.txt;.",
        "--add-data=ai_search_db;.",
        # Core AI imports
        "--hidden-import=ai_search",
        "--hidden-import=sentence_transformers",
        "--hidden-import=transformers",
        "--hidden-import=chromadb",
        "--hidden-import=torch",
        "--hidden-import=torch.nn",
        "--hidden-import=torch.nn.functional",
        "--hidden-import=torch.utils.data",
        "--hidden-import=torch.cuda",
        "--hidden-import=torch.version",
        "--hidden-import=huggingface_hub",
        "--hidden-import=numpy",
        "--hidden-import=pandas",
        "--hidden-import=sklearn",
        "--hidden-import=sklearn.feature_extraction",
        "--hidden-import=sklearn.metrics",
        # Tokenizers and processing
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
        # Additional dependencies
        "--hidden-import=openpyxl",
        "--hidden-import=json",
        "--hidden-import=hashlib",
        "--hidden-import=datetime",
        "--hidden-import=pathlib",
        "--hidden-import=shutil",
        "--hidden-import=subprocess",
        "--hidden-import=re",
        "--hidden-import=os",
        "--hidden-import=sys",
        "--hidden-import=time",
        "--hidden-import=threading",
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.filedialog",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=tkinter.ttk",
        # Collect all AI packages
        "--collect-all=sentence_transformers",
        "--collect-all=transformers",
        "--collect-all=chromadb",
        "--collect-all=torch",
        "--collect-all=huggingface_hub",
        "--collect-all=tokenizers",
        "--collect-all=accelerate",
        "--collect-all=safetensors",
        # Exclude unnecessary modules to reduce size
        "--exclude-module=matplotlib",
        "--exclude-module=scipy",
        "--exclude-module=PIL",
        "--exclude-module=cv2",
        "--exclude-module=IPython",
        "--exclude-module=jupyter",
        "searchAuto.py"
    ]
    
    if os.path.exists('icon.ico'):
        cmd.extend(['--icon=icon.ico'])
    
    subprocess.run(cmd, check=True)
    print("[OK] Full AI EXE build completed!")

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
    print("[OK] Created fix_ai_models.bat")

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
    print("[OK] Created test_ai.py")

def create_full_ai_nsis_installer():
    """Create NSIS installer script for SearchAuto Full AI"""
    nsis_script = '''!define APPNAME "SearchAuto Full AI"
!define COMPANYNAME "SearchAuto"
!define DESCRIPTION "SearchAuto Full AI Standalone"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0
!define HELPURL "https://github.com/your-repo/SearchAuto"
!define UPDATEURL "https://github.com/your-repo/SearchAuto"
!define ABOUTURL "https://github.com/your-repo/SearchAuto"
!define INSTALLSIZE 100000

RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\\${COMPANYNAME}\\${APPNAME}"

Name "${APPNAME}"
Icon "icon.ico"
outFile "SearchAuto_FullAI_Setup.exe"

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
    File "dist\\SearchAuto_FullAI.exe"
    File "icon.ico"
    File "requirements.txt"
    File "README.md"
    File "install_full_ai.bat"
    File "fix_ai_models.bat"
    File "test_ai.py"
    
    WriteUninstaller "$INSTDIR\\uninstall.exe"
    
    CreateDirectory "$SMPROGRAMS\\${COMPANYNAME}"
    CreateShortCut "$SMPROGRAMS\\${COMPANYNAME}\\${APPNAME}.lnk" "$INSTDIR\\SearchAuto_FullAI.exe" "" "$INSTDIR\\icon.ico"
    CreateShortCut "$SMPROGRAMS\\${COMPANYNAME}\\Uninstall ${APPNAME}.lnk" "$INSTDIR\\uninstall.exe" "" "$INSTDIR\\icon.ico"
    
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "UninstallString" "$\"$INSTDIR\\uninstall.exe$\""
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "QuietUninstallString" "$\"$INSTDIR\\uninstall.exe$\" /S"
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
    with open('SearchAuto_FullAI_installer.nsi', 'w') as f:
        f.write(nsis_script)
    print("[OK] Created SearchAuto_FullAI_installer.nsi file")

def build_full_ai_nsis_installer():
    """Build the NSIS installer for SearchAuto Full AI if makensis.exe is available"""
    nsis_paths = [
        r"C:\\Program Files\\NSIS\\makensis.exe",
        r"C:\\Program Files (x86)\\NSIS\\makensis.exe"
    ]
    nsis_found = False
    for path in nsis_paths:
        if os.path.exists(path):
            nsis_found = True
            break
    if not nsis_found:
        print("[WARN] NSIS not found. Install NSIS to create installer.")
        print("   Download from: https://nsis.sourceforge.io/Download")
        return
    subprocess.run([path, "SearchAuto_FullAI_installer.nsi"], check=True)
    print("[OK] Windows installer created: SearchAuto_FullAI_Setup.exe")

def main():
    """Main build process"""
    print("==> SearchAuto Full AI Build Process")
    print("=" * 40)
    
    # Build full AI EXE
    build_full_ai_exe()
    
    # Create AI installer
    create_ai_installer()
    
    # Create AI fix script
    create_ai_fix_script()
    
    # Create AI test script
    create_ai_test_script()
    
    # Create NSIS installer script
    create_full_ai_nsis_installer()
    
    # Build NSIS installer if possible
    build_full_ai_nsis_installer()
    
    print("\n[OK] Full AI build completed successfully!")
    print("\n[DIR] Generated files:")
    print("  - dist/SearchAuto_FullAI.exe (Full AI EXE)")
    print("  - install_full_ai.bat (AI installer)")
    print("  - fix_ai_models.bat (AI fix script)")
    print("  - test_ai.py (AI test script)")
    print("  - SearchAuto_FullAI_installer.nsi (NSIS script)")
    print("  - SearchAuto_FullAI_Setup.exe (Windows installer)")
    print("\n[TIP] Troubleshooting:")
    print("  1. If AI search doesn't work in EXE, run fix_ai_models.bat")
    print("  2. Run test_ai.py to diagnose AI component issues")
    print("  3. Make sure you have sufficient disk space for AI models (~2GB)")

if __name__ == "__main__":
    main() 