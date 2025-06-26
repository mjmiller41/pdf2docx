#!/usr/bin/env python3
"""
Simple setup script for PDF to DOCX Converter
Uses user installation instead of virtual environment
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def install_dependencies():
    """Install dependencies using user installation"""
    print("📦 Installing dependencies (user installation)...")
    
    # Install Flask and werkzeug first
    success, output = run_command("python3 -m pip install flask werkzeug --user")
    if not success:
        print(f"❌ Failed to install Flask: {output}")
        return False
    
    print("✅ Flask and werkzeug installed")
    
    # Install remaining requirements
    success, output = run_command("python3 -m pip install -r requirements.txt --user")
    if success:
        print("✅ All dependencies installed successfully")
        return True
    else:
        print(f"❌ Failed to install some dependencies: {output}")
        return False

def test_installation():
    """Test if the installation works"""
    print("🧪 Testing installation...")
    
    test_script = '''
import sys
try:
    import fitz
    import pdf2docx
    import docx
    import flask
    import werkzeug
    print("✅ All core modules imported successfully")
    sys.exit(0)
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
'''
    
    success, output = run_command(f'python3 -c "{test_script}"')
    if success:
        print(output.strip())
        return True
    else:
        print(f"❌ Installation test failed: {output}")
        return False

def create_run_scripts():
    """Create convenient run scripts"""
    print("📝 Creating run scripts...")
    
    # CLI converter script
    cli_script = '''#!/bin/bash
# PDF to DOCX Converter - CLI Script

echo "🚀 PDF to DOCX Converter"
echo "Usage: ./run_cli.sh input.pdf output.docx [options]"
echo ""

if [ $# -lt 2 ]; then
    echo "❌ Error: Please provide input and output files"
    echo "Example: ./run_cli.sh input.pdf output.docx"
    exit 1
fi

python3 simple_pdf2docx_converter.py "$@"
'''
    
    with open("run_cli.sh", "w") as f:
        f.write(cli_script)
    os.chmod("run_cli.sh", 0o755)
    
    # Web interface script
    web_script = '''#!/bin/bash
# PDF to DOCX Converter - Web Interface Script

echo "🚀 Starting PDF to DOCX Converter Web Interface..."
echo "Open your browser and go to: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python3 web_interface.py
'''
    
    with open("run_web.sh", "w") as f:
        f.write(web_script)
    os.chmod("run_web.sh", 0o755)
    
    # Test script
    test_script = '''#!/bin/bash
# PDF to DOCX Converter - Test Script

echo "🧪 Running PDF to DOCX Converter tests..."
echo ""

python3 test_converter.py
'''
    
    with open("run_tests.sh", "w") as f:
        f.write(test_script)
    os.chmod("run_tests.sh", 0o755)
    
    print("✅ Run scripts created:")
    print("   - run_cli.sh (Command line converter)")
    print("   - run_web.sh (Web interface)")
    print("   - run_tests.sh (Test suite)")

def main():
    """Main setup function"""
    print("🚀 PDF to DOCX Converter Simple Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️  Some dependencies failed to install.")
        print("You may need to install them manually:")
        print("  python3 -m pip install flask werkzeug --user")
        print("  python3 -m pip install -r requirements.txt --user")
    
    # Test installation
    if not test_installation():
        print("\n⚠️  Installation test failed.")
        print("Please check the error messages above.")
    
    # Create run scripts
    create_run_scripts()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    print("\n📖 Quick start:")
    print("1. Test the installation:")
    print("   ./run_tests.sh")
    print("\n2. Convert a PDF:")
    print("   ./run_cli.sh input.pdf output.docx")
    print("\n3. Use web interface:")
    print("   ./run_web.sh")
    print("\n4. Manual commands:")
    print("   python3 simple_pdf2docx_converter.py input.pdf output.docx")
    print("   python3 web_interface.py")

if __name__ == "__main__":
    main()
