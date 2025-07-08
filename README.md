# SearchAuto - Universal File Content Search Tool

A powerful, multi-root file content search application with a Tkinter GUI that supports indexing and searching across multiple file types including text files, DOCX documents, PDF files, and Excel spreadsheets. Now enhanced with **AI-powered semantic search** capabilities and **file conversion tools**!

## 🚀 Features

### Core Functionality
- **Multi-Root Support**: Index and search across multiple root directories simultaneously
- **Multiple File Types**: Supports TXT, DOCX, PDF, and XLSX files
- **Three Search Modes**:
  - **Live Search**: Real-time file scanning (no index required)
  - **Index Search**: Fast keyword search using pre-built index
  - **AI Search**: Advanced semantic search with document understanding
- **Smart Indexing**: Automatic background updates when system is idle
- **Thread-Safe**: Database locking prevents conflicts during concurrent operations

### File Conversion Tools
- **DOC to DOCX Converter**: Convert legacy .doc files to modern .docx format
- **Markdown Converter**: Convert DOCX, PDF, and TXT files to Markdown format
- **Unified Converter**: All-in-one tool with both conversion features
- **Multiple Conversion Methods**: LibreOffice, Microsoft Word, and python-docx support
- **Batch Processing**: Convert multiple files at once
- **Chinese Character Support**: Full Unicode support for international documents

### User Interface
- **Intuitive GUI**: Clean, organized interface with separate sections for different functions
- **Root Management**: Add, remove, and reorder indexed directories with up/down buttons
- **Multi-Select**: Select multiple roots for targeted searching
- **Real-Time Status**: Visual indicators for indexing progress and system idle status
- **Results Display**: Scrollable results with file opening and folder navigation options
- **AI Search Integration**: Dedicated AI search button with semantic capabilities
- **Document Summaries**: AI-generated summaries displayed in search results

### Advanced Features
- **AI-Powered Semantic Search**: Understands meaning, not just keywords
- **Document Summarization**: Auto-generates summaries of long documents
- **Enhanced Query Processing**: Automatically adds synonyms and related terms
- **Multi-language Support**: Works across different languages including Chinese
- **Idle-Based Updates**: Automatic index updates only when system is inactive for 30+ minutes
- **Activity Tracking**: Monitors user interactions to determine optimal update times
- **Conflict Prevention**: Prevents database locking issues with comprehensive thread safety
- **File Navigation**: Direct file opening and folder location access from search results
- **Background Processing**: Non-blocking operations keep the GUI responsive

## 📋 Requirements

### Python Dependencies
```bash
pip install python-docx
pip install PyPDF2
pip install pandas
pip install openpyxl
pip install pdfminer.six
pip install sentence-transformers
pip install chromadb
pip install torch
pip install transformers
pip install pywin32
```

### System Requirements
- Python 3.7 or higher
- Windows, macOS, or Linux
- Sufficient disk space for index database (~2GB for AI models)
- Read access to target directories
- Internet connection for initial AI model download
- Microsoft Word (optional, for DOC to DOCX conversion)
- LibreOffice (optional, for better DOC to DOCX conversion)

## 🛠️ Installation

### Quick Start
1. **Clone or Download**: Get the SearchAuto files
2. **Install Dependencies**:
   ```bash
   cd SearchAuto
   pip install -r requirements.txt
   ```
3. **Run the Application**:
   ```bash
   python searchAuto.py
   ```

### Building Standalone Executables
For creating standalone executables and installers, see the comprehensive [BUILD_GUIDE.md](BUILD_GUIDE.md).

**Quick Build Commands:**
```bash
# Simple build (no AI)
python build_simple_exe.py

# Full AI build
python build_full_ai_exe.py

# Light AI build
python build_simple_ai_exe.py
```

## 📖 Usage Guide

### SearchAuto Main Application

#### Initial Setup
1. **Launch the Application**: Run `python searchAuto.py`
2. **Add Root Directories**: Click "Add Root" to select folders to index
3. **Build Regular Index**: Click "Rebuild Index" to create the keyword index
4. **Build AI Index**: Click "Build AI" to create the semantic search index
5. **Start Searching**: Use Live Search, Index Search, or AI Search

#### Adding Root Directories
1. Click the **"Add Root"** button
2. Select a directory from the file dialog
3. The directory will appear in the roots list
4. Use **Ctrl+Click** to select multiple roots for targeted searching

#### Managing Roots
- **Remove Roots**: Select root(s) and click "Remove Root" (removes from index)
- **Reorder Roots**: Select a root and use ▲/▼ buttons to change order
- **Multi-Select**: Hold Ctrl while clicking to select multiple roots

#### Searching Files

