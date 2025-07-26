#!/usr/bin/env python3
"""
Test script for AI search functionality
"""

import os
import sys

def test_ai_imports():
    """Test if all AI dependencies can be imported"""
    print("Testing AI imports...")
    
    try:
        import sentence_transformers
        print("✓ sentence_transformers imported successfully")
    except Exception as e:
        print(f"✗ sentence_transformers import failed: {e}")
        return False
    
    try:
        import chromadb
        print("✓ chromadb imported successfully")
    except Exception as e:
        print(f"✗ chromadb import failed: {e}")
        return False
    
    try:
        import torch
        print("✓ torch imported successfully")
    except Exception as e:
        print(f"✗ torch import failed: {e}")
        return False
    
    try:
        from transformers import pipeline
        print("✓ transformers pipeline imported successfully")
    except Exception as e:
        print(f"✗ transformers pipeline import failed: {e}")
        return False
    
    return True

def test_ai_search():
    """Test AI search functionality"""
    print("\nTesting AI search functionality...")
    
    try:
        from ai_search import initialize_ai_search, add_documents_to_ai_index, ai_search, clear_ai_index, get_ai_index_stats
        print("✓ AI search module imported successfully")
    except Exception as e:
        print(f"✗ AI search module import failed: {e}")
        return False
    
    try:
        # Initialize AI search
        result = initialize_ai_search()
        print(f"✓ AI search initialization: {result}")
    except Exception as e:
        print(f"✗ AI search initialization failed: {e}")
        return False
    
    try:
        # Test with sample documents
        test_documents = [
            {
                'file_path': 'test1.txt',
                'file_type': 'TXT',
                'content': 'This is a test document about artificial intelligence and machine learning.'
            },
            {
                'file_path': 'test2.txt', 
                'file_type': 'TXT',
                'content': 'Another document about data science and programming.'
            }
        ]
        
        # Add documents to index
        add_result = add_documents_to_ai_index(test_documents)
        print(f"✓ Adding documents to index: {add_result}")
        
        # Test search
        search_results = ai_search("artificial intelligence", n_results=5)
        print(f"✓ AI search returned {len(search_results)} results")
        
        # Get stats
        stats = get_ai_index_stats()
        print(f"✓ AI index stats: {stats}")
        
        # Clear index
        clear_result = clear_ai_index()
        print(f"✓ Clearing index: {clear_result}")
        
    except Exception as e:
        print(f"✗ AI search test failed: {e}")
        return False
    
    return True

def test_external_apis():
    """Test external API integrations"""
    print("\nTesting external API integrations...")
    
    # Test OpenAI
    try:
        import openai
        print("✓ OpenAI package imported")
    except ImportError:
        print("✗ OpenAI package not available")
    
    # Test Cohere
    try:
        import cohere
        print("✓ Cohere package imported")
    except ImportError:
        print("✗ Cohere package not available")

if __name__ == "__main__":
    print("=== AI Search Test Suite ===\n")
    
    # Test imports
    if not test_ai_imports():
        print("\n❌ AI imports failed. Please check your installation.")
        sys.exit(1)
    
    # Test AI search
    if not test_ai_search():
        print("\n❌ AI search functionality failed.")
        sys.exit(1)
    
    # Test external APIs
    test_external_apis()
    
    print("\n✅ All AI tests passed! AI embeddings should be working.")
    print("\nIf you're still having issues in the GUI, try:")
    print("1. Restart the application")
    print("2. Check if you have any files indexed")
    print("3. Try building the AI index first using the '🤖 Build AI' button")
