#!/usr/bin/env python3
"""
Test script to simulate EXE imports and identify missing dependencies
"""

import sys
import os

def test_exe_style_imports():
    """Test imports the way the EXE would load them"""
    print("Testing EXE-style imports...")
    
    # Test 1: Basic imports
    try:
        print("1. Testing basic sentence_transformers import...")
        import sentence_transformers
        print("   [OK] sentence_transformers imported")
        
        # Test 2: Model loading
        print("2. Testing SentenceTransformer model loading...")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("   [OK] SentenceTransformer model loaded")
        
        # Test 3: Transformers pipeline
        print("3. Testing transformers pipeline...")
        from transformers import pipeline
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
        print("   [OK] Transformers pipeline created")
        
        # Test 4: ChromaDB
        print("4. Testing ChromaDB...")
        import chromadb
        client = chromadb.PersistentClient(path="test_exe_db")
        print("   [OK] ChromaDB client created")
        
        # Test 5: AI Search Engine (simulate EXE loading)
        print("5. Testing AI Search Engine import...")
        import ai_search
        print("   [OK] ai_search module imported")
        
        # Test 6: Initialize AI engine
        print("6. Testing AI engine initialization...")
        from ai_search import AISearchEngine
        engine = AISearchEngine("test_exe_db")
        if engine.initialize():
            print("   [OK] AI Search Engine initialized")
        else:
            print("   [ERR] AI Search Engine failed to initialize")
        
        print("\n[SUCCESS] All EXE-style imports work correctly!")
        return True
        
    except ImportError as e:
        print(f"   [ERR] Import Error: {e}")
        print(f"   [INFO] This module might be missing from the EXE bundle")
        return False
    except Exception as e:
        print(f"   [ERR] Runtime Error: {e}")
        print(f"   [INFO] This might be a runtime issue in the EXE")
        return False

def test_hidden_imports():
    """Test specific hidden imports that might be missing"""
    print("\nTesting hidden imports...")
    
    hidden_imports = [
        'torch.nn.functional',
        'torch.utils.data',
        'torch.cuda',
        'transformers.pipelines',
        'transformers.models.bart',
        'transformers.modeling_utils',
        'huggingface_hub',
        'tokenizers',
        'accelerate',
        'safetensors',
        'regex',
        'requests',
        'urllib3',
        'packaging',
        'filelock',
        'typing_extensions',
        'importlib_metadata',
        'zipp'
    ]
    
    failed_imports = []
    for module in hidden_imports:
        try:
            __import__(module)
            print(f"   [OK] {module}")
        except ImportError as e:
            print(f"   [ERR] {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n[WARN] Failed imports: {failed_imports}")
        return False
    else:
        print("\n[OK] All hidden imports available")
        return True

if __name__ == "__main__":
    print("=== EXE Import Test ===")
    
    # Test 1: EXE-style imports
    success1 = test_exe_style_imports()
    
    # Test 2: Hidden imports
    success2 = test_hidden_imports()
    
    if success1 and success2:
        print("\n[SUCCESS] All tests passed! EXE should work correctly.")
    else:
        print("\n[WARN] Some tests failed. This might explain the EXE issues.")
    
    input("\nPress Enter to continue...") 