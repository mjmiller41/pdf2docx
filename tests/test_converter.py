#!/usr/bin/env python3
"""
Test script for PDF to DOCX converter
"""

import os
import sys
from pathlib import Path
from pdf2docx import parse

def test_basic_conversion():
    """Test basic PDF to DOCX conversion"""
    print("🧪 Testing basic PDF to DOCX conversion...")
    
    input_pdf = "first_hundred/the first hundred years Book pg 1-10.pdf"
    output_docx = "output/test_basic.docx"
    
    if not Path(input_pdf).exists():
        print(f"❌ Test PDF not found: {input_pdf}")
        return False
    
    try:
        # Create output directory
        Path("output").mkdir(exist_ok=True)
        
        # Convert using pdf2docx directly
        parse(input_pdf, output_docx)
        
        if Path(output_docx).exists():
            file_size = Path(output_docx).stat().st_size
            print(f"✅ Basic conversion successful!")
            print(f"   Output: {output_docx}")
            print(f"   Size: {file_size / 1024 / 1024:.1f} MB")
            return True
        else:
            print(f"❌ Output file not created: {output_docx}")
            return False
            
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return False

def test_cli_converter():
    """Test the CLI converter"""
    print("\n🧪 Testing CLI converter...")
    
    cmd = 'python3 simple_pdf2docx_converter.py "first_hundred/the first hundred years Book pg 1-10.pdf" "output/test_cli.docx" --fonts "first_hundred/amazon_endure_font"'
    
    try:
        result = os.system(cmd)
        if result == 0:
            print("✅ CLI converter executed successfully!")
            return True
        else:
            print(f"❌ CLI converter failed with exit code: {result}")
            return False
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    required_modules = [
        'fitz',  # PyMuPDF
        'pdf2docx',
        'docx',  # python-docx
        'cv2',   # opencv-python-headless
        'PIL',   # Pillow
        'click',
        'rich',
        'numpy'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module} - MISSING")
            missing.append(module)
    
    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies available!")
        return True

def main():
    """Run all tests"""
    print("🚀 PDF to DOCX Converter Test Suite")
    print("=" * 50)
    
    # Check dependencies first
    deps_ok = check_dependencies()
    if not deps_ok:
        print("\n❌ Cannot proceed without required dependencies")
        sys.exit(1)
    
    # Test basic conversion
    basic_ok = test_basic_conversion()
    
    # Test CLI converter
    cli_ok = test_cli_converter()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"   Dependencies: {'✅ PASS' if deps_ok else '❌ FAIL'}")
    print(f"   Basic Conversion: {'✅ PASS' if basic_ok else '❌ FAIL'}")
    print(f"   CLI Converter: {'✅ PASS' if cli_ok else '❌ FAIL'}")
    
    if all([deps_ok, basic_ok]):
        print("\n🎉 Core functionality is working!")
        print("   You can now use the converter for PDF to DOCX conversion.")
        print("\n📖 Usage examples:")
        print("   python3 simple_pdf2docx_converter.py input.pdf output.docx")
        print("   python3 web_interface.py  # Start web interface")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