##### Live Search (Real-time)
- **Best for**: Quick searches, small directories, or when index is outdated
- **Usage**: Enter keyword and click "🔍 Live Search"
- **Pros**: Always up-to-date, no index required
- **Cons**: Slower for large directories

##### Index Search (Pre-built index)
- **Best for**: Large directories, frequent searches, performance
- **Usage**: Enter keyword and click "⚡ Index Search"
- **Pros**: Very fast, supports complex queries
- **Cons**: Requires index to be built and updated

##### AI Search (Semantic search)
- **Best for**: Finding meaning, not just keywords; natural language queries
- **Usage**: Enter natural language query and click "🤖 AI Search"
- **Pros**: Understands context and meaning, finds related concepts, generates summaries
- **Cons**: Requires AI index to be built, uses more resources

### File Conversion Tools

#### DOC to DOCX Converter
```bash
# GUI Version
python doc_to_docx_converter.py

# Command Line Version
python doc_converter_cli.py "C:\Input\Folder" "C:\Output\Folder"
```

**Features:**
- Convert legacy .doc files to modern .docx format
- Multiple conversion methods (LibreOffice, Microsoft Word, python-docx)
- Smart file detection (handles DOCX files disguised as DOC)
- Chinese character support
- Batch processing for multiple files

#### Markdown Converter
```bash
# GUI Version
python markdown_converter.py

# Command Line Version
python markdown_converter_cli.py "C:\Input\Folder" "C:\Output\Folder" "docx,pdf,txt"
```

**Features:**
- Convert DOCX, PDF, and TXT files to Markdown format
- Smart formatting detection (headings, bold, italic)
- Multiple input format support
- Batch processing
- Chinese character support

#### Unified Converter (Recommended)
```bash
python unified_converter.py
```

**Features:**
- All-in-one tool with both DOC to DOCX and Markdown conversion
- Tabbed interface for easy switching between conversion types
- Shared progress tracking and status updates
- Professional UI with consistent interface

#### 🚀 Integrated Application (All-in-One)
```bash
python searchauto_integrated.py
# or
run_integrated.bat
```

**Features:**
- **Search Tab**: Full SearchAuto functionality with live, index, and AI search
- **Convert Tab**: DOC to DOCX and Markdown conversion with progress tracking
- **Organize Tab**: Markdown collection management with auto-indexing and tag extraction
- **Seamless Workflow**: Switch between search, convert, and organize without closing the app
- **Unified Database**: All tools share the same file index and AI models
- **Professional UI**: Tabbed interface with consistent design across all features

### Understanding Search Results

Each result shows:
- **File Type**: TXT, DOCX, PDF, or XLSX (color-coded)
- **File Path**: Full path to the file
- **Location**: Where the match was found (line, paragraph, sheet, or AI match with similarity score)
- **Content**: Preview of the matching text with AI-generated summaries for AI search results
- **Actions**: "📄 Open File" and "📁 Folder" buttons

**Content Column Features:**
- **AI Search Results**: Shows AI-generated summaries followed by content preview
- **Regular Search Results**: Shows content preview only
- **Tooltip Support**: Hover over content to see full text
- **Smart Truncation**: Long content is truncated with "..." and full text available on hover

### Index Management

#### Manual Index Operations
- **🔄 Rebuild Index**: Completely rebuilds the keyword index (use when adding new roots)
- **🔄 Update Index**: Incrementally updates existing keyword index (faster)
- **🤖 Build AI**: Creates semantic search index from existing keyword index
- **🗑️ Clear AI**: Clears the AI search index
- **❌ Cancel**: Stops ongoing indexing operations

#### Automatic Updates
- **Idle Detection**: System monitors user activity
- **Auto-Update**: Runs when system is idle for 30+ minutes
- **Status Display**: Shows current idle time and update status

## 🔧 Configuration

### Adjusting Idle Settings
Edit these variables in `searchAuto.py`:
```python
idle_check_interval = 5 * 60 * 1000  # Check every 5 minutes
idle_threshold = 30 * 60             # Wait 30 minutes of inactivity
```

### Database Location
- **Keyword Index**: `file_index.db` in the same directory as the script
- **AI Index**: `ai_search_db/` directory with ChromaDB collections
- **AI Models**: Downloaded to `~/.cache/huggingface/` on first use

## 🐛 Troubleshooting

### Common Issues

#### "Database is locked" Error
- **Cause**: Multiple operations trying to access database simultaneously
- **Solution**: Wait a moment and try again (threading protection should handle this)

#### Search Returns No Results
- **Check**: Ensure files are in supported formats (TXT, DOCX, PDF, XLSX)
- **Check**: Verify root directories are properly added
- **Check**: Try rebuilding the index if using Index Search
- **Check**: For AI Search, ensure AI index is built and try different query terms

