# SearchAuto Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
# Run the installation script
install_all.bat

# Or manually install
pip install -r requirements.txt
```

### Step 2: Run the Main Search Tool
```bash
# Double-click or run
run_search.bat

# Or manually
python searchAuto.py
```

### Step 3: Use the File Converters
```bash
# Unified converter (recommended)
run_converter.bat

# Or individual tools
python doc_to_docx_converter.py
python markdown_converter.py
```

### Step 4: Try the Integrated Application (Recommended)
```bash
# All-in-one tool with search, convert, and organize features
run_integrated.bat
```

## 📋 What Each Tool Does

### 🔍 SearchAuto (Main Tool)
- **Multi-root file search** across TXT, DOCX, PDF, XLSX files
- **Three search modes**: Live, Index, and AI-powered semantic search
- **Document summarization** with AI
- **Content column** showing previews and AI summaries
- **Background indexing** when system is idle

### 🔄 Unified Converter
- **DOC to DOCX**: Convert legacy .doc files to modern .docx format
- **Markdown Converter**: Convert DOCX, PDF, TXT to Markdown format
- **Batch processing** for multiple files
- **Chinese character support**

### 🚀 Integrated Application (All-in-One)
- **Search Tab**: Full SearchAuto functionality with live, index, and AI search
- **Convert Tab**: DOC to DOCX and Markdown conversion with progress tracking
- **Organize Tab**: Markdown collection management with auto-indexing and tag extraction
- **Seamless Workflow**: Switch between search, convert, and organize without closing the app

## 🎯 Common Use Cases

### For File Search:
1. Click "Add Root" to select folders
2. Click "Rebuild Index" to build keyword index
3. Click "Build AI" for semantic search capability
4. Use "🔍 Live Search" for quick searches
5. Use "⚡ Index Search" for fast searches
6. Use "🤖 AI Search" for natural language queries

### For File Conversion:
1. Run `run_converter.bat`
2. Choose "DOC to DOCX" tab for .doc files
3. Choose "Markdown" tab for DOCX/PDF/TXT files
4. Select input and output folders
5. Click "Start Conversion"

## 💡 Pro Tips

- **Install LibreOffice** for better DOC to DOCX conversion
- **Use AI Search** for finding meaning, not just keywords
- **Select specific roots** instead of searching all folders
- **Batch convert** files for efficiency
- **Chinese characters** are fully supported in all tools

## 🆘 Need Help?

- Check the main README.md for detailed documentation
- Look at the troubleshooting section for common issues
- Ensure all dependencies are installed correctly
- Try running tools individually to isolate problems
- For build issues, see BUILD_GUIDE.md

## 🏗️ Building Executables

For creating standalone executables:

```bash
# Simple build (no AI)
python build_simple_exe.py

# Full AI build
python build_full_ai_exe.py

# Light AI build
python build_simple_ai_exe.py
```

See [BUILD_GUIDE.md](BUILD_GUIDE.md) for complete build documentation.

## 📁 File Structure
```
SearchAuto/
├── searchAuto.py              # Main search application
├── searchauto_integrated.py   # All-in-one integrated app
├── unified_converter.py       # All-in-one converter
├── run_integrated.bat        # Quick start for integrated app
├── run_search.bat            # Quick start for search
├── run_converter.bat         # Quick start for converter
├── install_all.bat           # Complete installation
└── README.md                 # Full documentation
```

Happy searching and converting! 🎉 