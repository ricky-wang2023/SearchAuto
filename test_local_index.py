#!/usr/bin/env python3
"""
Test script for local index functionality
"""

import sqlite3
import os

def test_local_index():
    """Test local index functionality"""
    print("🧪 Testing local index functionality...")
    
    # Check if database exists
    if not os.path.exists('file_index.db'):
        print("✗ file_index.db not found")
        return False
    
    # Check database structure
    try:
        conn = sqlite3.connect('file_index.db')
        c = conn.cursor()
        
        # Check if tables exist
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in c.fetchall()]
        print(f"✓ Database tables: {tables}")
        
        # Check roots
        c.execute('SELECT root_path FROM roots')
        roots = [row[0] for row in c.fetchall()]
        print(f"✓ Indexed roots: {roots}")
        
        # Check indexed files
        c.execute('SELECT COUNT(*) FROM file_index')
        file_count = c.fetchone()[0]
        print(f"✓ Files in index: {file_count}")
        
        # Check file types
        c.execute('SELECT file_type, COUNT(*) FROM file_index GROUP BY file_type')
        file_types = c.fetchall()
        print(f"✓ File types: {file_types}")
        
        # Test a simple search
        c.execute("SELECT file_path, snippet(file_index, 3, '[', ']', '...', 20) FROM file_index WHERE content MATCH 'test' LIMIT 3")
        search_results = c.fetchall()
        print(f"✓ Search results for 'test': {len(search_results)}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def test_search_functions():
    """Test search functions"""
    print("\n🔍 Testing search functions...")
    
    try:
        from searchAuto import search_index, get_roots, get_selected_roots
        
        # Test getting roots
        roots = get_roots()
        print(f"✓ Roots from function: {roots}")
        
        # Test search
        results = search_index('test')
        print(f"✓ Search results: {len(results)}")
        
        if results:
            print("Sample results:")
            for i, result in enumerate(results[:2]):
                print(f"  {i+1}. {result.get('File Path', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"✗ Search function error: {e}")
        return False

if __name__ == "__main__":
    print("=== Local Index Test Suite ===\n")
    
    # Test database
    if not test_local_index():
        print("\n❌ Local index database issues found.")
        exit(1)
    
    # Test search functions
    if not test_search_functions():
        print("\n❌ Search function issues found.")
        exit(1)
    
    print("\n✅ Local index appears to be working correctly!")
    print("\nIf you're having issues in the GUI, try:")
    print("1. Restart the application")
    print("2. Make sure you have files selected in the roots list")
    print("3. Try different search terms")
    print("4. Check if the search results are being displayed properly") 