#### Slow Performance
- **Live Search**: Use Index Search for large directories
- **Index Search**: Ensure index is up-to-date
- **AI Search**: First run downloads models (~2GB), subsequent runs are faster
- **General**: Close other resource-intensive applications

#### File Opening Issues
- **Windows**: Ensure file associations are set correctly
- **Permissions**: Check file and folder access permissions
- **Path Issues**: Verify file paths don't contain special characters

#### Conversion Issues
- **DOC to DOCX**: Install LibreOffice for best results with old DOC files
- **Microsoft Word**: Ensure Word is installed for Windows conversion
- **Chinese Characters**: All tools support Unicode and Chinese characters
- **Large Files**: Conversion may take time for very large documents

### Performance Tips

1. **Use Index Search** for large directories
2. **Use AI Search** for semantic understanding and natural language queries
3. **Select specific roots** instead of searching all
4. **Keep index updated** for best performance
5. **Close unnecessary applications** during large operations
6. **Allow first AI run** to download models completely
7. **Use LibreOffice** for better DOC to DOCX conversion
8. **Batch convert** files for efficiency

## 📁 File Structure

```
SearchAuto/
├── searchAuto.py                  # Main search application
├── searchauto_integrated.py       # Integrated app (search + convert + organize)
├── ai_search.py                   # AI search engine module
├── ai_search_light.py             # Lightweight AI search (alternative)
├── doc_to_docx_converter.py      # DOC to DOCX converter (GUI)
├── doc_converter_cli.py          # DOC to DOCX converter (CLI)
├── markdown_converter.py         # Markdown converter (GUI)
├── markdown_converter_cli.py     # Markdown converter (CLI)
├── unified_converter.py          # All-in-one converter tool
├── run_integrated.bat            # Quick start for integrated app
├── run_search.bat                # Quick start for search tool
├── run_converter.bat             # Quick start for converter
├── install_all.bat               # Complete installation
├── build_exe.py                  # Main build script
├── build_simple_exe.py           # Simple build (no AI)
├── build_full_ai_exe.py          # Full AI build
├── build_simple_ai_exe.py        # Light AI build
├── SearchAuto.spec               # PyInstaller spec (simple)
├── SearchAuto_FullAI.spec        # PyInstaller spec (full AI)
├── installer.nsi                 # NSIS installer script
├── file_index.db                 # SQLite keyword index database (created automatically)
├── ai_search_db/                 # ChromaDB AI index directory (created automatically)
├── README.md                     # This documentation
├── BUILD_GUIDE.md               # Build documentation
├── QUICK_START.md               # Quick start guide
└── requirements.txt              # Python dependencies
```

## 🔒 Security & Privacy

- **Local Processing**: All file processing happens locally on your machine
- **No Data Upload**: No files or content are uploaded to external servers
- **AI Models**: Downloaded once and stored locally for future use
- **Index Privacy**: All search indexes are stored locally in your project directory

## 🌟 Recent Updates

### Version 2.1 - Enhanced Search Results Display
- ✅ **Content Column**: New column showing content previews and AI summaries
- ✅ **AI Summary Integration**: AI-generated summaries displayed in search results
- ✅ **Tooltip Support**: Hover over content to see full text
- ✅ **Smart Truncation**: Long content intelligently truncated with full text on hover
- ✅ **Enhanced UI**: Improved layout with better content visibility
- ✅ **Cross-Search Compatibility**: Content column works with all search modes

### Version 2.0 - File Conversion Tools
- ✅ **DOC to DOCX Converter**: Convert legacy .doc files to modern .docx format
- ✅ **Markdown Converter**: Convert DOCX, PDF, and TXT files to Markdown
- ✅ **Unified Converter**: All-in-one tool with tabbed interface
- ✅ **Chinese Character Support**: Full Unicode support for international documents
- ✅ **Multiple Conversion Methods**: LibreOffice, Microsoft Word, python-docx
- ✅ **Batch Processing**: Convert multiple files simultaneously
- ✅ **Smart File Detection**: Automatically detects file formats
- ✅ **Professional UI**: Clean, modern interface with progress tracking

### Version 1.0 - Core Search Features
- ✅ **Multi-root file indexing and search**
- ✅ **AI-powered semantic search**
- ✅ **Live, Index, and AI search modes**
- ✅ **Document summarization**
- ✅ **Multi-language support**
- ✅ **Background indexing**
- ✅ **Thread-safe operations**

## 📞 Support

For issues, questions, or feature requests:
1. Check the troubleshooting section above
2. Ensure all dependencies are installed correctly
3. Try running the conversion tools separately to isolate issues
4. Check file permissions and paths for conversion tools

## 📄 License

This project is open source and available under the MIT License. 