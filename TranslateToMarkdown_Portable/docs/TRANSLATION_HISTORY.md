# Translation History System

## Overview
The translation system now includes a smart history feature that remembers which files have been translated and avoids re-processing them unnecessarily.

## Features

### 🔄 **Smart File Detection**
- **File Hash Tracking**: Uses file modification time and size to detect changes
- **Output Verification**: Checks if translated output file exists
- **Skip Mode**: Automatically skips already translated files

### 📊 **History Management**
- **View History**: See total files translated and recent translations
- **Reset History**: Clear all translation records to start fresh
- **Toggle Skip Mode**: Enable/disable automatic skipping

### ⚡ **Performance Benefits**
- **Faster Processing**: Skip already translated files
- **Time Savings**: No need to re-translate unchanged files
- **Batch Efficiency**: Process only new or modified files

## How It Works

### File Detection
1. **Hash Generation**: Creates unique hash from file modification time + size
2. **History Check**: Compares current hash with stored hash
3. **Output Check**: Verifies translated file exists in output folder
4. **Skip Decision**: Skips if hash matches and output exists

### Translation Process
1. **Scan Files**: Check all files in input folder
2. **Filter Files**: Separate new/modified files from already translated
3. **Show Summary**: Display how many files will be processed vs skipped
4. **Process Only New**: Translate only files that need it
5. **Update History**: Record successful translations with metadata

## UI Controls

### 📊 View History
- Shows total files translated
- Displays last translation date
- Lists 10 most recent translations with engine used

### 🔄 Reset History
- Clears all translation records
- Confirms before resetting
- Starts fresh translation tracking

### ⏭️ Skip Translated
- Toggle between ON/OFF modes
- ON: Skip already translated files
- OFF: Process all files (including already translated)

## File Storage

### History File: `translation_history.json`
```json
{
    "translated_files": {
        "path/to/file.docx": {
            "hash": "1234567890_1024",
            "output_path": "path/to/output/file.md",
            "engine": "deepl",
            "translated_date": "2024-01-15 14:30:25"
        }
    },
    "last_translation_date": "2024-01-15 14:30:25",
    "total_files_translated": 42
}
```

## Benefits

### ✅ **Time Efficiency**
- Skip unchanged files automatically
- Process only new or modified content
- Batch processing optimization

### ✅ **Resource Savings**
- Avoid unnecessary API calls
- Reduce processing time
- Save translation costs

### ✅ **Smart Workflow**
- Resume interrupted translations
- Track translation progress
- Maintain translation history

## Usage Tips

1. **First Run**: Process all files normally
2. **Subsequent Runs**: Only new/modified files will be processed
3. **File Changes**: Modify source files to force re-translation
4. **Reset When Needed**: Use reset to start fresh
5. **Check History**: View what's been translated before

## Advanced Features

### File Change Detection
- **Modification Time**: Detects when file was last changed
- **File Size**: Detects content changes
- **Combined Hash**: Unique identifier for file state

### Output Verification
- **File Existence**: Checks if output file exists
- **Path Validation**: Ensures output path is correct
- **Engine Tracking**: Records which translation engine was used

### Error Handling
- **Graceful Skipping**: Continues processing if file check fails
- **History Integrity**: Maintains history even with errors
- **User Feedback**: Shows clear status messages 