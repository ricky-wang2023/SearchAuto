#!/usr/bin/env python3
"""
Lightweight AI Search Module for SearchAuto
Handles batch size issues and threading better
"""

import os
import json
import threading
from typing import List, Dict, Any, Optional
from pathlib import Path

# Global variables for AI search
ai_initialized = False
ai_models_loaded = False
ai_search_engine = None
ai_lock = threading.Lock()

def check_ai_dependencies():
    """Check if AI dependencies are available"""
    try:
        import sentence_transformers
        import chromadb
        import torch
        return True
    except ImportError:
        return False

def initialize_ai_search():
    """Initialize AI search engine with better error handling"""
    global ai_initialized, ai_search_engine
    
    with ai_lock:
        if ai_initialized:
            return True
            
        try:
            if not check_ai_dependencies():
                print("AI dependencies not available. Install with: pip install sentence-transformers chromadb torch")
                return False
            
            # Import AI modules
            from ai_search import AISearchEngine
            
            print("Loading AI model...")
            ai_search_engine = AISearchEngine()
            
            if ai_search_engine.initialize():
                ai_initialized = True
                print("AI Search Engine initialized successfully!")
                return True
            else:
                print("Failed to initialize AI search engine")
                return False
                
        except Exception as e:
            print(f"Error initializing AI search: {e}")
            return False

def add_documents_to_ai_index(documents: List[Dict[str, Any]]) -> bool:
    """Add documents to AI index with better batch handling"""
    global ai_search_engine
    
    if not ai_initialized:
        if not initialize_ai_search():
            return False
    
    try:
        # Process documents in smaller batches
        batch_size = 50  # Very small batches to avoid memory issues
        total_added = 0
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            
            try:
                success = ai_search_engine.add_documents(batch)
                if success:
                    total_added += len(batch)
                    print(f"Added batch {i//batch_size + 1}/{len(documents)//batch_size + 1} ({len(batch)} documents)")
                else:
                    print(f"Failed to add batch {i//batch_size + 1}")
                    
            except Exception as e:
                print(f"Error adding batch {i//batch_size + 1}: {e}")
                continue
        
        print(f"Successfully added {total_added}/{len(documents)} documents to AI index")
        return total_added > 0
        
    except Exception as e:
        print(f"Error adding documents to AI index: {e}")
        return False

def search_ai_index(query: str, top_k: int = 10) -> List[Dict[str, Any]]:
    """Search AI index with error handling"""
    global ai_search_engine
    
    if not ai_initialized:
        if not initialize_ai_search():
            return []
    
    try:
        results = ai_search_engine.search(query, top_k=top_k)
        return results
    except Exception as e:
        print(f"Error searching AI index: {e}")
        return []

def get_ai_index_stats() -> Dict[str, Any]:
    """Get AI index statistics"""
    global ai_search_engine
    
    if not ai_initialized or not ai_search_engine:
        return {'total_documents': 0, 'index_size': '0 MB'}
    
    try:
        stats = ai_search_engine.get_stats()
        return stats
    except Exception as e:
        print(f"Error getting AI index stats: {e}")
        return {'total_documents': 0, 'index_size': '0 MB'}

def clear_ai_index():
    """Clear AI index"""
    global ai_search_engine, ai_initialized
    
    if not ai_initialized or not ai_search_engine:
        return False
    
    try:
        success = ai_search_engine.clear_index()
        if success:
            print("AI index cleared successfully")
        return success
    except Exception as e:
        print(f"Error clearing AI index: {e}")
        return False

def summarize_text(text: str, max_length: int = 150) -> str:
    """Summarize text with error handling"""
    global ai_search_engine
    
    if not ai_initialized:
        if not initialize_ai_search():
            return text[:max_length] + "..." if len(text) > max_length else text
    
    try:
        summary = ai_search_engine.summarize_text(text, max_length=max_length)
        return summary
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return text[:max_length] + "..." if len(text) > max_length else text

def is_ai_available() -> bool:
    """Check if AI features are available"""
    return check_ai_dependencies()

def get_ai_status() -> str:
    """Get AI status message"""
    if not check_ai_dependencies():
        return "AI dependencies not available"
    elif not ai_initialized:
        return "AI not initialized"
    else:
        return "AI ready" 