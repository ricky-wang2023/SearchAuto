#!/usr/bin/env python3
"""
Script to clear all SearchAuto data files
"""

import os
import shutil
import sqlite3
from pathlib import Path

def clear_all_data():
    """Clear all SearchAuto data files"""
    print("🧹 Clearing all SearchAuto data files...")
    
    files_to_remove = [
        # Database files
        "file_index.db",
        "ai_search_db",
        
        # Embedding files
        "embeddings_openai.json",
        "embeddings_cohere.json",
        
        # Test databases
        "test_ai_db",
        "test_db",
        "test_exe_db",
        
        # Progress and config files
        "file_monitor_progress.json",
        "file_monitor_config.json",
        
        # Translation history files
        "translation_history.json",
        "translation_history.json.backup",
        "translation_history.json.repair_backup",
        
        # App settings
        "app_settings.json",
        "api_keys.json"
    ]
    
    removed_count = 0
    
    for file_path in files_to_remove:
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"✓ Removed file: {file_path}")
                removed_count += 1
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"✓ Removed directory: {file_path}")
                removed_count += 1
        except Exception as e:
            print(f"✗ Failed to remove {file_path}: {e}")
    
    # Also clear any ChromaDB collections if they exist
    try:
        if os.path.exists("ai_search_db"):
            # Try to connect and clear collections
            import chromadb
            client = chromadb.PersistentClient(path="ai_search_db")
            collections = client.list_collections()
            for collection in collections:
                try:
                    client.delete_collection(collection.name)
                    print(f"✓ Cleared ChromaDB collection: {collection.name}")
                except:
                    pass
    except Exception as e:
        print(f"Note: Could not clear ChromaDB collections: {e}")
    
    print(f"\n✅ Cleared {removed_count} files/directories")
    print("\nAll SearchAuto data has been cleared!")
    print("You can now start fresh with a clean installation.")

if __name__ == "__main__":
    # Ask for confirmation
    response = input("⚠️  This will delete ALL SearchAuto data files. Continue? (y/N): ")
    if response.lower() in ['y', 'yes']:
        clear_all_data()
    else:
        print("Operation cancelled.") 