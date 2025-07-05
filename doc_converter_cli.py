#!/usr/bin/env python3
"""
Command-line DOC to DOCX Converter
Usage: python doc_converter_cli.py <input_folder> <output_folder>
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def convert_doc_to_docx(doc_path, docx_path):
    """Convert a single DOC file to DOCX"""
    try:
        # Normalize paths and handle encoding issues
        doc_path = os.path.abspath(doc_path)
        docx_path = os.path.abspath(docx_path)
        
        # Check if source file exists
        if not os.path.exists(doc_path):
            print(f"Source file not found: {doc_path}")
            return False
            
        # Create output directory if needed
        os.makedirs(os.path.dirname(docx_path), exist_ok=True)
        
        # Method 1: Try using LibreOffice (if available)
        if try_libreoffice_conversion(doc_path, docx_path):
            return True
            
        # Method 2: Try using Microsoft Word (if available)
        if try_word_conversion(doc_path, docx_path):
            return True
            
        # Method 3: Try using python-docx (limited success with old DOC files)
        if try_python_docx_conversion(doc_path, docx_path):
            return True
            
        # Method 4: Try to copy if it's already a DOCX in disguise
        if try_copy_if_docx(doc_path, docx_path):
            return True
            
        return False
        
    except Exception as e:
        print(f"Error converting {doc_path}: {e}")
        return False
        
def try_libreoffice_conversion(doc_path, docx_path):
    """Try conversion using LibreOffice"""
    try:
        # Check if LibreOffice is available
        libreoffice_paths = [
            "soffice",  # Linux/Mac
            "libreoffice",  # Linux
            r"C:\Program Files\LibreOffice\program\soffice.exe",  # Windows
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"  # Windows 32-bit
        ]
        
        for path in libreoffice_paths:
            try:
                cmd = [path, "--headless", "--convert-to", "docx", 
                       "--outdir", os.path.dirname(docx_path), doc_path]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    # LibreOffice creates the file with a different name
                    expected_name = os.path.splitext(os.path.basename(doc_path))[0] + ".docx"
                    expected_path = os.path.join(os.path.dirname(docx_path), expected_name)
                    
                    if os.path.exists(expected_path):
                        if expected_path != docx_path:
                            shutil.move(expected_path, docx_path)
                        return True
            except:
                continue
                
        return False
        
    except Exception as e:
        print(f"LibreOffice conversion failed: {e}")
        return False
        
def try_word_conversion(doc_path, docx_path):
    """Try conversion using Microsoft Word (Windows only)"""
    try:
        import win32com.client
        
        # Convert path to absolute path and fix slashes
        abs_doc_path = os.path.abspath(doc_path).replace('/', '\\')
        abs_docx_path = os.path.abspath(docx_path).replace('/', '\\')
        
        # Check if file exists
        if not os.path.exists(abs_doc_path):
            print(f"File not found: {abs_doc_path}")
            return False
        
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        
        try:
            doc = word.Documents.Open(abs_doc_path)
            doc.SaveAs2(abs_docx_path, FileFormat=16)  # 16 = docx format
            doc.Close()
            return True
        except Exception as e:
            print(f"Word document operation failed: {e}")
            return False
        finally:
            word.Quit()
        
    except Exception as e:
        print(f"Word conversion failed: {e}")
        return False
        
def try_python_docx_conversion(doc_path, docx_path):
    """Try conversion using python-docx (limited success)"""
    try:
        from docx import Document
        
        # Check if file exists and is readable
        if not os.path.exists(doc_path):
            print(f"File not found: {doc_path}")
            return False
            
        # Try to read the file first
        try:
            with open(doc_path, 'rb') as f:
                # Check if it's actually a DOCX file in disguise
                content = f.read(4)
                if content == b'PK\x03\x04':
                    # It's actually a DOCX file, just copy it
                    shutil.copy2(doc_path, docx_path)
                    return True
        except Exception as e:
            print(f"Cannot read file {doc_path}: {e}")
            return False
        
        # This method has limited success with old DOC files
        # It works better with newer DOC files that are actually DOCX in disguise
        doc = Document(doc_path)
        doc.save(docx_path)
        return True
        
    except Exception as e:
        print(f"python-docx conversion failed: {e}")
        return False

def try_copy_if_docx(doc_path, docx_path):
    """Check if file is actually a DOCX file in disguise and copy it"""
    try:
        with open(doc_path, 'rb') as f:
            # Check for ZIP file signature (DOCX files are ZIP archives)
            content = f.read(4)
            if content == b'PK\x03\x04':
                print(f"File {os.path.basename(doc_path)} is actually a DOCX file, copying...")
                shutil.copy2(doc_path, docx_path)
                return True
        return False
    except Exception as e:
        print(f"Error checking file format: {e}")
        return False

def main():
    """Main function"""
    if len(sys.argv) != 3:
        print("Usage: python doc_converter_cli.py <input_folder> <output_folder>")
        print("Example: python doc_converter_cli.py C:\\Documents C:\\Converted")
        sys.exit(1)
        
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        sys.exit(1)
        
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
        except Exception as e:
            print(f"Error: Cannot create output folder '{output_folder}': {e}")
            sys.exit(1)
            
    # Find all DOC files
    doc_files = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith('.doc'):
                doc_files.append(os.path.join(root, file))
                
    if not doc_files:
        print("No DOC files found in the input folder.")
        sys.exit(0)
        
    print(f"Found {len(doc_files)} DOC files to convert...")
    
    # Convert files
    successful = 0
    failed = 0
    
    for i, doc_file in enumerate(doc_files, 1):
        print(f"[{i}/{len(doc_files)}] Converting: {os.path.basename(doc_file)}")
        
        # Create output path
        rel_path = os.path.relpath(doc_file, input_folder)
        docx_file = os.path.join(output_folder, 
                               os.path.splitext(rel_path)[0] + ".docx")
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(docx_file), exist_ok=True)
        
        # Convert file
        if convert_doc_to_docx(doc_file, docx_file):
            print(f"  ✓ Success: {os.path.basename(docx_file)}")
            successful += 1
        else:
            print(f"  ✗ Failed: {os.path.basename(doc_file)}")
            failed += 1
            
    print(f"\nConversion complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Output folder: {output_folder}")

if __name__ == "__main__":
    main() 