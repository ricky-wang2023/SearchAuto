#!/usr/bin/env python3
"""
DOC to DOCX Converter Tool
Converts .doc files to .docx format
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from pathlib import Path
import subprocess
import shutil

class DocToDocxConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📄 DOC to DOCX Converter")
        self.root.geometry("700x500")
        self.root.configure(bg="#f5f5f5")
        self.root.resizable(True, True)  # Allow window resizing
        
        # Variables
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.conversion_progress = tk.DoubleVar()
        self.status_text = tk.StringVar(value="Ready to convert")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame with scroll capability
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="📄 DOC to DOCX Converter", 
                             font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#2196F3")
        title_label.pack(pady=(0, 20))
        
        # Input folder selection
        input_frame = tk.LabelFrame(main_frame, text="📁 Input Folder (DOC files)", 
                                  font=("Arial", 11, "bold"), bg="#f5f5f5", fg="navy")
        input_frame.pack(fill="x", pady=10)
        
        input_inner = tk.Frame(input_frame, bg="#f5f5f5")
        input_inner.pack(fill="x", padx=10, pady=10)
        
        tk.Entry(input_inner, textvariable=self.input_folder, width=60, font=("Arial", 10)).pack(side="left", padx=(0, 10), fill="x", expand=True)
        tk.Button(input_inner, text="Browse", command=self.browse_input_folder, 
                 bg="#2196F3", fg="white", font=("Arial", 9, "bold")).pack(side="right")
        
        # Output folder selection
        output_frame = tk.LabelFrame(main_frame, text="📁 Output Folder (DOCX files)", 
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
        
        # Buttons frame - ensure it's at the bottom
        buttons_frame = tk.Frame(main_frame, bg="#f5f5f5")
        buttons_frame.pack(fill="x", pady=(20, 0), side="bottom")
        
        # Create a sub-frame for better button layout
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
        folder = filedialog.askdirectory(title="Select folder containing DOC files")
        if folder:
            self.input_folder.set(folder)
            
    def browse_output_folder(self):
        """Browse for output folder"""
        folder = filedialog.askdirectory(title="Select folder for DOCX files")
        if folder:
            self.output_folder.set(folder)
            
    def scan_files(self):
        """Scan for DOC files in the input folder"""
        input_path = self.input_folder.get()
        if not input_path:
            messagebox.showwarning("Warning", "Please select an input folder first.")
            return
            
        if not os.path.exists(input_path):
            messagebox.showerror("Error", "Input folder does not exist.")
            return
            
        doc_files = []
        for root, dirs, files in os.walk(input_path):
            for file in files:
                if file.lower().endswith('.doc'):
                    doc_files.append(os.path.join(root, file))
                    
        if doc_files:
            messagebox.showinfo("Scan Results", f"Found {len(doc_files)} DOC files:\n\n" + 
                              "\n".join([os.path.basename(f) for f in doc_files[:10]]) + 
                              ("\n..." if len(doc_files) > 10 else ""))
        else:
            messagebox.showinfo("Scan Results", "No DOC files found in the selected folder.")
            
    def convert_doc_to_docx(self, doc_path, docx_path):
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
            if self.try_libreoffice_conversion(doc_path, docx_path):
                return True
                
            # Method 2: Try using Microsoft Word (if available)
            if self.try_word_conversion(doc_path, docx_path):
                return True
                
            # Method 3: Try using python-docx (limited success with old DOC files)
            if self.try_python_docx_conversion(doc_path, docx_path):
                return True
                
            # Method 4: Try to copy if it's already a DOCX in disguise
            if self.try_copy_if_docx(doc_path, docx_path):
                return True
                
            return False
            
        except Exception as e:
            print(f"Error converting {doc_path}: {e}")
            return False
            
    def try_libreoffice_conversion(self, doc_path, docx_path):
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
            
    def try_word_conversion(self, doc_path, docx_path):
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
            
    def try_python_docx_conversion(self, doc_path, docx_path):
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
            
    def try_copy_if_docx(self, doc_path, docx_path):
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
        """Convert all DOC files in the input folder"""
        input_path = self.input_folder.get()
        output_path = self.output_folder.get()
        
        # Find all DOC files
        doc_files = []
        for root, dirs, files in os.walk(input_path):
            for file in files:
                if file.lower().endswith('.doc'):
                    doc_files.append(os.path.join(root, file))
                    
        if not doc_files:
            self.root.after(0, lambda: messagebox.showinfo("Info", "No DOC files found in the input folder."))
            return
            
        # Update status
        self.root.after(0, lambda: self.status_text.set(f"Found {len(doc_files)} DOC files to convert..."))
        
        # Convert files
        successful = 0
        failed = 0
        
        for i, doc_file in enumerate(doc_files):
            # Update progress
            progress = (i / len(doc_files)) * 100
            self.root.after(0, lambda p=progress: self.conversion_progress.set(p))
            self.root.after(0, lambda f=os.path.basename(doc_file): 
                           self.status_text.set(f"Converting: {f}"))
            
            # Create output path
            rel_path = os.path.relpath(doc_file, input_path)
            docx_file = os.path.join(output_path, 
                                   os.path.splitext(rel_path)[0] + ".docx")
            
            # Create output directory if needed
            os.makedirs(os.path.dirname(docx_file), exist_ok=True)
            
            # Convert file
            if self.convert_doc_to_docx(doc_file, docx_file):
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
    print("📄 Starting DOC to DOCX Converter...")
    converter = DocToDocxConverter()
    converter.run()

if __name__ == "__main__":
    main() 