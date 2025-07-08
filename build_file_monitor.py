#!/usr/bin/env python3
"""
Build script for File Monitor standalone executable
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

def create_file_monitor_spec():
    """Create PyInstaller spec file for File Monitor"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['file_monitor.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('file_monitor_config.json', '.'),
        ('README_file_monitor.md', '.'),
    ],
    hiddenimports=[
        'docx',
        'PyPDF2',
        'pdfminer',
        'pdfminer.high_level',
        'win32com.client',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.ttk',
        'threading',
        'json',
        'hashlib',
        'datetime',
        'pathlib',
        'shutil',
        'subprocess',
        're',
        'os',
        'sys',
        'time',
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
    name='FileMonitor',
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
    
    with open('FileMonitor.spec', 'w') as f:
        f.write(spec_content)
    print("✅ Created FileMonitor.spec file")

def create_file_monitor_installer():
    """Create NSIS installer script for File Monitor"""
    nsis_script = '''!define APPNAME "File Monitor"
!define COMPANYNAME "SearchAuto"
!define DESCRIPTION "File Monitor and Auto-Converter"
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
outFile "FileMonitor_Setup.exe"

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
    File /r "dist\\FileMonitor\\*.*"
    
    WriteUninstaller "$INSTDIR\\uninstall.exe"
    
    CreateDirectory "$SMPROGRAMS\\${COMPANYNAME}"
    CreateShortCut "$SMPROGRAMS\\${COMPANYNAME}\\${APPNAME}.lnk" "$INSTDIR\\FileMonitor.exe" "" "$INSTDIR\\icon.ico"
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
    
    with open('FileMonitor_installer.nsi', 'w') as f:
        f.write(nsis_script)
    print("✅ Created FileMonitor_installer.nsi file")

def build_file_monitor_exe():
    """Build File Monitor EXE"""
    print("🔨 Building File Monitor EXE...")
    
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
        "--name=FileMonitor",
        "--add-data=file_monitor_config.json;.",
        "--add-data=README_file_monitor.md;.",
        "--hidden-import=docx",
        "--hidden-import=PyPDF2",
        "--hidden-import=pdfminer",
        "--hidden-import=pdfminer.high_level",
        "--hidden-import=win32com.client",
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.filedialog",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=threading",
        "--hidden-import=json",
        "--hidden-import=hashlib",
        "--hidden-import=datetime",
        "--hidden-import=pathlib",
        "--hidden-import=shutil",
        "--hidden-import=subprocess",
        "--hidden-import=re",
        "file_monitor.py"
    ]
    
    if os.path.exists('icon.ico'):
        cmd.extend(['--icon=icon.ico'])
    
    subprocess.run(cmd, check=True)
    print("✅ File Monitor EXE build completed!")

def create_portable_package():
    """Create portable package"""
    print("📦 Creating portable package...")
    
    # Create portable directory
    portable_dir = "FileMonitor_Portable"
    if os.path.exists(portable_dir):
        shutil.rmtree(portable_dir)
    os.makedirs(portable_dir)
    
    # Copy executable
    if os.path.exists("dist/FileMonitor.exe"):
        shutil.copy2("dist/FileMonitor.exe", portable_dir)
    
    # Copy configuration files
    if os.path.exists("file_monitor_config.json"):
        shutil.copy2("file_monitor_config.json", portable_dir)
    
    if os.path.exists("README_file_monitor.md"):
        shutil.copy2("README_file_monitor.md", portable_dir)
    
    # Create batch file for easy running
    batch_content = '''@echo off
echo ========================================
echo    File Monitor Portable
echo ========================================
echo.
echo Starting File Monitor...
FileMonitor.exe
pause
'''
    
    with open(os.path.join(portable_dir, "run_file_monitor.bat"), 'w') as f:
        f.write(batch_content)
    
    print("✅ Portable package created in FileMonitor_Portable/")

def create_installer():
    """Create Windows installer"""
    print("🔧 Creating Windows installer...")
    
    # Check if NSIS is available
    nsis_paths = [
        r"C:\Program Files\NSIS\makensis.exe",
        r"C:\Program Files (x86)\NSIS\makensis.exe"
    ]
    
    nsis_found = False
    for path in nsis_paths:
        if os.path.exists(path):
            nsis_found = True
            break
    
    if not nsis_found:
        print("⚠️  NSIS not found. Install NSIS to create installer.")
        print("   Download from: https://nsis.sourceforge.io/Download")
        return
    
    # Create installer
    subprocess.run([path, "FileMonitor_installer.nsi"], check=True)
    print("✅ Windows installer created!")

def main():
    """Main build process"""
    print("🚀 File Monitor Build Process")
    print("=" * 50)
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Create spec file
    create_file_monitor_spec()
    
    # Build executable
    build_file_monitor_exe()
    
    # Create portable package
    create_portable_package()
    
    # Create installer
    create_installer()
    
    print("\n🎉 Build completed successfully!")
    print("\n📁 Output files:")
    print("   - dist/FileMonitor.exe (Standalone executable)")
    print("   - FileMonitor_Portable/ (Portable package)")
    print("   - FileMonitor_Setup.exe (Windows installer)")
    print("\n🚀 Ready to distribute!")

if __name__ == "__main__":
    main() 