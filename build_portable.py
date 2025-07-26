import shutil
import os
import glob

PORTABLE_DIR = "SearchAuto_Portable"
INCLUDE_FILES = [
    "*.py", "*.json", "*.env", "*.md", "*.ico", "*.bat", "requirements.txt"
]
INCLUDE_DIRS = [
    "ai_search_db", "test_ai_db", "test_db", "test_exe_db", "FileMonitor_Portable"
]

# Clean previous build
if os.path.exists(PORTABLE_DIR):
    shutil.rmtree(PORTABLE_DIR)
os.makedirs(PORTABLE_DIR, exist_ok=True)

# Copy files
for pattern in INCLUDE_FILES:
    for file in glob.glob(pattern):
        shutil.copy2(file, PORTABLE_DIR)

# Copy directories
for d in INCLUDE_DIRS:
    if os.path.exists(d):
        shutil.copytree(d, os.path.join(PORTABLE_DIR, d))

print(f"Portable package created in {PORTABLE_DIR}/. You can now zip and deploy this folder.") 