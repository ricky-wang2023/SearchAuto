# Translate to Markdown GUI

A Python GUI application for batch translation of Chinese documents to English Markdown format.

## Features

- ✅ **Multiple Translation Engines**: Google Translate, DeepL, OpenAI
- ✅ **Multiple File Formats**: DOCX, PDF, TXT, MD
- ✅ **Progress Window**: Real-time progress display without popup interruptions
- ✅ **Translation History**: Automatically skips already translated files
- ✅ **Conflict Resolution**: Auto-rename, overwrite, skip, or ask for each file
- ✅ **Settings Memory**: Remembers last used folders and settings
- ✅ **Virtual Environment**: Automatic setup and management

## Quick Start

### Option 1: Use the Launcher (Recommended)
Double-click one of these files:
- `launch.bat` - For Command Prompt
- `launch.ps1` - For PowerShell

The launcher will automatically:
1. Create virtual environment if needed
2. Install dependencies
3. Start the GUI

### Option 2: Manual Setup
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install python-docx PyPDF2 openai googletrans==4.0.0-rc1 deepl
pip install httpx==0.13.3 httpcore==0.9.1

# Run the application
python translate_to_md_gui.py
```

## Usage

1. **Select Input Folder**: Choose folder containing files to translate
2. **Select Output Folder**: Choose where to save translated files
3. **Choose Translation Engine**: Google (free), DeepL (API key), or OpenAI (API key)
4. **Configure Languages**: Source (Chinese) and Target (English)
5. **Scan Files**: Click "Scan Files" to load documents
6. **Translate**: Click "🚀 Translate All" to start translation

## Features

### Progress Window
- Real-time progress display beneath file list
- No popup interruptions during translation
- Shows current file being processed
- Displays file size and status

### Translation History
- Automatically skips already translated files
- Tracks file hashes to detect changes
- View history with "View History" button
- Reset history if needed

### Conflict Resolution
- **Auto Rename**: Adds suffix to avoid overwriting
- **Overwrite**: Replace existing files
- **Skip**: Skip files that would overwrite
- **Ask Each Time**: Prompt for each conflict

### Settings Memory
- Automatically remembers input/output folders
- Saves translation engine preference
- Remembers language selections
- Stores conflict resolution mode
- Settings saved in `app_settings.json`
- Manual save button available

### API Keys
- DeepL API key for DeepL engine
- OpenAI API key for OpenAI engine
- Keys saved in `api_keys.json`
- Edit keys via GUI buttons

## File Formats Supported

- **DOCX**: Microsoft Word documents
- **PDF**: PDF documents (text extraction)
- **TXT**: Plain text files
- **MD**: Markdown files

## Output

All files are translated to English and saved as Markdown (`.md`) files in the output folder.

## Troubleshooting

### Virtual Environment Issues
- Use `launch.bat` or `launch.ps1` for automatic setup
- Ensure Python 3.7+ is installed
- Check that `venv` folder exists

### Translation Issues
- Check API keys for DeepL/OpenAI engines
- Ensure input files are readable
- Check output folder permissions

### GUI Issues
- Window size increased to 900x700
- All buttons should be visible
- Progress window appears beneath file list

## Files

- `translate_to_md_gui.py` - Main application
- `launch.bat` - Windows batch launcher
- `launch.ps1` - PowerShell launcher
- `api_keys.json` - API keys storage
- `translation_history.json` - Translation history
- `app_settings.json` - Application settings
- `venv/` - Virtual environment folder 