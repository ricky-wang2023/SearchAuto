#!/usr/bin/env python3
"""
Setup script for API keys
"""

import os
import json

def setup_api_keys():
    """Setup API keys for OpenAI and Cohere"""
    print("🔑 Setting up API keys for external AI services...")
    print("\nNote: You need API keys from:")
    print("- OpenAI: https://platform.openai.com/api-keys")
    print("- Cohere: https://dashboard.cohere.ai/api-keys")
    print("\nIf you don't have API keys, you can still use local AI search.")
    
    # Create .env file
    env_content = []
    
    # OpenAI API Key
    openai_key = input("\nEnter your OpenAI API key (or press Enter to skip): ").strip()
    if openai_key:
        env_content.append(f"OPENAI_API_KEY={openai_key}")
        print("✓ OpenAI API key set")
    else:
        print("⚠️  OpenAI API key not set - OpenAI features will be disabled")
    
    # Cohere API Key
    cohere_key = input("Enter your Cohere API key (or press Enter to skip): ").strip()
    if cohere_key:
        env_content.append(f"COHERE_API_KEY={cohere_key}")
        print("✓ Cohere API key set")
    else:
        print("⚠️  Cohere API key not set - Cohere features will be disabled")
    
    # Write .env file
    if env_content:
        with open(".env", "w") as f:
            f.write("\n".join(env_content))
        print("\n✅ API keys saved to .env file")
        print("The application will automatically load these keys on startup.")
    else:
        print("\n⚠️  No API keys provided")
        print("You can still use local AI search features.")
    
    print("\n📝 To use external AI services:")
    print("1. Get API keys from the respective platforms")
    print("2. Run this script again to set them up")
    print("3. Restart the SearchAuto application")

if __name__ == "__main__":
    setup_api_keys() 