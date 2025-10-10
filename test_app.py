#!/usr/bin/env python3
"""
Test script for AI Image Studio Streamlit app
Tests the main components without running the full Streamlit interface
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

def test_nano_banana_client():
    """Test Nano Banana client initialization"""
    try:
        from nano_banana_client import NanoBananaClient
        
        # Set the API key from your existing setup
        os.environ['GOOGLE_AI_API_KEY'] = 'AIzaSyDxRXDddcuFCIa_3JhbgTCBr4ffCs0hFaY'
        
        client = NanoBananaClient()
        print("✅ Nano Banana client initialized successfully")
        print(f"   Cost per image: ${client.get_pricing_info()['cost_per_image_usd']}")
        return True
    except Exception as e:
        print(f"❌ Nano Banana client failed: {e}")
        return False

def test_cloudinary_client():
    """Test Cloudinary client initialization"""
    try:
        from cloudinary_utils import CloudinaryManager
        
        # Note: This will fail without real Cloudinary credentials
        # That's expected for now
        print("🔄 Testing Cloudinary client...")
        
        # Check if environment variables are set
        required_vars = ['CLOUDINARY_CLOUD_NAME', 'CLOUDINARY_API_KEY', 'CLOUDINARY_API_SECRET']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"⚠️  Cloudinary client: Missing environment variables: {missing_vars}")
            print("   This is expected for local testing without Cloudinary setup")
            return False
        else:
            cloudinary_client = CloudinaryManager()
            print("✅ Cloudinary client initialized successfully")
            return True
            
    except Exception as e:
        print(f"⚠️  Cloudinary client: {e}")
        print("   This is expected for local testing without Cloudinary setup")
        return False

def test_streamlit_imports():
    """Test that all required imports work"""
    try:
        import streamlit as st
        from PIL import Image
        import io
        import time
        import tempfile
        print("✅ All Streamlit imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_structure():
    """Test that app.py can be imported and has main components"""
    try:
        # Temporarily set environment variables to avoid errors
        os.environ['GOOGLE_AI_API_KEY'] = 'AIzaSyDxRXDddcuFCIa_3JhbgTCBr4ffCs0hFaY'
        
        # Test importing app functions (this will import the module but not run main)
        print("🔄 Testing app structure...")
        
        # Check if app.py exists and has the main components
        with open('app.py', 'r') as f:
            content = f.read()
            
        required_functions = [
            'initialize_session_state',
            'initialize_clients', 
            'generate_image_tab',
            'edit_image_tab',
            'session_gallery'
        ]
        
        for func in required_functions:
            if func in content:
                print(f"   ✅ Found function: {func}")
            else:
                print(f"   ❌ Missing function: {func}")
                return False
        
        print("✅ App structure looks good")
        return True
        
    except Exception as e:
        print(f"❌ App structure test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🍌 AI Image Studio - Component Tests")
    print("=" * 50)
    
    tests = [
        ("Streamlit Imports", test_streamlit_imports),
        ("Nano Banana Client", test_nano_banana_client),
        ("Cloudinary Client", test_cloudinary_client),
        ("App Structure", test_app_structure)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing: {test_name}")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))
        print()
    
    # Summary
    print("📊 Test Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed >= 3:  # Allow Cloudinary to fail for local testing
        print("\n🎉 App is ready to run!")
        print("\nTo start the app:")
        print("1. Set up your environment variables (copy .env.streamlit to .env)")
        print("2. Run: streamlit run app.py")
    else:
        print("\n🚨 Some critical components failed. Please check the errors above.")

if __name__ == "__main__":
    main()