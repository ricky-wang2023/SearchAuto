#!/usr/bin/env python3
"""
Test script for portable translation app
"""

import os
import sys
import json

def test_portable_setup():
    """Test if the portable setup is correct"""
    
    print("Testing Portable Translation App Setup...")
    print("=" * 50)
    
    # Check required files
    required_files = [
        "translate_to_md_gui.py",
        "requirements.txt",
        "launch.bat",
        "launch.ps1",
        "QUICK_START.md"
    ]
    
    docs_files = [
        "docs/README.md",
        "docs/API_KEYS_SETUP.md",
        "docs/TRANSLATION_HISTORY.md",
        "docs/FILE_CONFLICT_RESOLUTION.md"
    ]
    
    print("Checking required files...")
    all_files_ok = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            all_files_ok = False
    
    print("\nChecking documentation files...")
    for file in docs_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            all_files_ok = False
    
    # Check Python version
    print(f"\nPython version: {sys.version}")
    if sys.version_info >= (3, 7):
        print("✓ Python version is compatible (3.7+)")
    else:
        print("✗ Python version too old (need 3.7+)")
        all_files_ok = False
    
    # Test requirements.txt
    print("\nChecking requirements.txt...")
    if os.path.exists("requirements.txt"):
        try:
            with open("requirements.txt", "r") as f:
                requirements = f.read()
            if "python-docx" in requirements and "googletrans" in requirements:
                print("✓ requirements.txt contains required packages")
            else:
                print("✗ requirements.txt missing required packages")
                all_files_ok = False
        except Exception as e:
            print(f"✗ Error reading requirements.txt: {e}")
            all_files_ok = False
    else:
        print("✗ requirements.txt not found")
        all_files_ok = False
    
    # Test main script
    print("\nChecking main script...")
    if os.path.exists("translate_to_md_gui.py"):
        try:
            with open("translate_to_md_gui.py", "r", encoding="utf-8") as f:
                content = f.read()
            if "class TranslateApp" in content and "def __init__" in content:
                print("✓ Main script appears to be valid")
            else:
                print("✗ Main script appears to be corrupted")
                all_files_ok = False
        except Exception as e:
            print(f"✗ Error reading main script: {e}")
            all_files_ok = False
    else:
        print("✗ Main script not found")
        all_files_ok = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_files_ok:
        print("🎉 PORTABLE SETUP IS READY!")
        print("\nTo run the app:")
        print("1. Double-click launch.bat (Windows)")
        print("2. Or right-click launch.ps1 → Run with PowerShell")
        print("\nThe launcher will:")
        print("- Create virtual environment")
        print("- Install dependencies")
        print("- Start the GUI")
    else:
        print("❌ PORTABLE SETUP HAS ISSUES!")
        print("Please check the missing files above.")
    
    return all_files_ok

if __name__ == "__main__":
    test_portable_setup() 