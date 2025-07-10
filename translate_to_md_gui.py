#!/usr/bin/env python3
"""
Translate to Markdown GUI Application
Environment-aware script with dependency validation
"""

import sys
import os
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("ERROR: Python 3.7 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✓ Python version: {sys.version.split()[0]}")

def check_virtual_environment():
    """Check if running in a virtual environment"""
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if not in_venv:
        print("⚠️  WARNING: Not running in a virtual environment.")
        print("   Consider using: python -m venv venv && venv\\Scripts\\activate")
    else:
        print("✓ Running in virtual environment")
    return in_venv

def install_missing_dependencies():
    """Install missing dependencies"""
    required_packages = {
        'python-docx': 'docx',
        'PyPDF2': 'PyPDF2',
        'openai': 'openai',
        'googletrans': 'googletrans',
        'deepl': 'deepl'
    }
    
    missing_packages = []
    installed_packages = []
    
    for package_name, import_name in required_packages.items():
        try:
            if import_name == 'docx':
                import docx
            elif import_name == 'PyPDF2':
                import PyPDF2
            elif import_name == 'openai':
                import openai
            elif import_name == 'googletrans':
                import googletrans
            elif import_name == 'deepl':
                import deepl
            print(f"✓ {package_name} is installed")
            installed_packages.append(package_name)
        except ImportError:
            missing_packages.append(package_name)
            print(f"✗ {package_name} is missing")
    
    if missing_packages:
        print(f"\nInstalling missing packages: {', '.join(missing_packages)}")
        try:
            for package in missing_packages:
                if package == 'googletrans':
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'googletrans==4.0.0-rc1'])
                else:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✓ Installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to install packages: {e}")
            sys.exit(1)
    else:
        print("✓ All required packages are installed")

# --- PATCH for googletrans/httpx on Python 3.13+ (cgi module removed) ---
import types
if sys.version_info >= (3, 13):
    sys.modules['cgi'] = types.ModuleType('cgi')
    setattr(sys.modules['cgi'], 'parse_header', lambda x: (x, {}))
# ------------------------------------------------------------------------

# Environment validation
if __name__ == '__main__':
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        print("⚠️  WARNING: Not running in a virtual environment.")
        print("   Attempting to activate virtual environment...")
        
        # Try to activate virtual environment
        venv_script = os.path.join("venv", "Scripts", "activate")
        if os.path.exists(venv_script):
            print("✓ Found virtual environment, activating...")
            try:
                # This is a simplified activation - in practice, you'd need to run the script in a subprocess
                # For now, we'll just warn the user
                print("   Please run: venv\\Scripts\\activate && python translate_to_md_gui.py")
                print("   Or use: run_in_venv.bat")
                input("Press Enter to continue anyway...")
            except:
                pass
        else:
            print("   Virtual environment not found. Creating one...")
            try:
                import subprocess
                subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
                print("✓ Virtual environment created!")
                print("   Please run: venv\\Scripts\\activate && python translate_to_md_gui.py")
                print("   Or use: run_in_venv.bat")
                input("Press Enter to continue anyway...")
            except Exception as e:
                print(f"   Failed to create virtual environment: {e}")
                input("Press Enter to continue anyway...")
    else:
        print("✓ Running in virtual environment")
    
    # Quick check if we can skip environment validation
    all_available = True
    missing_packages = []
    
    try:
        import docx
        print("✓ python-docx available")
    except ImportError:
        all_available = False
        missing_packages.append("python-docx")
    
    try:
        import PyPDF2
        print("✓ PyPDF2 available")
    except ImportError:
        all_available = False
        missing_packages.append("PyPDF2")
    
    try:
        import openai
        print("✓ openai available")
    except ImportError:
        all_available = False
        missing_packages.append("openai")
    
    try:
        import googletrans
        print("✓ googletrans available")
    except ImportError:
        all_available = False
        missing_packages.append("googletrans")
    
    try:
        import deepl
        print("✓ deepl available")
    except ImportError:
        all_available = False
        missing_packages.append("deepl")
    
    if all_available:
        print("=== Translate to Markdown GUI ===")
        print("✓ All dependencies are available")
        print("=== Starting GUI ===\n")
    else:
        print("=== Translate to Markdown GUI - Environment Check ===")
        print(f"Missing packages: {', '.join(missing_packages)}")
        check_python_version()
        check_virtual_environment()
        install_missing_dependencies()
        print("=== Environment check complete ===\n")

import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from docx import Document
import PyPDF2
import logging
import json
import time

LOG_FILE = 'translate_to_md_debug.log'
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

# Conditional imports to avoid startup errors
GoogleTranslator = None
openai = None
deepl = None

try:
    from googletrans import Translator as GoogleTranslator
except (ImportError, AttributeError):
    # Handle the httpcore compatibility issue
    try:
        import httpcore
        if not hasattr(httpcore, 'SyncHTTPTransport'):
            # Try to patch httpcore for compatibility
            import types
            if not hasattr(httpcore, 'SyncHTTPTransport'):
                setattr(httpcore, 'SyncHTTPTransport', type('SyncHTTPTransport', (), {}))
        from googletrans import Translator as GoogleTranslator
    except:
        pass
