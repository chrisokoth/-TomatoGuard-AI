#!/usr/bin/env python3
"""
Health check script for Render deployment
"""

import os
import sys

def check_files():
    """Check if required files exist"""
    required_files = ['app.py', 'chatbot_local.py', 'tomato_model.keras']
    missing = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    return missing

def check_imports():
    """Check if imports work"""
    try:
        import streamlit
        import tensorflow as tf
        import numpy
        import PIL
        return True
    except ImportError as e:
        print(f"Import error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Health Check")
    print("=" * 30)
    
    # Check files
    missing = check_files()
    if missing:
        print(f"❌ Missing files: {missing}")
        sys.exit(1)
    else:
        print("✅ All files present")
    
    # Check imports
    if check_imports():
        print("✅ All imports working")
    else:
        print("❌ Import issues")
        sys.exit(1)
    
    print("✅ Health check passed!")
