# SearchAuto Build Guide

This guide covers all build options for creating standalone executables and installers for SearchAuto.

## 🏗️ Build Options

### 1. Simple Build (No AI)
Creates a lightweight executable without AI dependencies.

```bash
# Build simple version
python build_simple_exe.py

# Or manually with PyInstaller
pyinstaller SearchAuto.spec
```

**Features:**
- ✅ Fast build time
- ✅ Small file size (~50MB)
- ✅ Basic search functionality
- ❌ No AI search capabilities
- ❌ No document summarization

### 2. Full AI Build
Creates a complete executable with all AI capabilities.

```bash
# Build full AI version
python build_full_ai_exe.py

# Or manually with PyInstaller
pyinstaller SearchAuto_FullAI.spec
```

**Features:**
- ✅ Complete AI search functionality
- ✅ Document summarization
- ✅ Semantic search capabilities
- ❌ Large file size (~2GB)
- ❌ Long build time

### 3. Light AI Build
Creates a medium-sized executable with basic AI features.

```bash
# Build light AI version
python build_simple_ai_exe.py
```

**Features:**
- ✅ Basic AI search functionality
- ✅ Moderate file size (~500MB)
- ✅ Faster build than full AI
- ❌ Limited AI features

## 📦 Installation Packages

### Windows Installer (NSIS)
Creates a professional Windows installer.

```bash
# Build installer
python build_exe.py
```

**Requirements:**
- NSIS (Nullsoft Scriptable Install System)
- Windows environment

### Portable Package
Creates a portable version that can run from any location.

```bash
# Create portable package
python build_exe.py --portable
```

## 🔧 Build Scripts Overview

### Core Build Scripts
- `build_exe.py` - Main build script with installer creation
- `build_simple_exe.py` - Lightweight build without AI
- `build_full_ai_exe.py` - Complete AI build
- `build_simple_ai_exe.py` - Medium AI build

### Installation Scripts
- `install_all.bat` - Complete installation for development
- `install_full_ai.bat` - AI-specific installation
- `fix_ai_models.bat` - Fix AI model issues in EXE

### Testing Scripts
- `test_ai.py` - Test AI functionality
- `check_threads.py` - Verify threading setup

## 🚀 Quick Build Commands

### For Development
```bash
# Install all dependencies
install_all.bat

# Run directly
python searchAuto.py
```

### For Distribution
```bash
# Build simple version
python build_simple_exe.py

# Build full AI version
python build_full_ai_exe.py

# Create installer
python build_exe.py --installer
```

## 📋 Build Requirements

### System Requirements
- Python 3.7 or higher
- Windows 10/11 (for Windows builds)
- 8GB+ RAM (for AI builds)
- 10GB+ free disk space (for AI builds)

### Python Dependencies
```bash
pip install -r requirements.txt
pip install pyinstaller
```

### Optional Dependencies
- NSIS (for Windows installer)
- UPX (for executable compression)

## 🔍 Troubleshooting Build Issues

### Common Issues

#### "Module not found" Errors
```bash
# Solution: Add missing imports to spec file
# Edit SearchAuto_FullAI.spec and add to hiddenimports
```

#### Large File Size
```bash
# Solution: Use simple build or exclude unnecessary modules
# Edit spec file and add to excludes list
```

#### AI Models Not Loading
```bash
# Solution: Run fix script
fix_ai_models.bat
```

#### Build Fails with Memory Error
```bash
# Solution: Increase system memory or use simple build
# Close other applications during build
```

### Build Optimization Tips

1. **Use Simple Build** for basic functionality
2. **Use Full AI Build** only when AI features are needed
3. **Exclude matplotlib/scipy** to reduce size
4. **Use UPX compression** for smaller files
5. **Build on SSD** for faster builds

## 📁 Output Files

### Executables
- `dist/SearchAuto.exe` - Simple version
- `dist/SearchAuto_FullAI.exe` - Full AI version
- `dist/SearchAuto_LightAI.exe` - Light AI version

### Installers
- `SearchAuto_Setup.exe` - Windows installer
- `SearchAuto_Portable.zip` - Portable package

### Build Artifacts
- `build/` - Temporary build files
- `dist/` - Final executables
- `*.spec` - PyInstaller specification files

## 🔄 Build Process Flow

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. **Choose Build Type**
   - Simple: `python build_simple_exe.py`
   - Full AI: `python build_full_ai_exe.py`
   - Light AI: `python build_simple_ai_exe.py`

3. **Test Build**
   ```bash
   # Test the executable
   dist/SearchAuto.exe
   ```

4. **Create Installer** (Optional)
   ```bash
   python build_exe.py --installer
   ```

## 📊 Build Comparison

| Build Type | Size | Build Time | AI Features | Use Case |
|------------|------|------------|-------------|----------|
| Simple | ~50MB | 2-3 min | ❌ | Basic search |
| Light AI | ~500MB | 10-15 min | ✅ Basic | Moderate AI |
| Full AI | ~2GB | 30-45 min | ✅ Complete | Full AI |

## 🎯 Recommended Build Strategy

### For End Users
- **Simple Build**: For basic file search needs
- **Light AI Build**: For moderate AI requirements
- **Full AI Build**: For complete AI functionality

### For Developers
- **Development**: Run `python searchAuto.py` directly
- **Testing**: Use simple build for quick testing
- **Distribution**: Use appropriate build based on target users

## 📞 Build Support

For build issues:
1. Check the troubleshooting section above
2. Ensure all dependencies are installed
3. Verify Python version compatibility
4. Check available disk space and memory
5. Try building in a clean environment

## 🔄 Version History

### Build Scripts v2.1
- ✅ Updated Content column support
- ✅ Enhanced AI model handling
- ✅ Improved error handling
- ✅ Better dependency management

### Build Scripts v2.0
- ✅ Added AI build options
- ✅ Created installer scripts
- ✅ Added portable package support
- ✅ Improved build optimization

### Build Scripts v1.0
- ✅ Basic PyInstaller integration
- ✅ Simple executable creation
- ✅ Windows installer support 