try:
    import openai
except ImportError:
    pass
try:
    import deepl
except ImportError:
    pass

SUPPORTED_EXTS = ['.docx', '.txt', '.pdf', '.md']
API_KEYS_FILE = 'api_keys.json'
HISTORY_FILE = 'translation_history.json'
SETTINGS_FILE = 'app_settings.json'

def load_api_keys():
    """Load API keys from JSON file"""
    try:
        with open(API_KEYS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Create default file if it doesn't exist
        default_keys = {"deepl": "", "openai": ""}
        save_api_keys(default_keys)
        return default_keys

def save_api_keys(keys):
    """Save API keys to JSON file"""
    try:
        with open(API_KEYS_FILE, 'w') as f:
            json.dump(keys, f, indent=4)
    except Exception as e:
        logging.error(f'Failed to save API keys: {e}')

def load_app_settings():
    """Load application settings from JSON file"""
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Create default settings if file doesn't exist
        default_settings = {
            "input_folder": "",
            "output_folder": "",
            "engine": "google",
            "src_lang": "Chinese (zh-cn) [zh-cn]",
            "tgt_lang": "English (en) [en]",
            "skip_translated": True,
            "conflict_mode": "Auto Rename"
        }
        save_app_settings(default_settings)
        return default_settings

def save_app_settings(settings):
    """Save application settings to JSON file"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        logging.error(f'Failed to save app settings: {e}')

def load_translation_history():
    """Load translation history from JSON file"""
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
            # Validate history structure
            if not isinstance(history, dict):
                raise ValueError("Invalid history format")
            if "translated_files" not in history:
                history["translated_files"] = {}
            if "last_translation_date" not in history:
                history["last_translation_date"] = None
            if "total_files_translated" not in history:
                history["total_files_translated"] = 0
            return history
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        logging.warning(f'Failed to load translation history: {e}')
        # Try to load from backup
        backup_file = HISTORY_FILE + '.backup'
        if Path(backup_file).exists():
            try:
                with open(backup_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    logging.info('Loaded history from backup file')
                    return history
            except:
                pass
        
        # Create default history if it doesn't exist or is corrupted
        default_history = {
            "translated_files": {},
            "last_translation_date": None,
            "total_files_translated": 0
        }
        save_translation_history(default_history)
        logging.info('Created new default history file')
        return default_history

def save_translation_history(history):
    """Save translation history to JSON file"""
    try:
        # Create backup of existing file if it exists
        if Path(HISTORY_FILE).exists():
            backup_file = HISTORY_FILE + '.backup'
            try:
                import shutil
                shutil.copy2(HISTORY_FILE, backup_file)
            except Exception as e:
                logging.warning(f'Failed to create backup: {e}')
        
        # Write to temporary file first
        temp_file = HISTORY_FILE + '.tmp'
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
        
        # Move temp file to final location
        import shutil
        shutil.move(temp_file, HISTORY_FILE)
        
        logging.info(f'Successfully saved translation history with {len(history["translated_files"])} files')
            
    except Exception as e:
        logging.error(f'Failed to save translation history: {e}')
        # Try to restore from backup if available
        backup_file = HISTORY_FILE + '.backup'
        if Path(backup_file).exists():
            try:
                import shutil
                shutil.copy2(backup_file, HISTORY_FILE)
                logging.info('Restored history from backup')
            except Exception as restore_e:
                logging.error(f'Failed to restore from backup: {restore_e}')

def get_file_hash(file_path):
    """Get file hash for change detection"""
    try:
        stat = Path(file_path).stat()
        return f"{stat.st_mtime}_{stat.st_size}"
    except:
        return None

def is_file_already_translated(file_path, output_path, history):
    """Check if file has already been translated and output exists"""
    file_hash = get_file_hash(file_path)
    if not file_hash:
        return False
    
    # Convert file_path to string for comparison
    file_path_str = str(file_path)
    
    # Check if file is in history and output exists
    if file_path_str in history["translated_files"]:
        recorded_hash = history["translated_files"][file_path_str]["hash"]
        if recorded_hash == file_hash and Path(output_path).exists():
            return True
    
    return False

def update_translation_history(file_path, output_path, engine, history):
    """Update translation history with new file"""
    file_hash = get_file_hash(file_path)
    if file_hash:
        # Convert paths to strings to avoid JSON serialization issues
        file_path_str = str(file_path)
        output_path_str = str(output_path)
        
        history["translated_files"][file_path_str] = {
            "hash": file_hash,
            "output_path": output_path_str,
            "engine": engine,
            "translated_date": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        history["last_translation_date"] = time.strftime("%Y-%m-%d %H:%M:%S")
        history["total_files_translated"] += 1
        
        save_translation_history(history)
        logging.info(f'Updated translation history for {file_path_str}')
    else:
        logging.warning(f'Could not get file hash for {file_path}')

# Extraction functions

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def extract_text_from_pdf(file_path):
    text = []
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text.append(page.extract_text() or "")
    return '\n'.join(text)

def extract_text_from_md(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def translate_google(text, src='zh-cn', dest='en'):
    if not GoogleTranslator:
        raise ImportError("googletrans is not installed. Run: pip install googletrans==4.0.0-rc1")
    translator = GoogleTranslator()
    maxlen = 4500
    lines = text.split('\n')
    out = []
    buf = ''
    for line in lines:
        if len(buf) + len(line) < maxlen:
            buf += line + '\n'
        else:
            out.append(translator.translate(buf, src=src, dest=dest).text)
            buf = line + '\n'
    if buf:
        out.append(translator.translate(buf, src=src, dest=dest).text)
    return '\n'.join(out)

def translate_deepl(text, api_key, src='ZH', dest='EN-US'):
    if not deepl:
        raise ImportError("deepl is not installed. Run: pip install deepl")
    translator = deepl.Translator(api_key)
    result = translator.translate_text(text, source_lang=src, target_lang=dest)
    # DeepL may return a list or a single object depending on input
    if isinstance(result, list):
        return '\n'.join([r.text for r in result])
    return result.text

def translate_openai(text, api_key, model="gpt-3.5-turbo", src='zh-cn', dest='en'):
    if not openai:
        raise ImportError("openai is not installed. Run: pip install openai")
    openai.api_key = api_key
    prompt = f"Translate the following Chinese text to English, preserving formatting as Markdown.\n\n{text}"
    # Try both openai.ChatCompletion.create and openai.chat.completions.create for compatibility
    try:
        # For openai>=1.0.0
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            temperature=0.3,
        )
        content = getattr(response.choices[0].message, 'content', None)
        if content is not None:
            return content.strip()
        else:
            return "[OpenAI API error: No content in response]"
    except AttributeError:
        try:
            # For openai<1.0.0
            ChatCompletion = getattr(openai, 'ChatCompletion', None)
            if ChatCompletion is None:
                return '[OpenAI API error: ChatCompletion not found. Please check your openai package version.]'
            response = ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2048,
                temperature=0.3,
            )
            content = response.choices[0].message.get('content') if hasattr(response.choices[0], 'message') else None
            if content is not None:
                return content.strip()
            else:
                return "[OpenAI API error: No content in response]"
        except (Exception, ImportError) as e:
            return f"[OpenAI API error: {e}]\nIf you see this error, please check your openai package version."

def save_as_md(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

def get_files_in_folder(folder):
    files = []
    for ext in SUPPORTED_EXTS:
        files.extend(Path(folder).rglob(f'*{ext}'))
    return files

def get_unique_output_path(output_path):
    """Generate unique output path to avoid overwriting existing files"""
    if not Path(output_path).exists():
        return output_path
    
    # Try adding number suffix
    base_path = Path(output_path)
    stem = base_path.stem
    suffix = base_path.suffix
    counter = 1
    
    while True:
        new_path = base_path.parent / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            return str(new_path)
        counter += 1

def check_destination_conflicts(files, output_folder):
    """Check for potential file conflicts in destination folder"""
    conflicts = []
    for file_path in files:
        out_name = Path(file_path).stem + '.md'
        out_path = os.path.join(output_folder, out_name)
        if Path(out_path).exists():
            conflicts.append((file_path, out_path))
    return conflicts

class ProcessingWindow:
    """Window to show current file being processed"""
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("🔄 Processing Files")
        self.window.geometry("800x500")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()  # Make window modal
        
        # Make window stay on top and visible
        self.window.lift()
        self.window.attributes('-topmost', True)
        self.window.focus_force()
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"800x500+{x}+{y}")
        
        # Create widgets
        self.setup_ui()
        
        # Force window to show and update
        self.window.deiconify()
        self.window.update()
        self.window.focus_force()
        
        # Ensure window is visible and force update
        self.window.after(200, self.ensure_visible)
        self.window.after(500, self.force_update)
        
        # Log window creation
        logging.info('Processing window created')
        
    def setup_ui(self):
        # Main frame with border
        main_frame = tk.Frame(self.window, relief="raised", bd=3)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title with background
        title_frame = tk.Frame(main_frame, bg="#2196F3", relief="raised", bd=2)
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = tk.Label(title_frame, text="🔄 Processing Files", font=("Arial", 18, "bold"), 
                              fg="white", bg="#2196F3", padx=20, pady=10)
        title_label.pack()
        
        # Current file label with border
        file_frame = tk.Frame(main_frame, relief="groove", bd=2)
        file_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(file_frame, text="Current File:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
        self.current_file_label = tk.Label(file_frame, text="Preparing...", font=("Arial", 11), fg="#333")
        self.current_file_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        # Progress section
        progress_frame = tk.Frame(main_frame)
        progress_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(progress_frame, text="Progress:", font=("Arial", 10, "bold")).pack(anchor="w")
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100, length=400)
        self.progress_bar.pack(fill="x", pady=(5, 0))
        
        # Status label
        self.status_label = tk.Label(progress_frame, text="Starting...", font=("Arial", 10), fg="#666")
        self.status_label.pack(anchor="w", pady=(5, 0))
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=(20, 0))
        
        # Cancel button
        self.cancel_button = tk.Button(button_frame, text="❌ Cancel", command=self.cancel, 
                                     bg="#f44336", fg="white", font=("Arial", 11, "bold"),
                                     padx=20, pady=5)
        self.cancel_button.pack()
        
        self.cancelled = False
        
    def update_progress(self, current_file, current_index, total_files, status=""):
        """Update the processing window with current file and progress"""
        if self.cancelled:
            return
            
        try:
            # Update current file with size info
            file_name = Path(current_file).name
            try:
                file_size = Path(current_file).stat().st_size
                size_mb = file_size / (1024 * 1024)
                if size_mb > 1:
                    size_text = f"({size_mb:.1f} MB)"
                else:
                    size_text = f"({file_size / 1024:.1f} KB)"
            except:
                size_text = ""
            
            self.current_file_label.config(text=f"Processing: {file_name} {size_text}")
            
            # Update progress bar
            progress = (current_index / total_files) * 100
            self.progress_var.set(progress)
            
            # Update status
            if status:
                self.status_label.config(text=status)
            else:
                self.status_label.config(text=f"File {current_index + 1} of {total_files}")
                
            # Force window update
            self.window.update()
            self.window.update_idletasks()
            
            # Log progress
            logging.info(f'Progress: {current_index + 1}/{total_files} - {file_name} - {status}')
            
        except Exception as e:
            logging.error(f'Progress update failed: {e}')
        
    def cancel(self):
        """Cancel the processing"""
        self.cancelled = True
        self.status_label.config(text="Cancelling...")
        self.window.destroy()
        
    def ensure_visible(self):
        """Ensure the window is visible and on top"""
        try:
            self.window.lift()
            self.window.attributes('-topmost', True)
            self.window.focus_force()
            self.window.update()
        except:
            pass

    def force_update(self):
        """Force window update and ensure visibility"""
        try:
            self.window.update()
            self.window.lift()
            self.window.focus_force()
            logging.info('Processing window force update completed')
        except Exception as e:
            logging.error(f'Force update failed: {e}')

    def close(self):
        """Close the processing window"""
        self.window.destroy()

class TranslateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Batch Chinese-to-English Translator to Markdown")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Load saved settings
        self.settings = load_app_settings()
        
        self.input_folder = tk.StringVar(value=self.settings.get('input_folder', ''))
        self.output_folder = tk.StringVar(value=self.settings.get('output_folder', ''))
        self.engine = tk.StringVar(value=self.settings.get('engine', 'google'))
        self.deepl_key = tk.StringVar()
        self.openai_key = tk.StringVar()
        self.src_lang = tk.StringVar(value=self.settings.get('src_lang', 'Chinese (zh-cn) [zh-cn]'))
        self.tgt_lang = tk.StringVar(value=self.settings.get('tgt_lang', 'English (en) [en]'))
        self.files = []
        self.progress = tk.DoubleVar()
        self.status = tk.StringVar(value="Ready")
        self.conflict_mode = tk.StringVar(value=self.settings.get('conflict_mode', 'Auto Rename'))
        self.conflict_var = tk.StringVar(value=self.settings.get('conflict_mode', 'Auto Rename'))
        self.skip_translated_var = tk.BooleanVar(value=self.settings.get('skip_translated', True))
        
        # Load API keys from JSON file
        self.api_keys = load_api_keys()
        self.deepl_key.set(self.api_keys.get('deepl', ''))
        self.openai_key.set(self.api_keys.get('openai', ''))
        
        # Load translation history
        self.translation_history = load_translation_history()
        
        # Language mapping
        self.lang_map = {
            "Chinese (zh-cn) [zh-cn]": "zh-cn",
            "English (en) [en]": "en",
            "Japanese (ja) [ja]": "ja",
            "French (fr) [fr]": "fr",
            "German (de) [de]": "de",
            "Spanish (es) [es]": "es",
            "Korean (ko) [ko]": "ko",
            "Russian (ru) [ru]": "ru",
            "Italian (it) [it]": "it",
            "Portuguese (pt) [pt]": "pt",
            "Arabic (ar) [ar]": "ar",
            "Hindi (hi) [hi]": "hi",
        }
        
        self.setup_ui()
        
        # Set up automatic saving for settings changes
        self.setup_auto_save()
        logging.info('App started')

    def setup_ui(self):
        frm = tk.Frame(self.root)
        frm.pack(fill="both", expand=True, padx=10, pady=10)

        # Input folder
        tk.Label(frm, text="Input Folder:").grid(row=0, column=0, sticky="e")
        tk.Entry(frm, textvariable=self.input_folder, width=60).grid(row=0, column=1, sticky="w")
        tk.Button(frm, text="Browse", command=self.browse_input).grid(row=0, column=2, padx=5)

        # Output folder
        tk.Label(frm, text="Output Folder:").grid(row=1, column=0, sticky="e")
        tk.Entry(frm, textvariable=self.output_folder, width=60).grid(row=1, column=1, sticky="w")
        tk.Button(frm, text="Browse", command=self.browse_output).grid(row=1, column=2, padx=5)

        # Engine selection
        tk.Label(frm, text="Engine:").grid(row=2, column=0, sticky="e")
        engines = ["google", "deepl", "openai"]
        ttk.Combobox(frm, textvariable=self.engine, values=engines, state="readonly", width=10).grid(row=2, column=1, sticky="w")

        # Language selection
        LANGUAGES = [
            ("Chinese (zh-cn)", "zh-cn"),
            ("English (en)", "en"),
            ("Japanese (ja)", "ja"),
            ("French (fr)", "fr"),
            ("German (de)", "de"),
            ("Spanish (es)", "es"),
            ("Korean (ko)", "ko"),
            ("Russian (ru)", "ru"),
            ("Italian (it)", "it"),
            ("Portuguese (pt)", "pt"),
            ("Arabic (ar)", "ar"),
            ("Hindi (hi)", "hi"),
        ]
        tk.Label(frm, text="Source Language:").grid(row=3, column=0, sticky="e")
        ttk.Combobox(frm, textvariable=self.src_lang, values=[f"{n} [{c}]" for n, c in LANGUAGES], state="readonly", width=20).grid(row=3, column=1, sticky="w")
        tk.Label(frm, text="Target Language:").grid(row=4, column=0, sticky="e")
        ttk.Combobox(frm, textvariable=self.tgt_lang, values=[f"{n} [{c}]" for n, c in LANGUAGES], state="readonly", width=20).grid(row=4, column=1, sticky="w")
        # Map display string to code
        self.lang_map = {f"{n} [{c}]": c for n, c in LANGUAGES}

        # API key fields
        tk.Label(frm, text="DeepL API Key:").grid(row=5, column=0, sticky="e")
        tk.Entry(frm, textvariable=self.deepl_key, width=40).grid(row=5, column=1, sticky="w")
        tk.Label(frm, text="OpenAI API Key:").grid(row=6, column=0, sticky="e")
        tk.Entry(frm, textvariable=self.openai_key, width=40).grid(row=6, column=1, sticky="w")
        
        # Save API keys button
        tk.Button(frm, text="Save API Keys", command=self.save_api_keys_to_file, bg="#2196F3", fg="white").grid(row=6, column=2, padx=5)
        
        # Open API keys file button
        tk.Button(frm, text="Edit API Keys File", command=self.open_api_keys_file, bg="#FF9800", fg="white").grid(row=7, column=0, pady=5)
        tk.Button(frm, text="Reload API Keys", command=self.reload_api_keys, bg="#9C27B0", fg="white").grid(row=7, column=1, pady=5)
        
        # History management buttons
        tk.Button(frm, text="📊 View History", command=self.view_history, bg="#4CAF50", fg="white").grid(row=7, column=2, pady=5)
        tk.Button(frm, text="🔄 Reset History", command=self.reset_history, bg="#FF5722", fg="white").grid(row=8, column=0, pady=5)
        tk.Button(frm, text="⏭️ Skip Translated", command=self.toggle_skip_translated, bg="#607D8B", fg="white").grid(row=8, column=1, pady=5)
        tk.Button(frm, text="🔧 Repair History", command=self.repair_history, bg="#FFC107", fg="white").grid(row=8, column=2, pady=5)
        
        # Conflict resolution
        tk.Label(frm, text="File Conflicts:").grid(row=9, column=0, sticky="e", pady=5)
        conflict_modes = [
            ("Auto Rename", "auto_rename"),
            ("Overwrite", "overwrite"),
            ("Skip", "skip"),
            ("Ask Each Time", "ask")
        ]
        ttk.Combobox(frm, textvariable=self.conflict_mode, values=[mode[0] for mode in conflict_modes], 
                    state="readonly", width=15).grid(row=9, column=1, columnspan=2, sticky="w", pady=5)
        
        # Map display string to conflict mode
        self.conflict_map = {mode[0]: mode[1] for mode in conflict_modes}

        # File list
        tk.Button(frm, text="Scan Files", command=self.scan_files).grid(row=10, column=0, pady=10)
        self.file_listbox = tk.Listbox(frm, width=100, height=12)
        self.file_listbox.grid(row=11, column=0, columnspan=3, pady=5)
        
        # Progress section (beneath file list)
        progress_frame = tk.Frame(frm, relief="groove", bd=2)
        progress_frame.grid(row=12, column=0, columnspan=3, sticky="ew", pady=5, padx=5)
        
        # Progress title
        tk.Label(progress_frame, text="🔄 Translation Progress", font=("Arial", 10, "bold")).pack(anchor="w", padx=5, pady=(5,0))
        
        # Current file label
        self.current_file_label = tk.Label(progress_frame, text="Ready to translate...", font=("Arial", 9))
        self.current_file_label.pack(anchor="w", padx=5, pady=2)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill="x", padx=5, pady=2)
        
        # Status label
        self.status_label = tk.Label(progress_frame, text="No files to process", font=("Arial", 9))
        self.status_label.pack(anchor="w", padx=5, pady=(0,5))

        # Main action buttons in a frame
        button_frame = tk.Frame(frm)
        button_frame.grid(row=13, column=0, columnspan=3, pady=10)
        
        # Translate button (main action)
        tk.Button(button_frame, text="🚀 Translate All", command=self.start_translate_thread, 
                 bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), 
                 padx=20, pady=5).pack(side="left", padx=5)
        
        # Utility buttons in a separate frame
        utility_frame = tk.Frame(frm)
        utility_frame.grid(row=14, column=0, columnspan=3, pady=5)
        
        # Test processing window button
        tk.Button(utility_frame, text="🧪 Test", command=self.test_processing_window, 
                 bg="#FF9800", fg="white", font=("Arial", 9)).pack(side="left", padx=2)
        
        # Debug info button
        tk.Button(utility_frame, text="🐛 Debug", command=self.show_debug_info, 
                 bg="#9E9E9E", fg="white", font=("Arial", 9)).pack(side="left", padx=2)
        
        # Save settings button
        tk.Button(utility_frame, text="💾 Save Settings", command=self.manual_save_settings, 
                 bg="#4CAF50", fg="white", font=("Arial", 9)).pack(side="left", padx=2)
        
        # Add button to open log file location
        tk.Button(utility_frame, text="📁 Logs", command=self.open_log_folder, 
                 bg="#2196F3", fg="white", font=("Arial", 9)).pack(side="left", padx=2)

    def save_api_keys_to_file(self):
        """Save current API keys to JSON file"""
        try:
            keys = {
                'deepl': self.deepl_key.get(),
                'openai': self.openai_key.get()
            }
            save_api_keys(keys)
            messagebox.showinfo("Success", "API keys saved successfully!")
            logging.info('API keys saved to file')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save API keys: {e}")
            logging.error(f'Failed to save API keys: {e}')

    def open_api_keys_file(self):
        """Open API keys file for manual editing"""
        import platform, subprocess
        try:
            if platform.system() == "Windows":
                os.startfile(API_KEYS_FILE)
            elif platform.system() == "Darwin":
                subprocess.run(["open", API_KEYS_FILE])
            else:
                subprocess.run(["xdg-open", API_KEYS_FILE])
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open API keys file: {e}")

    def reload_api_keys(self):
        """Reload API keys from JSON file"""
        try:
            self.api_keys = load_api_keys()
            self.deepl_key.set(self.api_keys.get('deepl', ''))
            self.openai_key.set(self.api_keys.get('openai', ''))
            messagebox.showinfo("Success", "API keys reloaded from file!")
            logging.info('API keys reloaded from file')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reload API keys: {e}")
            logging.error(f'Failed to reload API keys: {e}')

    def view_history(self):
        """Show translation history"""
        history_text = f"Translation History:\n\n"
        history_text += f"Total files translated: {self.translation_history['total_files_translated']}\n"
        history_text += f"Last translation: {self.translation_history['last_translation_date'] or 'Never'}\n\n"
        
        if self.translation_history['translated_files']:
            history_text += "Recently translated files:\n"
            for file_path, info in list(self.translation_history['translated_files'].items())[-10:]:
                file_name = Path(file_path).name
                history_text += f"• {file_name} ({info['engine']}) - {info['translated_date']}\n"
        else:
            history_text += "No files have been translated yet."
        
        messagebox.showinfo("Translation History", history_text)

    def reset_history(self):
        """Reset translation history"""
        if messagebox.askyesno("Reset History", "Are you sure you want to reset the translation history? This will clear all recorded translations."):
            self.translation_history = {
                "translated_files": {},
                "last_translation_date": None,
                "total_files_translated": 0
            }
            save_translation_history(self.translation_history)
            messagebox.showinfo("Success", "Translation history has been reset!")
            logging.info('Translation history reset')

    def toggle_skip_translated(self):
        """Toggle skip translated files mode"""
        if not hasattr(self, 'skip_translated'):
            self.skip_translated = True
        else:
            self.skip_translated = not self.skip_translated
        
        status = "ON" if self.skip_translated else "OFF"
        messagebox.showinfo("Skip Mode", f"Skip already translated files: {status}")

    def test_processing_window(self):
        """Test the processing window to ensure it appears"""
        try:
            processing_window = ProcessingWindow(self.root)
            
            # Simulate some processing steps
            for i in range(5):
                if processing_window.cancelled:
                    break
                processing_window.update_progress(f"test_file_{i}.docx", i, 5, f"Testing step {i+1}/5")
                self.root.after(1000)  # Wait 1 second between updates
            
            processing_window.close()
            messagebox.showinfo("Test Complete", "Processing window test completed successfully!")
        except Exception as e:
            messagebox.showerror("Test Failed", f"Processing window test failed: {e}")

    def repair_history(self):
        """Repair corrupted translation history file"""
        try:
            # Backup current file
            if Path(HISTORY_FILE).exists():
                backup_file = HISTORY_FILE + '.repair_backup'
                import shutil
                shutil.copy2(HISTORY_FILE, backup_file)
            
            # Force reload of history
            self.translation_history = load_translation_history()
            
            # Validate and fix history structure
            if not isinstance(self.translation_history, dict):
                self.translation_history = {}
            
            if "translated_files" not in self.translation_history:
                self.translation_history["translated_files"] = {}
            
            if "last_translation_date" not in self.translation_history:
                self.translation_history["last_translation_date"] = None
            
            if "total_files_translated" not in self.translation_history:
                self.translation_history["total_files_translated"] = 0
            
            # Save repaired history
            save_translation_history(self.translation_history)
            
            messagebox.showinfo("History Repaired", 
                              f"Translation history has been repaired!\n\n"
                              f"Files in history: {len(self.translation_history['translated_files'])}\n"
                              f"Total translated: {self.translation_history['total_files_translated']}\n"
                              f"Last translation: {self.translation_history['last_translation_date'] or 'Never'}")
            
            logging.info('Translation history repaired successfully')
        except Exception as e:
            messagebox.showerror("Repair Failed", f"Failed to repair history: {e}")
            logging.error(f'Failed to repair history: {e}')

    def show_debug_info(self):
        """Show debug information about the current state"""
        try:
            debug_info = f"Debug Information:\n\n"
            debug_info += f"Files loaded: {len(self.files) if hasattr(self, 'files') else 0}\n"
            debug_info += f"Input folder: {self.input_folder.get() or 'Not set'}\n"
            debug_info += f"Output folder: {self.output_folder.get() or 'Not set'}\n"
            debug_info += f"Engine: {self.engine.get()}\n"
            debug_info += f"Skip translated: {getattr(self, 'skip_translated', 'Not set')}\n"
            debug_info += f"History files: {len(self.translation_history['translated_files'])}\n"
            debug_info += f"API keys loaded: {'Yes' if self.api_keys.get('deepl') or self.api_keys.get('openai') else 'No'}\n"
            debug_info += f"Log file: {LOG_FILE}\n"
            debug_info += f"History file: {HISTORY_FILE}\n"
            
            messagebox.showinfo("Debug Info", debug_info)
        except Exception as e:
            messagebox.showerror("Debug Error", f"Failed to get debug info: {e}")

    def open_log_folder(self):
        import platform, subprocess
        folder = os.path.abspath(os.path.dirname(LOG_FILE))
        try:
            if platform.system() == "Windows":
                os.startfile(folder)
            elif platform.system() == "Darwin":
                subprocess.run(["open", folder])
            else:
                subprocess.run(["xdg-open", folder])
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open log folder: {e}")

    def save_current_settings(self):
        """Save current settings to file"""
        try:
            settings = {
                "input_folder": self.input_folder.get(),
                "output_folder": self.output_folder.get(),
                "engine": self.engine.get(),
                "src_lang": self.src_lang.get(),
                "tgt_lang": self.tgt_lang.get(),
                "skip_translated": self.skip_translated_var.get(),
                "conflict_mode": self.conflict_mode.get()
            }
            save_app_settings(settings)
            logging.info('Settings saved')
            # Show success message if called from button
            if hasattr(self, '_settings_saved_from_button'):
                messagebox.showinfo("Success", "Settings saved successfully!")
                delattr(self, '_settings_saved_from_button')
        except Exception as e:
            logging.error(f'Failed to save settings: {e}')
            messagebox.showerror("Error", f"Failed to save settings: {e}")

    def setup_auto_save(self):
        """Set up automatic saving when settings change"""
        def on_setting_change(*args):
            self.save_current_settings()
        
        # Track changes to settings variables
        self.engine.trace_add("write", on_setting_change)
        self.src_lang.trace_add("write", on_setting_change)
        self.tgt_lang.trace_add("write", on_setting_change)
        self.skip_translated_var.trace_add("write", on_setting_change)
        self.conflict_mode.trace_add("write", on_setting_change)

    def manual_save_settings(self):
        """Manually save settings with user feedback"""
        self._settings_saved_from_button = True
        self.save_current_settings()

    def browse_input(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder.set(folder)
            self.save_current_settings()
            logging.info(f'Selected input folder: {folder}')

    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder.set(folder)
            self.save_current_settings()
            logging.info(f'Selected output folder: {folder}')

    def scan_files(self):
        folder = self.input_folder.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid input folder.")
            logging.error('Invalid input folder selected')
            return
        self.files = get_files_in_folder(folder)
        self.file_listbox.delete(0, tk.END)
        for f in self.files:
            self.file_listbox.insert(tk.END, str(f))
        self.status.set(f"Found {len(self.files)} files.")
        logging.info(f'Scanned files: {self.files}')

    def start_translate_thread(self):
        # Check if we have files to translate
        if not self.files:
            messagebox.showwarning("No Files", "Please scan files first before translating.")
            return
        
        # Check if output folder is selected
        if not self.output_folder.get():
            messagebox.showwarning("No Output Folder", "Please select an output folder before translating.")
            return
        
        # Run in main thread to avoid GUI issues
        self.translate_all()

    def translate_all(self):
        """Translate all files in the list using the new progress window"""
        if not self.files:
            self.status_label.config(text="No files to translate!")
            return
            
        if not self.output_folder.get():
            self.status_label.config(text="Please select an output folder!")
            return
            
        # Pre-check files and output folder
        valid_files = []
        for file_path in self.files:
            if os.path.exists(file_path):
                valid_files.append(file_path)
            else:
                self.status_label.config(text=f"File not found: {file_path}")
                return
                
        if not valid_files:
            self.status_label.config(text="No valid files to translate!")
            return
            
        if not os.path.exists(self.output_folder.get()):
            try:
                os.makedirs(self.output_folder.get())
            except Exception as e:
                self.status_label.config(text=f"Cannot create output folder: {e}")
                return
        
        # Load translation history
        history = load_translation_history()
        
        # Check for conflicts
        conflict_mode = self.conflict_var.get()
        conflicts = []
        for file_path in valid_files:
            output_path = self.get_output_path(file_path)
            if os.path.exists(output_path) and output_path != file_path:
                conflicts.append((file_path, output_path))
        
        if conflicts and conflict_mode == "ask":
            # Ask user for each conflict
            for file_path, output_path in conflicts:
                result = messagebox.askyesnocancel(
                    "File Conflict",
                    f"Output file exists:\n{output_path}\n\nOverwrite?",
                    icon=messagebox.WARNING
                )
                if result is None:  # Cancel
                    self.status_label.config(text="Translation cancelled")
                    return
                elif result:  # Yes - overwrite
                    pass
                else:  # No - skip
                    valid_files.remove(file_path)
        
        # Process files
        processed_count = 0
        skipped_count = 0
        error_count = 0
        total_files = len(valid_files)
        engine = self.engine.get()
        
        for i, file_path in enumerate(valid_files):
            try:
                # Update progress display
                filename = os.path.basename(file_path)
                self.current_file_label.config(text=f"Processing: {filename}")
                progress = ((i + 1) / total_files) * 100
                self.progress_var.set(progress)
                self.status_label.config(text=f"File {i+1} of {total_files}")
                self.root.update()
                
                # Check if already translated
                if self.skip_translated_var.get() and is_file_already_translated(file_path, self.get_output_path(file_path), history):
                    skipped_count += 1
                    self.status_label.config(text=f"Skipped (already translated): {filename}")
                    self.root.update()
                    continue
                
                # Check for conflicts
                output_path = self.get_output_path(file_path)
                if os.path.exists(output_path) and output_path != file_path:
                    if conflict_mode == "skip":
                        skipped_count += 1
                        self.status_label.config(text=f"Skipped (conflict): {filename}")
                        self.root.update()
                        continue
                    elif conflict_mode == "auto_rename":
                        output_path = self.get_unique_output_path(output_path)
                
                # Translate file
                self.translate_file(file_path, output_path)
                processed_count += 1
                
                # Update history
                update_translation_history(file_path, output_path, engine, history)
                
            except Exception as e:
                error_count += 1
                self.status_label.config(text=f"Error translating {filename}: {e}")
                self.root.update()
        
        # Show final summary
        summary = f"Translation complete! Processed: {processed_count}, Skipped: {skipped_count}, Errors: {error_count}"
        self.status_label.config(text=summary)
        self.current_file_label.config(text="Ready to translate...")
        self.progress_var.set(0)
        
        # Save history
        save_translation_history(history)
    
    def get_output_path(self, file_path):
        """Get the output path for a file"""
        filename = os.path.splitext(os.path.basename(file_path))[0] + '.md'
        return os.path.join(self.output_folder.get(), filename)
    
    def get_unique_output_path(self, output_path):
        """Get a unique output path by adding suffix if needed"""
        if not os.path.exists(output_path):
            return output_path
        
        base_path = os.path.splitext(output_path)[0]
        extension = os.path.splitext(output_path)[1]
        counter = 1
        
        while True:
            new_path = f"{base_path}_{counter}{extension}"
            if not os.path.exists(new_path):
                return new_path
            counter += 1
    
    def translate_file(self, file_path, output_path):
        """Translate a single file"""
        engine = self.engine.get()
        deepl_key = self.deepl_key.get()
        openai_key = self.openai_key.get()
        
        # Get selected language codes
        src_code = self.lang_map.get(self.src_lang.get(), 'zh-cn')
        tgt_code = self.lang_map.get(self.tgt_lang.get(), 'en')
        
        # Extract text based on file type
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.docx':
            text = extract_text_from_docx(file_path)
        elif ext == '.txt':
            text = extract_text_from_txt(file_path)
        elif ext == '.pdf':
            text = extract_text_from_pdf(file_path)
        elif ext == '.md':
            text = extract_text_from_md(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        
        # Translate text
        if engine == 'google':
            translated = translate_google(text, src=src_code, dest=tgt_code)
        elif engine == 'deepl':
            if not deepl_key:
                raise ValueError("DeepL API key required")
            # DeepL language code mapping
            deepl_lang_map = {
                'zh-cn': 'ZH', 'zh': 'ZH', 'en': 'EN-US',
                'ja': 'JA', 'fr': 'FR', 'de': 'DE', 'es': 'ES',
                'ko': 'KO', 'ru': 'RU', 'it': 'IT', 'pt': 'PT',
                'ar': 'AR', 'hi': 'HI'
            }
            deepl_src = deepl_lang_map.get(src_code, src_code.upper())
            deepl_tgt = deepl_lang_map.get(tgt_code, tgt_code.upper())
            translated = translate_deepl(text, deepl_key, src=deepl_src, dest=deepl_tgt)
        elif engine == 'openai':
            if not openai_key:
                raise ValueError("OpenAI API key required")
            translated = translate_openai(text, openai_key, model="gpt-3.5-turbo", src=src_code, dest=tgt_code)
        else:
            raise ValueError(f"Unknown engine: {engine}")
        
        # Save translated text
        save_as_md(translated, output_path)

if __name__ == '__main__':
    root = tk.Tk()
    app = TranslateApp(root)
    root.mainloop() 