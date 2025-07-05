#!/usr/bin/env python3
"""
Enhanced Markdown Converter Tool
Converts DOCX, PDF, and TXT files to Markdown format
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from pathlib import Path
import re
import html
from docx import Document
import PyPDF2
from pdfminer.high_level import extract_text as pdfminer_extract_text

class MarkdownConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📝 Markdown Converter")
        self.root.geometry("800x600")
        self.root.configure(bg="#f5f5f5")
        self.root.resizable(True, True)
        
        # Variables
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.conversion_progress = tk.DoubleVar()
        self.status_text = tk.StringVar(value="Ready to convert")
        self.file_types = tk.StringVar(value="docx,pdf,txt")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="📝 Markdown Converter", 
                             font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#2196F3")
        title_label.pack(pady=(0, 20))
        
        # File types selection
        types_frame = tk.LabelFrame(main_frame, text="📄 File Types to Convert", 
                                  font=("Arial", 11, "bold"), bg="#f5f5f5", fg="navy")
        types_frame.pack(fill="x", pady=10)
        
        types_inner = tk.Frame(types_frame, bg="#f5f5f5")
        types_inner.pack(fill="x", padx=10, pady=10)
        
        # Checkboxes for file types
        self.docx_var = tk.BooleanVar(value=True)
        self.pdf_var = tk.BooleanVar(value=True)
        self.txt_var = tk.BooleanVar(value=True)
        
        tk.Checkbutton(types_inner, text="DOCX files", variable=self.docx_var, 
                      bg="#f5f5f5", font=("Arial", 10)).pack(side="left", padx=10)
        tk.Checkbutton(types_inner, text="PDF files", variable=self.pdf_var, 
                      bg="#f5f5f5", font=("Arial", 10)).pack(side="left", padx=10)
        tk.Checkbutton(types_inner, text="TXT files", variable=self.txt_var, 
                      bg="#f5f5f5", font=("Arial", 10)).pack(side="left", padx=10)
        
        # Input folder selection
        input_frame = tk.LabelFrame(main_frame, text="📁 Input Folder", 
                                  font=("Arial", 11, "bold"), bg="#f5f5f5", fg="navy")
        input_frame.pack(fill="x", pady=10)
        
        input_inner = tk.Frame(input_frame, bg="#f5f5f5")
        input_inner.pack(fill="x", padx=10, pady=10)
        
        tk.Entry(input_inner, textvariable=self.input_folder, width=60, font=("Arial", 10)).pack(side="left", padx=(0, 10), fill="x", expand=True)
        tk.Button(input_inner, text="Browse", command=self.browse_input_folder, 
                 bg="#2196F3", fg="white", font=("Arial", 9, "bold")).pack(side="right")
        
        # Output folder selection
        output_frame = tk.LabelFrame(main_frame, text="📁 Output Folder (Markdown files)", 
                                   font=("Arial", 11, "bold"), bg="#f5f5f5", fg="navy")
        output_frame.pack(fill="x", pady=10)
        
        output_inner = tk.Frame(output_frame, bg="#f5f5f5")
        output_inner.pack(fill="x", padx=10, pady=10)
        
        tk.Entry(output_inner, textvariable=self.output_folder, width=60, font=("Arial", 10)).pack(side="left", padx=(0, 10), fill="x", expand=True)
        tk.Button(output_inner, text="Browse", command=self.browse_output_folder, 
                 bg="#2196F3", fg="white", font=("Arial", 9, "bold")).pack(side="right")
        
        # Progress frame
        progress_frame = tk.LabelFrame(main_frame, text="🔄 Conversion Progress", 
                                     font=("Arial", 11, "bold"), bg="#f5f5f5", fg="navy")
        progress_frame.pack(fill="x", pady=10)
        
        progress_inner = tk.Frame(progress_frame, bg="#f5f5f5")
        progress_inner.pack(fill="x", padx=10, pady=10)
        
        self.progress_bar = ttk.Progressbar(progress_inner, variable=self.conversion_progress, 
                                           maximum=100, length=500)
        self.progress_bar.pack(fill="x", pady=5)
        
        tk.Label(progress_inner, textvariable=self.status_text, font=("Arial", 9), 
                bg="#f5f5f5").pack()
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg="#f5f5f5")
        buttons_frame.pack(fill="x", pady=(20, 0), side="bottom")
        
        button_sub_frame = tk.Frame(buttons_frame, bg="#f5f5f5")
        button_sub_frame.pack(expand=True)
        
        tk.Button(button_sub_frame, text="🔄 Convert Files", command=self.start_conversion, 
                 bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), 
                 relief="flat", bd=0, height=2, width=15).pack(side="left", padx=5)
        
        tk.Button(button_sub_frame, text="📊 Scan Files", command=self.scan_files, 
                 bg="#FF9800", fg="white", font=("Arial", 12, "bold"), 
                 relief="flat", bd=0, height=2, width=15).pack(side="left", padx=5)
        
        tk.Button(button_sub_frame, text="❌ Exit", command=self.root.quit, 
                 bg="#f44336", fg="white", font=("Arial", 12, "bold"), 
                 relief="flat", bd=0, height=2, width=15).pack(side="right", padx=5)
        
    def browse_input_folder(self):
        """Browse for input folder"""
        folder = filedialog.askdirectory(title="Select folder containing files to convert")
        if folder:
            self.input_folder.set(folder)
            
    def browse_output_folder(self):
        """Browse for output folder"""
        folder = filedialog.askdirectory(title="Select folder for Markdown files")
        if folder:
            self.output_folder.set(folder)
            
    def get_selected_file_types(self):
        """Get list of selected file types"""
        types = []
        if self.docx_var.get():
            types.append('.docx')
        if self.pdf_var.get():
            types.append('.pdf')
        if self.txt_var.get():
            types.append('.txt')
        return types
            
    def scan_files(self):
        """Scan for files in the input folder"""
        input_path = self.input_folder.get()
        if not input_path:
            messagebox.showwarning("Warning", "Please select an input folder first.")
            return
            
        if not os.path.exists(input_path):
            messagebox.showerror("Error", "Input folder does not exist.")
            return
            
        selected_types = self.get_selected_file_types()
        if not selected_types:
            messagebox.showwarning("Warning", "Please select at least one file type.")
            return
            
        files = []
        for root, dirs, filenames in os.walk(input_path):
            for file in filenames:
                if any(file.lower().endswith(ext) for ext in selected_types):
                    files.append(os.path.join(root, file))
                    
        if files:
            messagebox.showinfo("Scan Results", f"Found {len(files)} files to convert:\n\n" + 
                              "\n".join([os.path.basename(f) for f in files[:10]]) + 
                              ("\n..." if len(files) > 10 else ""))
        else:
            messagebox.showinfo("Scan Results", "No files found in the selected folder.")
            
    def convert_docx_to_markdown(self, docx_path, md_path):
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
            
    def convert_pdf_to_markdown(self, pdf_path, md_path):
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
            
    def convert_txt_to_markdown(self, txt_path, md_path):
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
            
    def convert_file_to_markdown(self, file_path, md_path):
        """Convert a single file to Markdown based on its type"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.docx':
            return self.convert_docx_to_markdown(file_path, md_path)
        elif file_ext == '.pdf':
            return self.convert_pdf_to_markdown(file_path, md_path)
        elif file_ext == '.txt':
            return self.convert_txt_to_markdown(file_path, md_path)
        else:
            print(f"Unsupported file type: {file_ext}")
            return False
            
    def start_conversion(self):
        """Start the conversion process"""
        input_path = self.input_folder.get()
        output_path = self.output_folder.get()
        
        if not input_path or not output_path:
            messagebox.showwarning("Warning", "Please select both input and output folders.")
            return
            
        if not os.path.exists(input_path):
            messagebox.showerror("Error", "Input folder does not exist.")
            return
            
        if not os.path.exists(output_path):
            try:
                os.makedirs(output_path)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot create output folder: {e}")
                return
                
        # Start conversion in a separate thread
        thread = threading.Thread(target=self.convert_files)
        thread.daemon = True
        thread.start()
        
    def convert_files(self):
        """Convert all files in the input folder"""
        input_path = self.input_folder.get()
        output_path = self.output_folder.get()
        selected_types = self.get_selected_file_types()
        
        # Find all files to convert
        files = []
        for root, dirs, filenames in os.walk(input_path):
            for file in filenames:
                if any(file.lower().endswith(ext) for ext in selected_types):
                    files.append(os.path.join(root, file))
                    
        if not files:
            self.root.after(0, lambda: messagebox.showinfo("Info", "No files found to convert."))
            return
            
        # Update status
        self.root.after(0, lambda: self.status_text.set(f"Found {len(files)} files to convert..."))
        
        # Convert files
        successful = 0
        failed = 0
        
        for i, file_path in enumerate(files):
            # Update progress
            progress = (i / len(files)) * 100
            self.root.after(0, lambda p=progress: self.conversion_progress.set(p))
            self.root.after(0, lambda f=os.path.basename(file_path): 
                           self.status_text.set(f"Converting: {f}"))
            
            # Create output path
            rel_path = os.path.relpath(file_path, input_path)
            md_file = os.path.join(output_path, 
                                 os.path.splitext(rel_path)[0] + ".md")
            
            # Create output directory if needed
            os.makedirs(os.path.dirname(md_file), exist_ok=True)
            
            # Convert file
            if self.convert_file_to_markdown(file_path, md_file):
                successful += 1
            else:
                failed += 1
                
        # Update final status
        self.root.after(0, lambda: self.conversion_progress.set(100))
        self.root.after(0, lambda: self.status_text.set(
            f"Conversion complete! Success: {successful}, Failed: {failed}"))
        
        # Show results
        self.root.after(0, lambda: messagebox.showinfo("Conversion Complete", 
            f"Conversion completed!\n\nSuccessful: {successful}\nFailed: {failed}\n\n"
            f"Output folder: {output_path}"))
        
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Main function"""
    print("📝 Starting Markdown Converter...")
    converter = MarkdownConverter()
    converter.run()

if __name__ == "__main__":
    main() 