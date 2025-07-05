# SearchAuto - Universal File Content Search Tool

A powerful, multi-root file content search application with a Tkinter GUI that supports indexing and searching across multiple file types including text files, DOCX documents, PDF files, and Excel spreadsheets. Now enhanced with **AI-powered semantic search** capabilities!

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
- **Multi-language Support**: Works across different languages
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
```

### System Requirements
- Python 3.7 or higher
- Windows, macOS, or Linux
- Sufficient disk space for index database (~2GB for AI models)
- Read access to target directories
- Internet connection for initial AI model download

## 🛠️ Installation

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

## 📖 Usage Guide

### Initial Setup

1. **Launch the Application**: Run `python searchAuto.py`
2. **Add Root Directories**: Click "Add Root" to select folders to index
3. **Build Regular Index**: Click "Rebuild Index" to create the keyword index
4. **Build AI Index**: Click "Build AI" to create the semantic search index
5. **Start Searching**: Use Live Search, Index Search, or AI Search

### Adding Root Directories

1. Click the **"Add Root"** button
2. Select a directory from the file dialog
3. The directory will appear in the roots list
4. Use **Ctrl+Click** to select multiple roots for targeted searching

### Managing Roots

- **Remove Roots**: Select root(s) and click "Remove Root" (removes from index)
- **Reorder Roots**: Select a root and use ▲/▼ buttons to change order
- **Multi-Select**: Hold Ctrl while clicking to select multiple roots

### Searching Files

#### Live Search (Real-time)
- **Best for**: Quick searches, small directories, or when index is outdated
- **Usage**: Enter keyword and click "🔍 Live Search"
- **Pros**: Always up-to-date, no index required
- **Cons**: Slower for large directories

#### Index Search (Pre-built index)
- **Best for**: Large directories, frequent searches, performance
- **Usage**: Enter keyword and click "⚡ Index Search"
- **Pros**: Very fast, supports complex queries
- **Cons**: Requires index to be built and updated

#### AI Search (Semantic search)
- **Best for**: Finding meaning, not just keywords; natural language queries
- **Usage**: Enter natural language query and click "🤖 AI Search"
- **Pros**: Understands context and meaning, finds related concepts, generates summaries
- **Cons**: Requires AI index to be built, uses more resources

### Understanding Search Results

Each result shows:
- **File Type**: TXT, DOCX, PDF, or XLSX (color-coded)
- **File Path**: Full path to the file
- **Location**: Where the match was found (line, paragraph, sheet, or AI match with similarity score)
- **Content**: Preview of the matching text (with AI-generated summary if available)
- **Actions**: "📄 Open File" and "📁 Folder" buttons

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

### Performance Tips

1. **Use Index Search** for large directories
2. **Use AI Search** for semantic understanding and natural language queries
3. **Select specific roots** instead of searching all
4. **Keep index updated** for best performance
5. **Close unnecessary applications** during large operations
6. **Allow first AI run** to download models completely

## 📁 File Structure

```
SearchAuto/
├── searchAuto.py          # Main application file
├── ai_search.py           # AI search engine module
├── ai_search_light.py     # Lightweight AI search (alternative)
├── file_index.db          # SQLite keyword index database (created automatically)
├── ai_search_db/          # ChromaDB AI index directory (created automatically)
├── README.md              # This documentation
└── requirements.txt       # Python dependencies
```

## 🔒 Security & Privacy

- **Local Only**: All operations are performed locally
- **No Data Collection**: No information is sent to external servers
- **File Access**: Only reads files, never modifies them
- **Database**: Index database contains only file paths and content excerpts
- **AI Models**: Downloaded once and cached locally, no ongoing internet required
- **Privacy**: All AI processing happens on your local machine

## 🚀 Advanced Usage

### AI Search Examples
Try these natural language queries with AI Search:
- "How to fix printer problems"
- "Budget reports for Q4"
- "Meeting notes about project updates"
- "Error handling procedures"
- "Customer feedback and complaints"

### Command Line Options
Currently, the application runs in GUI mode only. Future versions may include command-line options.

### Custom File Types
To add support for additional file types, modify the `extract_file_content()` function in `searchAuto.py`.

### Database Maintenance
- **Keyword Index**: Delete `file_index.db` and rebuild
- **AI Index**: Use "🗑️ Clear AI" button or delete `ai_search_db/` directory
- **AI Models**: Stored in `~/.cache/huggingface/`, can be deleted to free space

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please check the license file for details.

## 🆘 Support

For issues and questions:
1. Check this README for troubleshooting
2. Review the error messages in the application
3. Check the console output for detailed error information
4. Create an issue with detailed steps to reproduce the problem

## 🔄 Version History

### Current Version
- Multi-root support
- Idle-based auto-updates
- Thread-safe database operations
- Enhanced UI with status indicators
- Comprehensive error handling

### Planned Features
- Command-line interface
- Additional file format support
- Advanced search filters
- Export search results
- Cloud storage integration

---

**Note**: This application is designed for personal and organizational use. Ensure you have proper permissions to access and search the directories you add to the index. 