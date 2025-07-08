#!/usr/bin/env python3
"""
Check what conversion tools are available on the system
"""

import os
import subprocess
import sys

def check_libreoffice():
    """Check if LibreOffice is available"""
    print("🔍 Checking LibreOffice availability...")
    
    libreoffice_paths = [
        "soffice",  # Linux/Mac
        "libreoffice",  # Linux
        r"C:\Program Files\LibreOffice\program\soffice.exe",  # Windows
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",  # Windows 32-bit
        r"C:\Program Files\LibreOffice*\program\soffice.exe",  # Windows with version
        r"C:\Program Files (x86)\LibreOffice*\program\soffice.exe",  # Windows 32-bit with version
    ]
    
    for path in libreoffice_paths:
        try:
            # Handle wildcards in paths
            if '*' in path:
                import glob
                matching_paths = glob.glob(path)
                if matching_paths:
                    path = matching_paths[0]
                    print(f"  ✓ Found LibreOffice: {path}")
                    return True
                continue
            
            # Test if the executable exists
            if os.path.exists(path):
                print(f"  ✓ Found LibreOffice: {path}")
                return True
            elif path in ["soffice", "libreoffice"]:
                # Test if command is available
                try:
                    result = subprocess.run([path, "--version"], 
                                         capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        print(f"  ✓ Found LibreOffice: {path}")
                        return True
                except:
                    continue
        except Exception as e:
            continue
    
    print("  ✗ LibreOffice not found")
    return False

def check_microsoft_word():
    """Check if Microsoft Word is available"""
    print("🔍 Checking Microsoft Word availability...")
    
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        word.Quit()
        print("  ✓ Microsoft Word is available")
        return True
    except Exception as e:
        print(f"  ✗ Microsoft Word not available: {e}")
        return False

def check_python_docx():
    """Check if python-docx is available"""
    print("🔍 Checking python-docx availability...")
    
    try:
        from docx import Document
        print("  ✓ python-docx is available")
        return True
    except ImportError:
        print("  ✗ python-docx not installed")
        return False

def check_pywin32():
    """Check if pywin32 is available"""
    print("🔍 Checking pywin32 availability...")
    
    try:
        import win32com.client
        print("  ✓ pywin32 is available")
        return True
    except ImportError:
        print("  ✗ pywin32 not installed")
        return False

def check_pdf_tools():
    """Check if PDF tools are available"""
    print("🔍 Checking PDF tools availability...")
    
    tools_available = True
    
    try:
        import PyPDF2
        print("  ✓ PyPDF2 is available")
    except ImportError:
        print("  ✗ PyPDF2 not installed")
        tools_available = False
    
    try:
        from pdfminer.high_level import extract_text
        print("  ✓ pdfminer.six is available")
    except ImportError:
        print("  ✗ pdfminer.six not installed")
        tools_available = False
    
    return tools_available

def main():
    """Main function"""
    print("🔧 Conversion Tools Check")
    print("=" * 50)
    
    libreoffice_available = check_libreoffice()
    word_available = check_microsoft_word()
    docx_available = check_python_docx()
    pywin32_available = check_pywin32()
    pdf_tools_available = check_pdf_tools()
    
    print("\n📊 Summary:")
    print("=" * 50)
    
    if libreoffice_available:
        print("✅ LibreOffice - Best option for DOC to DOCX conversion")
    else:
        print("❌ LibreOffice - Install for best DOC conversion results")
    
    if word_available:
        print("✅ Microsoft Word - Available for DOC to DOCX conversion")
    else:
        print("❌ Microsoft Word - Not available")
    
    if docx_available:
        print("✅ python-docx - Available for DOCX processing")
    else:
        print("❌ python-docx - Not installed")
    
    if pywin32_available:
        print("✅ pywin32 - Available for Windows COM automation")
    else:
        print("❌ pywin32 - Not installed")
    
    if pdf_tools_available:
        print("✅ PDF tools - Available for PDF processing")
    else:
        print("❌ PDF tools - Not fully installed")
    
    print("\n💡 Recommendations:")
    if not libreoffice_available:
        print("- Install LibreOffice for best DOC to DOCX conversion")
        print("  Download from: https://www.libreoffice.org/")
    
    if not docx_available:
        print("- Install python-docx: pip install python-docx")
    
    if not pywin32_available:
        print("- Install pywin32: pip install pywin32")
    
    if not pdf_tools_available:
        print("- Install PDF tools: pip install PyPDF2 pdfminer.six")

if __name__ == "__main__":
    main() 