#!/usr/bin/env python3
"""
Quick Setup Script for NotebookLM-Style RAG System
Run this first to set up the environment
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check Python version (3.8+)"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_env_file():
    """Check if .env file exists"""
    if Path(".env").exists():
        print("✅ .env file found")
        return True
    else:
        print("⚠️ .env file not found")
        print("   Creating from template...")
        if Path(".env.example").exists():
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ .env created from .env.example")
            print("   ⚠️ IMPORTANT: Edit .env and add your GROQ_API_KEY")
            return False
        return False

def check_requirements():
    """Check if requirements are installed"""
    try:
        import streamlit
        import groq
        import PyPDF2
        import docx
        import numpy
        print("✅ All requirements installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("   Run: pip install -r requirements.txt")
        return False

def main():
    print("\n" + "="*50)
    print("🚀 NotebookLM RAG System - Setup Check")
    print("="*50 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment File", check_env_file),
        ("Dependencies", check_requirements),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        results.append(check_func())
    
    print("\n" + "="*50)
    
    if all(results):
        print("✅ Setup Complete! Ready to run.")
        print("\nStart the app with:")
        print("  streamlit run app.py")
    else:
        print("⚠️ Setup incomplete. Please fix issues above.")
        print("\nTo install dependencies:")
        print("  pip install -r requirements.txt")
        print("\nTo set up .env:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your GROQ_API_KEY")
        print("  3. Save and run: streamlit run app.py")
    
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
