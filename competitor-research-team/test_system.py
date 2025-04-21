"""
Test script to verify the Competitive Analysis system setup.

This script tests:
1. API key configuration
2. Directory structure
3. Module imports
"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv

def test_environment():
    """Test environment configuration"""
    print("Testing environment setup...")
    
    # Load environment variables
    load_dotenv()
    
    # Check OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found. Please set it in the .env file.")
        return False
    else:
        print("✅ OPENAI_API_KEY found.")
    
    return True

def test_directory_structure():
    """Test directory structure"""
    print("\nTesting directory structure...")
    
    # Check core directories
    core_dirs = [
        "data",
        "data/raw",
        "data/raw/competitors",
        "data/raw/competitors/primary",
        "data/raw/competitors/adjacent",
        "data/raw/industry",
        "data/processed",
        "data/processed/competitors",
        "data/processed/competitors/primary",
        "data/processed/competitors/adjacent",
        "data/processed/industry",
        "data/analysis",
        "data/analysis/excel",
        "data/analysis/reports",
        "data/analysis/visualizations"
    ]
    
    all_good = True
    for dir_path in core_dirs:
        path = Path(dir_path)
        if not path.exists():
            print(f"❌ Directory not found: {dir_path}")
            all_good = False
        else:
            print(f"✅ Directory found: {dir_path}")
    
    return all_good

def test_imports():
    """Test module imports"""
    print("\nTesting module imports...")
    
    all_good = True
    
    # Test importing tools
    try:
        from src.tools import pdf_extractor, web_scraper, excel_generator, visualization
        print("✅ Successfully imported tool modules.")
    except ImportError as e:
        print(f"❌ Error importing tool modules: {str(e)}")
        all_good = False
    
    # Test importing analysis
    try:
        from src.analysis import competitive_analyst
        print("✅ Successfully imported analysis modules.")
    except ImportError as e:
        print(f"❌ Error importing analysis modules: {str(e)}")
        all_good = False
    
    # Test importing UI
    try:
        from src.ui import cli
        print("✅ Successfully imported UI modules.")
    except ImportError as e:
        print(f"❌ Error importing UI modules: {str(e)}")
        all_good = False
    
    return all_good

def test_openai_connection():
    """Test connection to OpenAI API"""
    print("\nTesting OpenAI API connection...")
    
    try:
        import openai
        from config import OPENAI_API_KEY
        
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Connection successful' if you can hear me."}
            ],
            max_tokens=20
        )
        
        result = response.choices[0].message.content
        if "Connection successful" in result:
            print(f"✅ OpenAI API connection successful.")
            return True
        else:
            print(f"⚠️ OpenAI API connection may have issues. Unexpected response.")
            return False
        
    except Exception as e:
        print(f"❌ Error connecting to OpenAI API: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("Running system tests for Constructiv AI Competitive Analysis Tool\n")
    
    env_ok = test_environment()
    dirs_ok = test_directory_structure()
    imports_ok = test_imports()
    
    # Only test API connection if environment is configured
    api_ok = test_openai_connection() if env_ok else False
    
    # Overall status
    print("\n" + "="*50)
    if env_ok and dirs_ok and imports_ok and api_ok:
        print("🎉 All tests passed! The system is ready to use.")
    else:
        print("⚠️ Some tests failed. Please fix the issues before using the system.")
    
    print("="*50)

if __name__ == "__main__":
    main() 