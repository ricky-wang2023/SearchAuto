#!/usr/bin/env python3
"""
Command-line Markdown Converter
Usage: python markdown_converter_cli.py <input_folder> <output_folder> [file_types]
Example: python markdown_converter_cli.py C:\Documents C:\Markdown docx,pdf,txt
"""

import os
import sys
import re
from docx import Document
import PyPDF2
from pdfminer.high_level import extract_text as pdfminer_extract_text

def convert_docx_to_markdown(docx_path, md_path):
    """Convert DOCX file to Markdown"""
    try:
        doc = Document(docx_path)
        markdown_content = []
        
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if not text:
                markdown_content.append("")
                continue
                
            # Check for headings
            style_name = paragraph.style.name if paragraph.style and paragraph.style.name else ""
            if style_name.startswith('Heading'):
                level_str = style_name[-1] if style_name[-1].isdigit() else "1"
                level = int(level_str) if level_str.isdigit() else 1
                markdown_content.append(f"{'#' * level} {text}")
            else:
                # Check for bold and italic
                formatted_text = text
                for run in paragraph.runs:
                    if run.bold and run.italic:
                        formatted_text = formatted_text.replace(run.text, f"***{run.text}***")
                    elif run.bold:
                        formatted_text = formatted_text.replace(run.text, f"**{run.text}**")
                    elif run.italic:
                        formatted_text = formatted_text.replace(run.text, f"*{run.text}*")
                
                markdown_content.append(formatted_text)
                
        # Write markdown file
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown_content))
            
        return True
        
    except Exception as e:
        print(f"Error converting DOCX {docx_path}: {e}")
        return False
        
def convert_pdf_to_markdown(pdf_path, md_path):
    """Convert PDF file to Markdown"""
    try:
        # Try pdfminer first (better for text extraction)
        try:
            text = pdfminer_extract_text(pdf_path)
        except:
            # Fallback to PyPDF2
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                    
        # Clean and format text
        lines = text.split('\n')
        markdown_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Simple heading detection (lines in caps or with numbers)
            if line.isupper() and len(line) < 100:
                markdown_content.append(f"## {line}")
            elif re.match(r'^[0-9]+\.', line):
                markdown_content.append(f"### {line}")
            else:
                markdown_content.append(line)
                
        # Write markdown file
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown_content))
            
        return True
        
    except Exception as e:
        print(f"Error converting PDF {pdf_path}: {e}")
        return False
        
def convert_txt_to_markdown(txt_path, md_path):
    """Convert TXT file to Markdown"""
    try:
        with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Clean and format text
        lines = content.split('\n')
        markdown_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Simple heading detection
            if line.isupper() and len(line) < 100:
                markdown_content.append(f"## {line}")
            elif re.match(r'^[0-9]+\.', line):
                markdown_content.append(f"### {line}")
            else:
                markdown_content.append(line)
                
        # Write markdown file
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown_content))
            
        return True
        
    except Exception as e:
        print(f"Error converting TXT {txt_path}: {e}")
        return False

def convert_file_to_markdown(file_path, md_path):
    """Convert a single file to Markdown based on its type"""
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.docx':
        return convert_docx_to_markdown(file_path, md_path)
    elif file_ext == '.pdf':
        return convert_pdf_to_markdown(file_path, md_path)
    elif file_ext == '.txt':
        return convert_txt_to_markdown(file_path, md_path)
    else:
        print(f"Unsupported file type: {file_ext}")
        return False

def main():
    """Main function"""
    if len(sys.argv) < 3:
        print("Usage: python markdown_converter_cli.py <input_folder> <output_folder> [file_types]")
        print("Example: python markdown_converter_cli.py C:\\Documents C:\\Markdown docx,pdf,txt")
        print("Supported file types: docx, pdf, txt")
        sys.exit(1)
        
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    file_types = sys.argv[3].split(',') if len(sys.argv) > 3 else ['docx', 'pdf', 'txt']
    
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        sys.exit(1)
        
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
        except Exception as e:
            print(f"Error: Cannot create output folder '{output_folder}': {e}")
            sys.exit(1)
            
    # Find all files to convert
    files = []
    for root, dirs, filenames in os.walk(input_folder):
        for file in filenames:
            if any(file.lower().endswith(f'.{ft}') for ft in file_types):
                files.append(os.path.join(root, file))
                
    if not files:
        print("No files found to convert.")
        sys.exit(0)
        
    print(f"Found {len(files)} files to convert...")
    
    # Convert files
    successful = 0
    failed = 0
    
    for i, file_path in enumerate(files, 1):
        print(f"[{i}/{len(files)}] Converting: {os.path.basename(file_path)}")
        
        # Create output path
        rel_path = os.path.relpath(file_path, input_folder)
        md_file = os.path.join(output_folder, 
                             os.path.splitext(rel_path)[0] + ".md")
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(md_file), exist_ok=True)
        
        # Convert file
        if convert_file_to_markdown(file_path, md_file):
            print(f"  ✓ Success: {os.path.basename(md_file)}")
            successful += 1
        else:
            print(f"  ✗ Failed: {os.path.basename(file_path)}")
            failed += 1
            
    print(f"\nConversion complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Output folder: {output_folder}")

if __name__ == "__main__":
    main() 