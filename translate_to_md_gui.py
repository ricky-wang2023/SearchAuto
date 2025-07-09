# --- PATCH for googletrans/httpx on Python 3.13+ (cgi module removed) ---
import sys
import types
if sys.version_info >= (3, 13):
    sys.modules['cgi'] = types.ModuleType('cgi')
    setattr(sys.modules['cgi'], 'parse_header', lambda x: (x, {}))
# ------------------------------------------------------------------------
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from docx import Document
import PyPDF2
import logging

LOG_FILE = 'translate_to_md_debug.log'
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

try:
    from googletrans import Translator as GoogleTranslator
except ImportError:
    GoogleTranslator = None
try:
    import openai
except ImportError:
    openai = None
try:
    import deepl
except ImportError:
    deepl = None

SUPPORTED_EXTS = ['.docx', '.txt', '.pdf', '.md']

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

class TranslateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Batch Chinese-to-English Translator to Markdown")
        self.root.geometry("800x600")
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.engine = tk.StringVar(value='google')
        self.deepl_key = tk.StringVar()
        self.openai_key = tk.StringVar()
        self.src_lang = tk.StringVar(value='zh-cn')
        self.tgt_lang = tk.StringVar(value='en')
        self.files = []
        self.progress = tk.DoubleVar()
        self.status = tk.StringVar(value="Ready")
        self.setup_ui()
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

        # API key fields (move down)
        tk.Label(frm, text="DeepL API Key:").grid(row=5, column=0, sticky="e")
        tk.Entry(frm, textvariable=self.deepl_key, width=40).grid(row=5, column=1, sticky="w")
        tk.Label(frm, text="OpenAI API Key:").grid(row=6, column=0, sticky="e")
        tk.Entry(frm, textvariable=self.openai_key, width=40).grid(row=6, column=1, sticky="w")

        # File list
        tk.Button(frm, text="Scan Files", command=self.scan_files).grid(row=7, column=0, pady=10)
        self.file_listbox = tk.Listbox(frm, width=100, height=15)
        self.file_listbox.grid(row=8, column=0, columnspan=3, pady=5)

        # Progress bar
        ttk.Progressbar(frm, variable=self.progress, maximum=100).grid(row=9, column=0, columnspan=3, sticky="ew", pady=5)
        tk.Label(frm, textvariable=self.status).grid(row=10, column=0, columnspan=3, sticky="w")

        # Translate button
        tk.Button(frm, text="Translate All", command=self.start_translate_thread, bg="#4CAF50", fg="white", font=("Arial", 11, "bold")).grid(row=11, column=0, columnspan=3, pady=10)
        # Add button to open log file location
        tk.Button(frm, text="Open Debug Log Folder", command=self.open_log_folder).grid(row=12, column=0, columnspan=3, pady=5)

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

    def browse_input(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder.set(folder)
            logging.info(f'Selected input folder: {folder}')

    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder.set(folder)
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
        threading.Thread(target=self.translate_all, daemon=True).start()

    def translate_all(self):
        if not self.files:
            self.status.set("No files to translate. Please scan files first.")
            logging.warning('No files to translate')
            return
        out_folder = self.output_folder.get()
        if not out_folder or not os.path.isdir(out_folder):
            messagebox.showerror("Error", "Please select a valid output folder.")
            logging.error('Invalid output folder selected')
            return
        engine = self.engine.get()
        deepl_key = self.deepl_key.get()
        openai_key = self.openai_key.get()
        # Get selected language codes
        src_code = self.lang_map.get(self.src_lang.get(), 'zh-cn')
        tgt_code = self.lang_map.get(self.tgt_lang.get(), 'en')
        logging.info(f'Translation started: engine={engine}, out_folder={out_folder}, src={src_code}, tgt={tgt_code}')
        self.progress.set(0)
        for idx, file_path in enumerate(self.files):
            try:
                ext = Path(file_path).suffix.lower()
                logging.info(f'Translating file: {file_path}')
                if ext == '.docx':
                    text = extract_text_from_docx(file_path)
                elif ext == '.txt':
                    text = extract_text_from_txt(file_path)
                elif ext == '.pdf':
                    text = extract_text_from_pdf(file_path)
                elif ext == '.md':
                    text = extract_text_from_md(file_path)
                else:
                    self.status.set(f"Unsupported file: {file_path}")
                    logging.warning(f'Unsupported file: {file_path}')
                    continue
                if engine == 'google':
                    translated = translate_google(text, src=src_code, dest=tgt_code)
                elif engine == 'deepl':
                    if not deepl_key:
                        self.status.set("DeepL API key required.")
                        logging.error('DeepL API key missing')
                        continue
                    # DeepL uses EN-US, JA, ZH, etc.
                    deepl_src = src_code.upper().replace('-', '_')
                    deepl_tgt = tgt_code.upper().replace('-', '_')
                    translated = translate_deepl(text, deepl_key, src=deepl_src, dest=deepl_tgt)
                elif engine == 'openai':
                    if not openai_key:
                        self.status.set("OpenAI API key required.")
                        logging.error('OpenAI API key missing')
                        continue
                    translated = translate_openai(text, openai_key, model="gpt-3.5-turbo", src=src_code, dest=tgt_code)
                else:
                    self.status.set(f"Unknown engine: {engine}")
                    logging.error(f'Unknown engine: {engine}')
                    continue
                out_name = Path(file_path).stem + '.md'
                out_path = os.path.join(out_folder, out_name)
                save_as_md(translated, out_path)
                self.status.set(f"Translated: {file_path} -> {out_path}")
                logging.info(f'Success: {file_path} -> {out_path}')
            except Exception as e:
                self.status.set(f"Error with {file_path}: {e}")
                logging.exception(f'Error with {file_path}')
            self.progress.set((idx + 1) / len(self.files) * 100)
        self.status.set("All files processed.")
        logging.info('All files processed')

if __name__ == '__main__':
    root = tk.Tk()
    app = TranslateApp(root)
    root.mainloop() 