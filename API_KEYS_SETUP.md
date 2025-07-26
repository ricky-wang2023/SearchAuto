# API Keys Setup Guide

## How to Set Up API Keys

### Option 1: Using the GUI (Recommended)
1. **Run the translate script**: `.\run_translate.bat`
2. **Enter your API keys** in the GUI fields:
   - DeepL API Key: Get from https://www.deepl.com/pro-api
   - OpenAI API Key: Get from https://platform.openai.com/api-keys
3. **Click "Save API Keys"** to save them to `api_keys.json`
4. **Your keys will be automatically loaded** next time you run the script

### Option 2: Manual File Editing
1. **Edit `api_keys.json`** directly:
   ```json
   {
       "deepl": "your-deepl-api-key-here",
       "openai": "your-openai-api-key-here"
   }
   ```
2. **Save the file** and restart the application
3. **Click "Reload API Keys"** in the GUI to load changes

### Option 3: Using the GUI Buttons
- **"Edit API Keys File"**: Opens `api_keys.json` in your default text editor
- **"Reload API Keys"**: Reloads keys from the file into the GUI
- **"Save API Keys"**: Saves current GUI values to the file

## Getting API Keys

### DeepL API Key
1. Visit: https://www.deepl.com/pro-api
2. Sign up for a free account (500,000 characters/month)
3. Get your API key from the dashboard
4. Format: `12345678-1234-1234-1234-123456789abc`

### OpenAI API Key
1. Visit: https://platform.openai.com/api-keys
2. Sign up for an OpenAI account
3. Create a new API key
4. Format: `sk-1234567890abcdef...`

## Security Notes
- The `api_keys.json` file is stored locally on your computer
- Keep this file secure and don't share it
- Consider adding `api_keys.json` to your `.gitignore` if using version control 