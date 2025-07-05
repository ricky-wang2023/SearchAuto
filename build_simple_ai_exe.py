#!/usr/bin/env python3
"""
Simple AI build script for SearchAuto
"""

import os
import sys
import subprocess

def build_simple_ai_exe():
    """Build AI EXE without cleaning previous builds"""
    print("🔨 Building SearchAuto EXE (AI Version)...")
    
    # Build with PyInstaller - AI version
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=SearchAuto_AI",
        "--add-data=README.md;.",
        "--add-data=requirements.txt;.",
        "--add-data=ai_search.py;.",
        "--add-data=ai_search_light.py;.",
        "--add-data=check_threads.py;.",
        "--hidden-import=sentence_transformers",
        "--hidden-import=transformers",
        "--hidden-import=chromadb",
        "--hidden-import=torch",
        "--hidden-import=huggingface_hub",
        "--hidden-import=numpy",
        "--hidden-import=tokenizers",
        "--hidden-import=accelerate",
        "--hidden-import=safetensors",
        "--hidden-import=regex",
        "--hidden-import=requests",
        "--hidden-import=urllib3",
        "--hidden-import=packaging",
        "--hidden-import=filelock",
        "--hidden-import=typing_extensions",
        "--hidden-import=importlib_metadata",
        "--hidden-import=zipp",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--collect-all=sentence_transformers",
        "--collect-all=transformers",
        "--collect-all=chromadb",
        "--exclude-module=matplotlib",
        "--exclude-module=scipy",
        "searchAuto.py"
    ]
    
    if os.path.exists('icon.ico'):
        cmd.extend(['--icon=icon.ico'])
    
    subprocess.run(cmd, check=True)
    print("✅ AI EXE build completed!")

def create_ai_test_script():
    """Create a script to test AI functionality"""
    test_script = '''import sys
import os

def test_ai_components():
    """Test AI components to diagnose issues"""
    print("Testing AI components...")
    
    try:
        print("1. Testing sentence_transformers...")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("   ✓ SentenceTransformer loaded successfully")
        
        print("2. Testing transformers...")
        from transformers import pipeline
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
        print("   ✓ Transformers pipeline loaded successfully")
        
        print("3. Testing chromadb...")
        import chromadb
        client = chromadb.PersistentClient(path="test_ai_db")
        print("   ✓ ChromaDB initialized successfully")
        
        print("4. Testing AI search engine...")
        from ai_search import AISearchEngine
        engine = AISearchEngine("test_ai_db")
        if engine.initialize():
            print("   ✓ AI Search Engine initialized successfully")
        else:
            print("   ✗ AI Search Engine failed to initialize")
            
        print("\\nAll AI components are working correctly!")
        return True
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_ai_components()
    if not success:
        print("\\nAI components test failed. Please check your installation.")
    input("Press Enter to continue...")
'''
    
    with open('test_ai.py', 'w') as f:
        f.write(test_script)
    print("✅ Created test_ai.py")

def main():
    """Main build process"""
    print("🚀 SearchAuto AI Build Process")
    print("=" * 40)
    
    # Build AI EXE
    build_simple_ai_exe()
    
    # Create AI test script
    create_ai_test_script()
    
    print("\n🎉 AI build completed successfully!")
    print("\n📁 Generated files:")
    print("  - dist/SearchAuto_AI.exe (AI EXE)")
    print("  - test_ai.py (AI test script)")
    print("\n💡 Troubleshooting:")
    print("  1. If AI search doesn't work, run test_ai.py to diagnose")
    print("  2. Make sure you have sufficient disk space for AI models (~2GB)")
    print("  3. First run will download AI models automatically")

if __name__ == "__main__":
    main() 