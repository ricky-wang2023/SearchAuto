# File Conflict Resolution System

## Overview
The translation system now includes intelligent file conflict resolution to prevent overwriting existing files in the destination folder.

## Conflict Resolution Options

### 🔄 **Auto Rename** (Default)
- **Behavior**: Automatically adds number suffix to avoid conflicts
- **Example**: `document.md` → `document_1.md` → `document_2.md`
- **Use Case**: Safe default, never overwrites existing files

### ⚠️ **Overwrite**
- **Behavior**: Replaces existing files with new translations
- **Example**: `document.md` → `document.md` (overwrites)
- **Use Case**: When you want to update existing translations

### ⏭️ **Skip**
- **Behavior**: Skips files that would create conflicts
- **Example**: `document.md` → (skipped, keeps existing)
- **Use Case**: Preserve existing files, only translate new ones

### ❓ **Ask Each Time**
- **Behavior**: Prompts user for each conflict
- **Options**: Auto Rename / Overwrite / Skip
- **Use Case**: Manual control over each conflict

## How It Works

### 1. **Conflict Detection**
- Scans destination folder before processing
- Identifies files that would be overwritten
- Shows conflict summary to user

### 2. **User Choice**
- **Auto Mode**: Uses selected conflict resolution
- **Ask Mode**: Prompts for each conflict
- **Bulk Mode**: Applies same choice to all conflicts

### 3. **File Processing**
- **Auto Rename**: Generates unique filename
- **Overwrite**: Replaces existing file
- **Skip**: Excludes from processing

## UI Controls

### File Conflicts Dropdown
- **Location**: Bottom of main interface
- **Options**: Auto Rename, Overwrite, Skip, Ask Each Time
- **Default**: Auto Rename

### Conflict Dialog (Ask Mode)
- **Shows**: List of conflicting files
- **Buttons**: Yes (Auto Rename) / No (Overwrite) / Cancel (Skip)
- **Limit**: Shows first 5 conflicts + count

## Examples

### Scenario 1: Auto Rename
```
Input: document.docx
Output folder: has document.md
Result: document_1.md (new file)
```

### Scenario 2: Overwrite
```
Input: document.docx
Output folder: has document.md
Result: document.md (replaced)
```

### Scenario 3: Skip
```
Input: document.docx
Output folder: has document.md
Result: document.md (unchanged, skipped)
```

### Scenario 4: Multiple Conflicts
```
Input: [doc1.docx, doc2.docx, doc3.docx]
Output folder: has [doc1.md, doc2.md]
Result: doc1_1.md, doc2_1.md, doc3.md
```

## Benefits

### ✅ **Data Safety**
- Prevents accidental file overwrites
- Preserves existing translations
- Safe default behavior

### ✅ **Flexibility**
- Multiple resolution strategies
- User choice per situation
- Bulk or individual control

### ✅ **Efficiency**
- Automatic conflict detection
- Smart filename generation
- Batch processing support

## Best Practices

### 🎯 **For New Projects**
- Use **Auto Rename** to avoid conflicts
- Review generated filenames
- Organize output folder structure

### 🎯 **For Updates**
- Use **Overwrite** to replace old translations
- Backup important files first
- Check translation quality

### 🎯 **For Mixed Content**
- Use **Ask Each Time** for control
- Review each conflict individually
- Choose based on file importance

### 🎯 **For Batch Processing**
- Use **Skip** to preserve existing work
- Process only new files
- Maintain translation history

## Advanced Features

### Smart Filename Generation
- **Pattern**: `original_name_number.md`
- **Increment**: Automatically finds next available number
- **Uniqueness**: Guaranteed unique filenames

### Conflict Summary
- **Pre-processing**: Shows conflict count before starting
- **Real-time**: Updates during processing
- **Post-processing**: Shows final results

### Error Handling
- **Graceful**: Continues processing despite conflicts
- **Informative**: Clear error messages
- **Recoverable**: Can retry with different settings

## Configuration

### Default Settings
- **Conflict Mode**: Auto Rename
- **Skip Translated**: Enabled
- **History Tracking**: Enabled

### Customization
- **Change Mode**: Use dropdown in UI
- **Per-Session**: Settings apply to current session
- **Persistent**: Settings saved between runs

## Troubleshooting

### Common Issues

**Q: Files are being skipped unexpectedly**
A: Check if "Skip Translated" is enabled and files exist in history

**Q: Too many numbered files**
A: Use "Overwrite" mode or clean up destination folder

**Q: Want to reprocess specific files**
A: Use "Reset History" or modify source files to change hash

**Q: Conflict dialog not appearing**
A: Ensure "Ask Each Time" is selected in dropdown

### Tips
- **Backup**: Always backup important files before overwriting
- **Test**: Try with small batch first
- **Review**: Check output filenames after processing
- **Organize**: Use subfolders to avoid conflicts 