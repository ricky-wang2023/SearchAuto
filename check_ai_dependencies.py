#!/usr/bin/env python3
"""
AI Dependency Checker for SearchAuto Full AI Version
"""

import sys
import subprocess
import importlib

def check_package(package_name, import_name=None, version_check=True):
    """Check if a package is installed and optionally get its version"""
    if import_name is None:
        import_name = package_name
    
    try:
        module = importlib.import_module(import_name)
        if version_check and hasattr(module, '__version__'):
            print(f"✅ {package_name}: {module.__version__}")
        else:
            print(f"✅ {package_name}: Installed")
        return True
    except ImportError:
        print(f"❌ {package_name}: Not installed")
        return False

def check_ai_models():
    """Check if AI models can be loaded"""
    print("\n🔍 Checking AI Models...")
    
    try:
        print("Testing SentenceTransformer model...")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ SentenceTransformer model loaded successfully")
        
        print("Testing Transformers summarization model...")
        from transformers.pipelines import pipeline
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
        print("✅ Transformers summarization model loaded successfully")
        
        return True
    except Exception as e:
        print(f"❌ AI Models error: {e}")
        return False

def check_chromadb():
    """Check ChromaDB functionality"""
    print("\n🔍 Checking ChromaDB...")
    try:
        import chromadb
        client = chromadb.PersistentClient(path="test_db")
        # Use get_or_create_collection if available, else handle exception
        if hasattr(client, 'get_or_create_collection'):
            collection = client.get_or_create_collection(name="test_collection")
        else:
            try:
                collection = client.create_collection(name="test_collection")
            except Exception as e:
                if "already exists" in str(e):
                    collection = client.get_collection(name="test_collection")
                else:
                    raise
        collection.add(
            documents=["This is a test document"],
            metadatas=[{"source": "test"}],
            ids=["test_id"]
        )
        print("✅ ChromaDB working correctly")
        return True
    except Exception as e:
        print(f"❌ ChromaDB error: {e}")
        return False

def check_torch():
    """Check PyTorch installation and capabilities"""
    print("\n🔍 Checking PyTorch...")
    try:
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        print(f"✅ CUDA available: {torch.cuda.is_available()}")
        cuda_version = getattr(getattr(torch, 'version', None), 'cuda', None)
        if torch.cuda.is_available() and cuda_version:
            print(f"✅ CUDA version: {cuda_version}")
        return True
    except Exception as e:
        print(f"❌ PyTorch error: {e}")
        return False

def main():
    """Main dependency check"""
    print("🔧 AI Dependencies Check for SearchAuto")
    print("=" * 50)
    
    # Core AI packages
    core_packages = [
        ("torch", "torch"),
        ("transformers", "transformers"),
        ("sentence-transformers", "sentence_transformers"),
        ("chromadb", "chromadb"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("scikit-learn", "sklearn"),
        ("huggingface-hub", "huggingface_hub"),
        ("tokenizers", "tokenizers"),
        ("accelerate", "accelerate"),
        ("safetensors", "safetensors"),
        ("regex", "regex"),
        ("requests", "requests"),
        ("urllib3", "urllib3"),
        ("packaging", "packaging"),
        ("filelock", "filelock"),
        ("typing-extensions", "typing_extensions"),
        ("importlib-metadata", "importlib_metadata"),
        ("zipp", "zipp"),
    ]
    
    print("\n📦 Checking Core AI Packages...")
    all_installed = True
    for package, import_name in core_packages:
        if not check_package(package, import_name):
            all_installed = False
    
    # Check AI models
    models_ok = check_ai_models()
    
    # Check ChromaDB
    chromadb_ok = check_chromadb()
    
    # Check PyTorch
    torch_ok = check_torch()
    
    print("\n📊 Summary:")
    print("=" * 50)
    if all_installed and models_ok and chromadb_ok and torch_ok:
        print("✅ All AI dependencies are installed and working!")
        print("✅ Ready to build SearchAuto Full AI EXE")
    else:
        print("❌ Some dependencies are missing or not working")
        print("\n💡 To install missing packages:")
        print("   pip install torch transformers sentence-transformers chromadb")
        print("   pip install numpy pandas scikit-learn huggingface-hub")
        print("   pip install tokenizers accelerate safetensors")
    
    return all_installed and models_ok and chromadb_ok and torch_ok

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Dependency check failed. Please install missing packages.")
        sys.exit(1)
    else:
        print("\n🎉 All dependencies ready for build!") 