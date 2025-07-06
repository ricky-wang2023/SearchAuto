# File Monitor & Auto-Converter

This script monitors folders for new or changed files and automatically converts them using standalone conversion functions (no extra GUI windows).

## Features

1. **Monitor Multiple Folders**: Add multiple folders to monitor for new or changed files
2. **Automatic DOC to DOCX Conversion**: When a new `.doc` file is detected, it's converted to `.docx` in the specified output folder
3. **Automatic DOCX to Markdown Conversion**: When a new `.docx` file is detected (or after DOC conversion), it's converted to `.md` in the specified output folder
4. **File Change Detection**: Uses file modification time and size to detect changes
5. **Overwrite Old Files**: Automatically overwrites existing converted files
6. **Real-time Logging**: Shows conversion progress and status in real-time
7. **Configuration Persistence**: Saves your folder settings between sessions
8. **Background Processing**: Processes existing files in background thread (GUI stays responsive)
9. **Configurable Monitoring Interval**: Adjust check frequency from 1-60 seconds
10. **Folder Structure Preservation**: Maintains original folder hierarchy in output folders
11. **Multiple Monitoring Folders**: Organizes output by source folder to prevent name collisions

## Requirements

- Python 3.6+
- Required dependencies: `python-docx`, `PyPDF2`, `pdfminer.six`
- Optional: LibreOffice or Microsoft Word for better DOC to DOCX conversion

## Usage

1. **Run the script**:
   ```bash
   python file_monitor.py
   ```

2. **Add Monitor Folders**: Click "Add Folder" to select folders you want to monitor

3. **Set Output Folders**: 
   - Set the DOCX output folder (where converted DOC files will be saved)
   - Set the Markdown output folder (where converted Markdown files will be saved)

4. **Configure Monitoring Interval**: Adjust the check interval (1-60 seconds) based on your needs

5. **Start Monitoring**: Click "Start Monitoring" to begin watching for file changes

6. **View Logs**: The activity log shows all conversion activities in real-time

## How It Works

### For DOC Files:
1. When a new `.doc` file is detected → Convert to `.docx` → Convert to `.md`
2. When an existing `.doc` file is modified → Convert to `.docx` → Convert to `.md`

### For DOCX Files:
1. When a new `.docx` file is detected → Convert directly to `.md`
2. When an existing `.docx` file is modified → Convert to `.md`

### Background Processing:
- **Immediate Response**: GUI becomes responsive immediately when starting monitoring
- **Real-time Monitoring**: File watching starts right away in background
- **Background Conversion**: Existing files are processed in separate thread
- **No GUI Blocking**: You can interact with interface while files are being converted

## File Structure with Multiple Monitoring Folders

### Input Structure:
```
C:\Work\
├── report1.doc              # File directly in root
├── meeting.docx             # File directly in root
├── Projects\                # Subfolder
│   ├── project1.doc
│   └── subfolder\
│       └── project2.docx
└── Archive\                 # Subfolder
    └── old_report.doc

C:\Personal\
├── todo.docx                # File directly in root
├── notes.md                 # File directly in root
├── Ideas\                   # Subfolder
│   └── brainstorm.doc
└── Photos\                  # Subfolder
    └── description.docx
```

### Output Structure:
```
Converted_Markdown\
├── Work\                    # Root folder name
│   ├── report1.md          # File from root
│   ├── meeting.md          # File from root
│   ├── Projects\           # Preserved subfolder
│   │   ├── project1.md
│   │   └── subfolder\
│   │       └── project2.md
│   └── Archive\            # Preserved subfolder
│       └── old_report.md
├── Personal\               # Root folder name
│   ├── todo.md             # File from root
│   ├── notes.md            # File from root
│   ├── Ideas\              # Preserved subfolder
│   │   └── brainstorm.md
│   └── Photos\             # Preserved subfolder
│       └── description.md
```

## Monitoring Interval Recommendations

| **Interval** | **Best for** | **Pros** | **Cons** |
|-------------|-------------|----------|----------|
| **1-2 seconds** | Active editing, frequent saves | Very responsive | Higher CPU usage |
| **3-5 seconds** | Normal work, occasional saves | Good balance | Slight delay |
| **10-15 seconds** | Batch processing, infrequent changes | Low CPU usage | Slower response |
| **30+ seconds** | Background monitoring, large folders | Minimal impact | Significant delay |

## Integration with SearchAuto.py

### Optimized Workflow:
1. **File Monitor** converts DOC/DOCX → Markdown (organized structure)
2. **SearchAuto.py** indexes the converted Markdown files
3. **Result**: Fast, accurate search through clean, organized content

### Benefits:
- **Faster indexing** - Markdown files index much faster than DOCX
- **Better search accuracy** - Clean text without formatting artifacts
- **Organized results** - Clear folder structure in search results
- **No name collisions** - Separate subfolders for each monitored folder

### Recommended Setup:
```
C:\SearchAuto\
├── Original_Files/          # Your source DOC/DOCX files
├── Converted_Markdown/      # File Monitor output
└── SearchAuto.py            # Your search tool
```

## Configuration

The script saves your settings in `file_monitor_config.json`:
- Monitor folders list
- DOCX output folder
- Markdown output folder
- Monitoring interval

## Troubleshooting

1. **Converters not found**: Ensure required dependencies are installed:
   ```bash
   pip install python-docx PyPDF2 pdfminer.six
   ```

2. **Permission errors**: Make sure you have write permissions to the output folders

3. **File locked**: The script will retry if a file is temporarily locked by another application

4. **Conversion failures**: Check the log for specific error messages. Some old DOC files may require LibreOffice or Microsoft Word for conversion

5. **High CPU usage**: Increase the monitoring interval to reduce system impact

## Performance Notes

- The script checks for file changes every 2-60 seconds (configurable)
- Files are overwritten automatically when they change
- The script maintains a hash of files to detect changes efficiently
- All conversion errors are logged for debugging
- Background processing keeps the GUI responsive during initial file conversion

## Advanced Features

### Background Processing:
- Initial file processing runs in background thread
- GUI remains responsive during conversion
- Real-time monitoring starts immediately
- Progress updates in activity log

### Folder Structure Preservation:
- Maintains original folder hierarchy
- Creates separate subfolders for each monitored folder
- Prevents name collisions between different source folders
- Organizes output logically for easy navigation

### Configurable Monitoring:
- Adjustable check interval (1-60 seconds)
- Settings saved automatically
- Real-time interval changes
- Optimized for different use cases

This setup provides efficient file conversion with organized output, perfect for integration with search tools like SearchAuto.py! 