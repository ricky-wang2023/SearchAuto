#!/usr/bin/env python3
"""
Test script to demonstrate embedding functionality
"""

import os

def test_embedding_functions():
    """Test the embedding build functions"""
    print("🧪 Testing embedding build functions...")
    
    # Test OpenAI embeddings
    print("\n1. Testing OpenAI embeddings...")
    try:
        from searchAuto import build_openai_embeddings
        result = build_openai_embeddings()
        print(f"OpenAI embedding result: {result}")
    except Exception as e:
        print(f"OpenAI embedding error: {e}")
    
    # Test Cohere embeddings
    print("\n2. Testing Cohere embeddings...")
    try:
        from searchAuto import build_cohere_embeddings
        result = build_cohere_embeddings()
        print(f"Cohere embedding result: {result}")
    except Exception as e:
        print(f"Cohere embedding error: {e}")
    
    # Check if .env file exists
    print("\n3. Checking environment setup...")
    if os.path.exists(".env"):
        print("✓ .env file found")
        with open(".env", "r") as f:
            content = f.read()
            if "OPENAI_API_KEY" in content:
                print("✓ OpenAI API key found in .env")
            else:
                print("✗ OpenAI API key not found in .env")
            if "COHERE_API_KEY" in content:
                print("✓ Cohere API key found in .env")
            else:
                print("✗ Cohere API key not found in .env")
    else:
        print("✗ .env file not found")
    
    print("\n📝 Summary:")
    print("- Embedding files are only created when API keys are available")
    print("- Without API keys, the functions return False and no files are created")
    print("- You can still use local AI search without external API keys")

if __name__ == "__main__":
    test_embedding_functions() 