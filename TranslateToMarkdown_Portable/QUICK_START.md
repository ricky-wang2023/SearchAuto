# Translate to Markdown - Portable Quick Start

## 🚀 Quick Start

### Option 1: Windows Command Prompt
1. Double-click `launch.bat`
2. Wait for setup to complete
3. Use the GUI!

### Option 2: PowerShell
1. Right-click `launch.ps1` → "Run with PowerShell"
2. Wait for setup to complete
3. Use the GUI!

## 📋 Requirements

- **Python 3.7+** installed on your system
- **Internet connection** for first-time setup (downloads dependencies)
- **Windows 10/11** (tested on Windows 10)

## 🎯 What's Included

- ✅ **Complete translation application** with GUI
- ✅ **Automatic virtual environment** setup
- ✅ **All dependencies** included
- ✅ **Documentation** in `docs/` folder
- ✅ **Settings memory** - remembers your preferences
- ✅ **Translation history** - tracks processed files
- ✅ **Multiple engines** - Google, DeepL, OpenAI

## 📁 Folder Structure

```
TranslateToMarkdown_Portable/
├── launch.bat              # Windows launcher
├── launch.ps1              # PowerShell launcher
├── translate_to_md_gui.py  # Main application
├── requirements.txt         # Python dependencies
├── docs/                   # Documentation
│   ├── README.md
│   ├── API_KEYS_SETUP.md
│   ├── TRANSLATION_HISTORY.md
│   └── FILE_CONFLICT_RESOLUTION.md
└── venv/                   # Virtual environment (created automatically)
```

## 🔧 First Time Setup

1. **Download** the portable folder to your computer
2. **Extract** if it's a ZIP file
3. **Double-click** `launch.bat` or `launch.ps1`
4. **Wait** for automatic setup (5-10 minutes first time)
5. **Start translating!**

## 📖 Documentation

- **README.md** - Complete feature guide
- **API_KEYS_SETUP.md** - How to set up DeepL/OpenAI keys
- **TRANSLATION_HISTORY.md** - How translation history works
- **FILE_CONFLICT_RESOLUTION.md** - How to handle file conflicts

## 🎮 Usage

1. **Select Input Folder** - Choose folder with files to translate
2. **Select Output Folder** - Choose where to save translated files
3. **Choose Engine** - Google (free), DeepL, or OpenAI
4. **Set Languages** - Source (Chinese) and Target (English)
5. **Scan Files** - Click "Scan Files" to load documents
6. **Translate** - Click "🚀 Translate All" to start

## 🔑 API Keys (Optional)

- **Google Translate**: Free, no key needed
- **DeepL**: Get API key from https://www.deepl.com/pro-api
- **OpenAI**: Get API key from https://platform.openai.com/api-keys

## 💾 Data Files

The app creates these files automatically:
- `api_keys.json` - Your API keys
- `app_settings.json` - Your settings (folders, preferences)
- `translation_history.json` - Translation history

## 🆘 Troubleshooting

### Python Not Found
- Install Python from https://python.org
- Check "Add Python to PATH" during installation

### Virtual Environment Issues
- Delete the `venv` folder
- Run launcher again

### Dependencies Issues
- Check internet connection
- Try running launcher as Administrator

### GUI Issues
- Ensure Python 3.7+ is installed
- Check Windows display settings

## 📞 Support

If you encounter issues:
1. Check the documentation in `docs/` folder
2. Look for error messages in the launcher
3. Ensure Python 3.7+ is installed and in PATH

---

**Enjoy translating! 🎉** 