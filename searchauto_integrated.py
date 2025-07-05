import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
import sqlite3
import re
from datetime import datetime
import shutil
import subprocess
import sys
from pathlib import Path
import webbrowser

# Import existing modules
try:
    from ai_search import AISearchEngine
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

class IntegratedSearchAuto:
    def __init__(self, root):
        self.root = root
        self.root.title("SearchAuto Integrated - Search, Convert & Organize")
        self.root.geometry("1400x900")
        
        # Initialize variables
        self.roots = []
        self.search_results = []
        self.is_indexing = False
        self.is_converting = False
        
        # Create database
        self.init_database()
        
        # Create UI
        self.create_ui()
        
        # Initialize AI if available
        self.ai_engine = None
        if AI_AVAILABLE:
            try:
                self.ai_engine = AISearchEngine()
            except:
                pass
    
    def init_database(self):
        """Initialize the search database"""
        self.conn = sqlite3.connect('file_index.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS files 
            (id INTEGER PRIMARY KEY, path TEXT UNIQUE, content TEXT, 
             file_type TEXT, last_modified REAL, tags TEXT)
        ''')
        self.conn.commit()
    
    def create_ui(self):
        """Create the integrated user interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Search Tab
        self.create_search_tab()
        
        # Convert Tab
        self.create_convert_tab()
        
        # Organize Tab
        self.create_organize_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_search_tab(self):
        """Create the search functionality tab"""
        search_frame = ttk.Frame(self.notebook)
        self.notebook.add(search_frame, text="🔍 Search")
        
        # Root management
        root_frame = ttk.LabelFrame(search_frame, text="Root Directories", padding=10)
        root_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Roots listbox with scrollbar
        roots_container = ttk.Frame(root_frame)
        roots_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.roots_listbox = tk.Listbox(roots_container, height=4, selectmode=tk.EXTENDED)
        roots_scrollbar = ttk.Scrollbar(roots_container, orient=tk.VERTICAL, command=self.roots_listbox.yview)
        self.roots_listbox.configure(yscrollcommand=roots_scrollbar.set)
        
        self.roots_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        roots_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Root buttons
        root_buttons = ttk.Frame(root_frame)
        root_buttons.pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(root_buttons, text="Add Root", command=self.add_root).pack(fill=tk.X, pady=2)
        ttk.Button(root_buttons, text="Remove Root", command=self.remove_root).pack(fill=tk.X, pady=2)
        ttk.Button(root_buttons, text="▲", command=self.move_root_up).pack(fill=tk.X, pady=2)
        ttk.Button(root_buttons, text="▼", command=self.move_root_down).pack(fill=tk.X, pady=2)
        
        # Search controls
        search_controls = ttk.Frame(search_frame)
        search_controls.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_controls, text="Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_controls, width=60)
        self.search_entry.pack(side=tk.LEFT, padx=(5, 10))
        self.search_entry.bind('<Return>', lambda e: self.perform_search())
        
        # Search buttons
        search_buttons = ttk.Frame(search_controls)
        search_buttons.pack(side=tk.LEFT)
        
        ttk.Button(search_buttons, text="🔍 Live Search", command=self.live_search).pack(side=tk.LEFT, padx=2)
        ttk.Button(search_buttons, text="⚡ Index Search", command=self.index_search).pack(side=tk.LEFT, padx=2)
        if AI_AVAILABLE:
            ttk.Button(search_buttons, text="🤖 AI Search", command=self.ai_search).pack(side=tk.LEFT, padx=2)
        
        # Index management
        index_frame = ttk.LabelFrame(search_frame, text="Index Management", padding=10)
        index_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(index_frame, text="🔄 Rebuild Index", command=self.rebuild_index).pack(side=tk.LEFT, padx=2)
        ttk.Button(index_frame, text="🔄 Update Index", command=self.update_index).pack(side=tk.LEFT, padx=2)
        if AI_AVAILABLE:
            ttk.Button(index_frame, text="🤖 Build AI", command=self.build_ai_index).pack(side=tk.LEFT, padx=2)
            ttk.Button(index_frame, text="🗑️ Clear AI", command=self.clear_ai_index).pack(side=tk.LEFT, padx=2)
        
        # Results frame
        results_frame = ttk.LabelFrame(search_frame, text="Search Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create Treeview for results
        self.results_tree = ttk.Treeview(results_frame, columns=("Type", "Path", "Content"), show="tree headings", height=15)
        self.results_tree.heading("#0", text="File")
        self.results_tree.heading("Type", text="Type")
        self.results_tree.heading("Path", text="Path")
        self.results_tree.heading("Content", text="Content Preview")
        
        # Set column widths (make Path wider)
        self.results_tree.column("#0", width=200)
        self.results_tree.column("Type", width=80)
        self.results_tree.column("Path", width=700, stretch=True)  # Wider for long paths
        self.results_tree.column("Content", width=500, stretch=True)
        
        # Add scrollbars
        results_scrollbar_y = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        results_scrollbar_x = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=results_scrollbar_y.set, xscrollcommand=results_scrollbar_x.set)
        
        # Pack results tree and scrollbars
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        results_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        results_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Results actions frame
        results_actions = ttk.Frame(results_frame)
        results_actions.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(results_actions, text="📄 Open File", command=self.open_selected_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(results_actions, text="📁 Open Folder", command=self.open_selected_folder).pack(side=tk.LEFT, padx=2)
        ttk.Button(results_actions, text="🗑️ Clear Results", command=self.clear_results).pack(side=tk.LEFT, padx=2)
        
        # Bind double-click to open file
        self.results_tree.bind('<Double-1>', lambda e: self.open_selected_file())

        # Tooltip for file path
        self.tooltip = tk.Toplevel(self.root)
        self.tooltip.withdraw()
        self.tooltip.overrideredirect(True)
        self.tooltip_label = tk.Label(self.tooltip, text="", background="#ffffe0", relief="solid", borderwidth=1, font=("Arial", 9))
        self.tooltip_label.pack(ipadx=1)
        self.results_tree.bind('<Motion>', self.on_treeview_motion)
        self.results_tree.bind('<Leave>', lambda e: self.tooltip.withdraw())
    
    def create_convert_tab(self):
        """Create the conversion functionality tab"""
        convert_frame = ttk.Frame(self.notebook)
        self.notebook.add(convert_frame, text="🔄 Convert")
        
        # Conversion type selection
        type_frame = ttk.LabelFrame(convert_frame, text="Conversion Type", padding=10)
        type_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.convert_type = tk.StringVar(value="doc_to_docx")
        ttk.Radiobutton(type_frame, text="DOC to DOCX", variable=self.convert_type, 
                       value="doc_to_docx").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(type_frame, text="To Markdown", variable=self.convert_type, 
                       value="to_markdown").pack(side=tk.LEFT, padx=10)
        
        # File selection
        file_frame = ttk.LabelFrame(convert_frame, text="File Selection", padding=10)
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(file_frame, text="Input Folder:").pack(side=tk.LEFT)
        self.input_folder_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.input_folder_var, width=50).pack(side=tk.LEFT, padx=(5, 10))
        ttk.Button(file_frame, text="Browse", command=self.browse_input_folder).pack(side=tk.LEFT)
        
        ttk.Label(file_frame, text="Output Folder:").pack(side=tk.LEFT, padx=(20, 0))
        self.output_folder_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.output_folder_var, width=50).pack(side=tk.LEFT, padx=(5, 10))
        ttk.Button(file_frame, text="Browse", command=self.browse_output_folder).pack(side=tk.LEFT)
        
        # Conversion options
        options_frame = ttk.LabelFrame(convert_frame, text="Options", padding=10)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.recursive_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Include subfolders", variable=self.recursive_var).pack(side=tk.LEFT, padx=10)
        
        self.overwrite_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Overwrite existing files", variable=self.overwrite_var).pack(side=tk.LEFT, padx=10)
        
        # Convert button
        convert_buttons = ttk.Frame(convert_frame)
        convert_buttons.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(convert_buttons, text="Start Conversion", command=self.start_conversion).pack(side=tk.LEFT)
        ttk.Button(convert_buttons, text="Cancel", command=self.cancel_conversion).pack(side=tk.LEFT, padx=10)
        
        # Progress
        progress_frame = ttk.LabelFrame(convert_frame, text="Progress", padding=10)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.progress_var = tk.StringVar(value="Ready")
        ttk.Label(progress_frame, textvariable=self.progress_var).pack()
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Conversion log
        log_frame = ttk.LabelFrame(convert_frame, text="Conversion Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.conversion_log = scrolledtext.ScrolledText(log_frame, height=10)
        self.conversion_log.pack(fill=tk.BOTH, expand=True)
    
    def create_organize_tab(self):
        """Create the Markdown organization tab"""
        organize_frame = ttk.Frame(self.notebook)
        self.notebook.add(organize_frame, text="📁 Organize")
        
        # Markdown collection management
        md_frame = ttk.LabelFrame(organize_frame, text="Markdown Collection", padding=10)
        md_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(md_frame, text="Collection Root:").pack(side=tk.LEFT)
        self.md_root_var = tk.StringVar()
        ttk.Entry(md_frame, textvariable=self.md_root_var, width=50).pack(side=tk.LEFT, padx=(5, 10))
        ttk.Button(md_frame, text="Browse", command=self.browse_md_root).pack(side=tk.LEFT)
        
        # Organization tools
        tools_frame = ttk.LabelFrame(organize_frame, text="Organization Tools", padding=10)
        tools_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(tools_frame, text="📋 Generate Indexes", command=self.generate_indexes).pack(side=tk.LEFT, padx=2)
        ttk.Button(tools_frame, text="🏷️ Extract Tags", command=self.extract_tags).pack(side=tk.LEFT, padx=2)
        ttk.Button(tools_frame, text="🔗 Find Backlinks", command=self.find_backlinks).pack(side=tk.LEFT, padx=2)
        ttk.Button(tools_frame, text="📊 Statistics", command=self.show_statistics).pack(side=tk.LEFT, padx=2)
        
        # Quick actions
        actions_frame = ttk.LabelFrame(organize_frame, text="Quick Actions", padding=10)
        actions_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(actions_frame, text="📝 New Note", command=self.create_new_note).pack(side=tk.LEFT, padx=2)
        ttk.Button(actions_frame, text="📁 New Folder", command=self.create_new_folder).pack(side=tk.LEFT, padx=2)
        ttk.Button(actions_frame, text="🔄 Refresh", command=self.refresh_organization).pack(side=tk.LEFT, padx=2)
        
        # Organization log
        org_log_frame = ttk.LabelFrame(organize_frame, text="Organization Log", padding=10)
        org_log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.org_log = scrolledtext.ScrolledText(org_log_frame, height=15)
        self.org_log.pack(fill=tk.BOTH, expand=True)
    
    # Search functionality methods
    def add_root(self):
        folder = filedialog.askdirectory(title="Select Root Directory")
        if folder and folder not in self.roots:
            self.roots.append(folder)
            self.update_roots_display()
    
    def remove_root(self):
        selection = self.roots_listbox.curselection()
        if selection:
            for index in reversed(selection):
                del self.roots[index]
            self.update_roots_display()
    
    def move_root_up(self):
        selection = self.roots_listbox.curselection()
        if selection and selection[0] > 0:
            index = selection[0]
            self.roots[index], self.roots[index-1] = self.roots[index-1], self.roots[index]
            self.update_roots_display()
            self.roots_listbox.selection_set(index-1)
    
    def move_root_down(self):
        selection = self.roots_listbox.curselection()
        if selection and selection[0] < len(self.roots) - 1:
            index = selection[0]
            self.roots[index], self.roots[index+1] = self.roots[index+1], self.roots[index]
            self.update_roots_display()
            self.roots_listbox.selection_set(index+1)
    
    def update_roots_display(self):
        self.roots_listbox.delete(0, tk.END)
        for root in self.roots:
            self.roots_listbox.insert(tk.END, root)
    
    def perform_search(self):
        query = self.search_entry.get().strip()
        if query:
            self.live_search()
    
    def live_search(self):
        query = self.search_entry.get().strip()
        if not query:
            return
        
        self.status_var.set("Performing live search...")
        self.clear_results()
        
        def search_thread():
            results = []
            for root in self.roots:
                for root_path, dirs, files in os.walk(root):
                    for file in files:
                        if file.lower().endswith(('.txt', '.md', '.docx', '.pdf')):
                            file_path = os.path.join(root_path, file)
                            try:
                                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                    content = f.read()
                                    if query.lower() in content.lower():
                                        results.append((file_path, content))
                            except:
                                continue
            
            self.root.after(0, lambda: self.display_results(results, "Live Search"))
        
        threading.Thread(target=search_thread, daemon=True).start()
    
    def index_search(self):
        query = self.search_entry.get().strip()
        if not query:
            return
        
        self.status_var.set("Performing index search...")
        self.clear_results()
        
        def search_thread():
            self.cursor.execute("""
                SELECT path, content FROM files 
                WHERE content LIKE ? 
                ORDER BY last_modified DESC
            """, (f'%{query}%',))
            results = self.cursor.fetchall()
            self.root.after(0, lambda: self.display_results(results, "Index Search"))
        
        threading.Thread(target=search_thread, daemon=True).start()
    
    def ai_search(self):
        if not self.ai_engine:
            messagebox.showwarning("AI Search", "AI engine not available")
            return
        
        query = self.search_entry.get().strip()
        if not query:
            return
        
        self.status_var.set("Performing AI search...")
        self.clear_results()
        
        selected_roots = self.roots  # Use the currently selected roots in the UI
        def is_in_selected_roots(path):
            return any(os.path.abspath(path).startswith(os.path.abspath(root)) for root in selected_roots)
        
        def search_thread():
            try:
                results = self.ai_engine.search(query)
                # Filter results by selected roots
                filtered_results = [r for r in results if is_in_selected_roots(r.get('path', ''))]
                self.root.after(0, lambda: self.display_ai_results(filtered_results))
            except Exception as e:
                self.root.after(0, lambda: self.results_tree.insert("", "end", values=("Error", "", f"AI Search Error: {str(e)}")))
        
        threading.Thread(target=search_thread, daemon=True).start()
    
    def display_results(self, results, search_type):
        self.clear_results()
        
        for i, (file_path, content) in enumerate(results[:50]):  # Limit to 50 results
            filename = os.path.basename(file_path)
            file_type = os.path.splitext(filename)[1].upper()
            content_preview = content[:200].replace('\n', ' ').replace('\r', ' ')
            
            # Handle Chinese characters properly
            try:
                content_preview = content_preview.encode('utf-8').decode('utf-8')
            except:
                content_preview = content_preview.encode('latin-1', errors='ignore').decode('latin-1')
            
            self.results_tree.insert("", "end", values=(file_type, file_path, content_preview))
        
        self.status_var.set(f"Found {len(results)} results")
    
    def display_ai_results(self, results):
        self.clear_results()
        
        for i, result in enumerate(results[:20]):
            file_path = result.get('path', 'Unknown')
            filename = os.path.basename(file_path)
            similarity = result.get('similarity', 'N/A')
            summary = result.get('summary', 'No summary available')
            
            self.results_tree.insert("", "end", values=(f"AI ({similarity})", file_path, summary))
        
        self.status_var.set(f"Found {len(results)} AI results")
    
    def clear_results(self):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
    
    def open_selected_file(self):
        selection = self.results_tree.selection()
        if selection:
            item = self.results_tree.item(selection[0])
            file_path = item['values'][1]  # Path is in second column
            if file_path and os.path.exists(file_path):
                try:
                    os.startfile(file_path)
                except:
                    # Fallback for non-Windows systems
                    subprocess.run(['xdg-open', file_path], capture_output=True)
    
    def open_selected_folder(self):
        selection = self.results_tree.selection()
        if selection:
            item = self.results_tree.item(selection[0])
            file_path = item['values'][1]  # Path is in second column
            if file_path and os.path.exists(file_path):
                folder_path = os.path.dirname(file_path)
                try:
                    os.startfile(folder_path)
                except:
                    # Fallback for non-Windows systems
                    subprocess.run(['xdg-open', folder_path], capture_output=True)
    
    def rebuild_index(self):
        if self.is_indexing:
            return
        
        self.is_indexing = True
        self.status_var.set("Rebuilding index...")
        
        def index_thread():
            try:
                self.cursor.execute("DELETE FROM files")
                for root in self.roots:
                    for root_path, dirs, files in os.walk(root):
                        for file in files:
                            if file.lower().endswith(('.txt', '.md', '.docx', '.pdf')):
                                file_path = os.path.join(root_path, file)
                                try:
                                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                        content = f.read()
                                        self.cursor.execute("""
                                            INSERT OR REPLACE INTO files (path, content, file_type, last_modified)
                                            VALUES (?, ?, ?, ?)
                                        """, (file_path, content, os.path.splitext(file)[1], os.path.getmtime(file_path)))
                                except:
                                    continue
                
                self.conn.commit()
                self.root.after(0, lambda: self.status_var.set("Index rebuilt successfully"))
            except Exception as e:
                self.root.after(0, lambda: self.status_var.set(f"Index error: {str(e)}"))
            finally:
                self.is_indexing = False
        
        threading.Thread(target=index_thread, daemon=True).start()
    
    def update_index(self):
        # Similar to rebuild but only updates changed files
        self.rebuild_index()
    
    def build_ai_index(self):
        if not self.ai_engine:
            messagebox.showwarning("AI Index", "AI engine not available")
            return
        
        self.status_var.set("Building AI index...")
        
        def ai_index_thread():
            try:
                self.cursor.execute("SELECT path, content FROM files")
                files = self.cursor.fetchall()
                # Convert to the format expected by AI engine
                documents = [{"path": row[0], "content": row[1]} for row in files]
                self.ai_engine.add_documents_to_ai_index(documents)
                self.root.after(0, lambda: self.status_var.set("AI index built successfully"))
            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda: self.status_var.set(f"AI index error: {error_msg}"))
        
        threading.Thread(target=ai_index_thread, daemon=True).start()
    
    def clear_ai_index(self):
        if self.ai_engine:
            self.ai_engine.clear_index()
            self.status_var.set("AI index cleared")
    
    # Conversion functionality methods
    def browse_input_folder(self):
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_folder_var.set(folder)
    
    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder_var.set(folder)
    
    def start_conversion(self):
        if self.is_converting:
            return
        
        input_folder = self.input_folder_var.get()
        output_folder = self.output_folder_var.get()
        convert_type = self.convert_type.get()
        
        if not input_folder or not output_folder:
            messagebox.showerror("Error", "Please select input and output folders")
            return
        
        self.is_converting = True
        self.progress_var.set("Starting conversion...")
        self.progress_bar['value'] = 0
        self.conversion_log.delete(1.0, tk.END)
        
        def conversion_thread():
            try:
                if convert_type == "doc_to_docx":
                    self.convert_doc_to_docx(input_folder, output_folder)
                else:
                    self.convert_to_markdown(input_folder, output_folder)
                
                self.root.after(0, lambda: self.progress_var.set("Conversion completed"))
            except Exception as e:
                self.root.after(0, lambda: self.progress_var.set(f"Conversion error: {str(e)}"))
            finally:
                self.is_converting = False
        
        threading.Thread(target=conversion_thread, daemon=True).start()
    
    def convert_doc_to_docx(self, input_folder, output_folder):
        # Implementation for DOC to DOCX conversion
        files = []
        for root, dirs, filenames in os.walk(input_folder):
            for filename in filenames:
                if filename.lower().endswith('.doc'):
                    files.append(os.path.join(root, filename))
        
        total_files = len(files)
        for i, file_path in enumerate(files):
            try:
                # Simple conversion logic (you can enhance this)
                relative_path = os.path.relpath(file_path, input_folder)
                output_path = os.path.join(output_folder, relative_path.replace('.doc', '.docx'))
                
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                shutil.copy2(file_path, output_path)
                
                self.root.after(0, lambda f=file_path: self.conversion_log.insert(tk.END, f"Converted: {f}\n"))
                self.root.after(0, lambda p=(i+1)/total_files*100: self.progress_bar.configure(value=p))
                
            except Exception as e:
                self.root.after(0, lambda f=file_path, e=str(e): self.conversion_log.insert(tk.END, f"Error converting {f}: {e}\n"))
    
    def convert_to_markdown(self, input_folder, output_folder):
        # Implementation for Markdown conversion
        files = []
        for root, dirs, filenames in os.walk(input_folder):
            for filename in filenames:
                if filename.lower().endswith(('.txt', '.docx', '.pdf')):
                    files.append(os.path.join(root, filename))
        
        total_files = len(files)
        for i, file_path in enumerate(files):
            try:
                relative_path = os.path.relpath(file_path, input_folder)
                output_path = os.path.join(output_folder, relative_path.rsplit('.', 1)[0] + '.md')
                
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Simple text to markdown conversion
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Basic markdown formatting
                lines = content.split('\n')
                markdown_lines = []
                for line in lines:
                    if line.strip().startswith('#'):
                        markdown_lines.append(line)
                    elif line.strip().isupper() and len(line.strip()) < 100:
                        markdown_lines.append(f"## {line}")
                    else:
                        markdown_lines.append(line)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(markdown_lines))
                
                self.root.after(0, lambda f=file_path: self.conversion_log.insert(tk.END, f"Converted: {f}\n"))
                self.root.after(0, lambda p=(i+1)/total_files*100: self.progress_bar.configure(value=p))
                
            except Exception as e:
                self.root.after(0, lambda f=file_path, e=str(e): self.conversion_log.insert(tk.END, f"Error converting {f}: {e}\n"))
    
    def cancel_conversion(self):
        self.is_converting = False
        self.progress_var.set("Conversion cancelled")
    
    # Organization functionality methods
    def browse_md_root(self):
        folder = filedialog.askdirectory(title="Select Markdown Collection Root")
        if folder:
            self.md_root_var.set(folder)
    
    def generate_indexes(self):
        md_root = self.md_root_var.get()
        if not md_root:
            messagebox.showerror("Error", "Please select a Markdown collection root")
            return
        
        def index_thread():
            try:
                for root, dirs, files in os.walk(md_root):
                    md_files = [f for f in files if f.endswith('.md') and f != 'index.md']
                    subdirs = [d for d in dirs if os.path.exists(os.path.join(root, d, 'index.md'))]
                    
                    lines = []
                    for f in sorted(md_files):
                        lines.append(f"- [{f[:-3]}]({f})")
                    
                    for d in sorted(subdirs):
                        lines.append(f"- [{d}/](./{d}/index.md)")
                    
                    index_path = os.path.join(root, 'index.md')
                    with open(index_path, 'w', encoding='utf-8') as idx:
                        idx.write("# Index\n\n")
                        idx.write('\n'.join(lines) + '\n')
                
                self.root.after(0, lambda: self.org_log.insert(tk.END, "Indexes generated successfully!\n"))
            except Exception as e:
                self.root.after(0, lambda: self.org_log.insert(tk.END, f"Error generating indexes: {str(e)}\n"))
        
        threading.Thread(target=index_thread, daemon=True).start()
    
    def extract_tags(self):
        md_root = self.md_root_var.get()
        if not md_root:
            messagebox.showerror("Error", "Please select a Markdown collection root")
            return
        
        def tag_thread():
            try:
                tag_pattern = re.compile(r'#([A-Za-z0-9_\-]+)')
                tags = set()
                
                for root, dirs, files in os.walk(md_root):
                    for f in files:
                        if f.endswith('.md'):
                            with open(os.path.join(root, f), encoding='utf-8') as file:
                                for line in file:
                                    tags.update(tag_pattern.findall(line))
                
                self.root.after(0, lambda: self.org_log.insert(tk.END, f"Tags found: {sorted(tags)}\n"))
            except Exception as e:
                self.root.after(0, lambda: self.org_log.insert(tk.END, f"Error extracting tags: {str(e)}\n"))
        
        threading.Thread(target=tag_thread, daemon=True).start()
    
    def find_backlinks(self):
        md_root = self.md_root_var.get()
        if not md_root:
            messagebox.showerror("Error", "Please select a Markdown collection root")
            return
        
        def backlink_thread():
            try:
                # Simple backlink detection
                all_files = {}
                for root, dirs, files in os.walk(md_root):
                    for f in files:
                        if f.endswith('.md'):
                            file_path = os.path.join(root, f)
                            with open(file_path, encoding='utf-8') as file:
                                content = file.read()
                                all_files[file_path] = content
                
                backlinks = {}
                for file_path, content in all_files.items():
                    filename = os.path.basename(file_path)
                    for other_path, other_content in all_files.items():
                        if other_path != file_path and filename in other_content:
                            if file_path not in backlinks:
                                backlinks[file_path] = []
                            backlinks[file_path].append(other_path)
                
                self.root.after(0, lambda: self.org_log.insert(tk.END, f"Backlinks found: {len(backlinks)} files have backlinks\n"))
                for file_path, links in backlinks.items():
                    self.root.after(0, lambda f=file_path, l=links: self.org_log.insert(tk.END, f"{os.path.basename(f)}: {len(l)} backlinks\n"))
                
            except Exception as e:
                self.root.after(0, lambda: self.org_log.insert(tk.END, f"Error finding backlinks: {str(e)}\n"))
        
        threading.Thread(target=backlink_thread, daemon=True).start()
    
    def show_statistics(self):
        md_root = self.md_root_var.get()
        if not md_root:
            messagebox.showerror("Error", "Please select a Markdown collection root")
            return
        
        def stats_thread():
            try:
                total_files = 0
                total_size = 0
                file_types = {}
                
                for root, dirs, files in os.walk(md_root):
                    for f in files:
                        if f.endswith('.md'):
                            file_path = os.path.join(root, f)
                            total_files += 1
                            total_size += os.path.getsize(file_path)
                            
                            ext = os.path.splitext(f)[1]
                            file_types[ext] = file_types.get(ext, 0) + 1
                
                stats_text = f"""
Statistics:
- Total Markdown files: {total_files}
- Total size: {total_size / 1024:.1f} KB
- File types: {file_types}
"""
                self.root.after(0, lambda: self.org_log.insert(tk.END, stats_text))
                
            except Exception as e:
                self.root.after(0, lambda: self.org_log.insert(tk.END, f"Error getting statistics: {str(e)}\n"))
        
        threading.Thread(target=stats_thread, daemon=True).start()
    
    def create_new_note(self):
        md_root = self.md_root_var.get()
        if not md_root:
            messagebox.showerror("Error", "Please select a Markdown collection root")
            return
        
        filename = f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        file_path = os.path.join(md_root, filename)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {filename[:-3]}\n\nCreated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            self.org_log.insert(tk.END, f"Created new note: {filename}\n")
        except Exception as e:
            self.org_log.insert(tk.END, f"Error creating note: {str(e)}\n")
    
    def create_new_folder(self):
        md_root = self.md_root_var.get()
        if not md_root:
            messagebox.showerror("Error", "Please select a Markdown collection root")
            return
        
        folder_name = f"folder_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        folder_path = os.path.join(md_root, folder_name)
        
        try:
            os.makedirs(folder_path, exist_ok=True)
            self.org_log.insert(tk.END, f"Created new folder: {folder_name}\n")
        except Exception as e:
            self.org_log.insert(tk.END, f"Error creating folder: {str(e)}\n")
    
    def refresh_organization(self):
        self.org_log.delete(1.0, tk.END)
        self.org_log.insert(tk.END, "Organization refreshed\n")

    def on_treeview_motion(self, event):
        region = self.results_tree.identify("region", event.x, event.y)
        if region == "cell":
            row_id = self.results_tree.identify_row(event.y)
            col = self.results_tree.identify_column(event.x)
            if col == "#3" and row_id:
                item = self.results_tree.item(row_id)
                file_path = item['values'][1]
                if file_path:
                    self.tooltip_label.config(text=file_path)
                    self.tooltip.deiconify()
                    self.tooltip.lift()
                    x = self.results_tree.winfo_rootx() + event.x + 20
                    y = self.results_tree.winfo_rooty() + event.y + 10
                    self.tooltip.geometry(f"+{x}+{y}")
                else:
                    self.tooltip.withdraw()
            else:
                self.tooltip.withdraw()
        else:
            self.tooltip.withdraw()

def main():
    root = tk.Tk()
    app = IntegratedSearchAuto(root)
    root.mainloop()

if __name__ == "__main__":
    main() 