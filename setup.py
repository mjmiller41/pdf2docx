#!/usr/bin/env python3
"""
Setup script for PDF to DOCX Converter

This script creates a virtual environment and installs all dependencies.
"""

import os
import sys
import subprocess
import venv
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True, 
                              capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def create_virtual_environment():
    """Create a Python virtual environment"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("📁 Virtual environment already exists")
        return True
    
    print("🔧 Creating virtual environment...")
    try:
        venv.create("venv", with_pip=True)
        print("✅ Virtual environment created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def get_pip_command():
    """Get the correct pip command for the virtual environment"""
    if os.name == 'nt':  # Windows
        return "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        return "venv/bin/pip"

def get_python_command():
    """Get the correct python command for the virtual environment"""
    if os.name == 'nt':  # Windows
        return "venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        return "venv/bin/python"

def install_dependencies():
    """Install all required dependencies"""
    print("📦 Installing dependencies...")
    
    pip_cmd = get_pip_command()
    
    # Upgrade pip first
    success, output = run_command(f"{pip_cmd} install --upgrade pip")
    if not success:
        print(f"⚠️  Warning: Could not upgrade pip: {output}")
    
    # Install requirements
    success, output = run_command(f"{pip_cmd} install -r requirements.txt")
    if success:
        print("✅ Dependencies installed successfully")
        return True
    else:
        print(f"❌ Failed to install dependencies: {output}")
        return False

def test_installation():
    """Test if the installation works"""
    print("🧪 Testing installation...")
    
    python_cmd = get_python_command()
    
    # Test basic imports
    test_script = '''
import sys
try:
    import fitz
    import pdf2docx
    import docx
    import flask
    print("✅ All core modules imported successfully")
    sys.exit(0)
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
'''
    
    success, output = run_command(f'{python_cmd} -c "{test_script}"')
    if success:
        print(output.strip())
        return True
    else:
        print(f"❌ Installation test failed: {output}")
        return False

def create_activation_scripts():
    """Create convenient activation scripts"""
    print("📝 Creating activation scripts...")
    
    # Unix/Linux/macOS activation script
    activate_script = '''#!/bin/bash
# PDF to DOCX Converter - Activation Script

echo "🚀 Activating PDF to DOCX Converter environment..."

# Activate virtual environment
source venv/bin/activate

echo "✅ Environment activated!"
echo ""
echo "📖 Available commands:"
echo "  python simple_pdf2docx_converter.py input.pdf output.docx"
echo "  python web_interface.py  # Start web interface"
echo "  python test_converter.py  # Run tests"
echo ""
echo "🔚 To deactivate, run: deactivate"
'''
    
    with open("activate.sh", "w") as f:
        f.write(activate_script)
    
    # Make it executable
    os.chmod("activate.sh", 0o755)
    
    # Windows activation script
    windows_script = '''@echo off
REM PDF to DOCX Converter - Activation Script

echo 🚀 Activating PDF to DOCX Converter environment...

REM Activate virtual environment
call venv\\Scripts\\activate.bat

echo ✅ Environment activated!
echo.
echo 📖 Available commands:
echo   python simple_pdf2docx_converter.py input.pdf output.docx
echo   python web_interface.py  # Start web interface
echo   python test_converter.py  # Run tests
echo.
echo 🔚 To deactivate, run: deactivate
'''
    
    with open("activate.bat", "w") as f:
        f.write(windows_script)
    
    print("✅ Activation scripts created:")
    print("   - activate.sh (Unix/Linux/macOS)")
    print("   - activate.bat (Windows)")

def main():
    """Main setup function"""
    print("🚀 PDF to DOCX Converter Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        sys.exit(1)
    
    # Create activation scripts
    create_activation_scripts()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📖 Next steps:")
    print("1. Activate the environment:")
    if os.name == 'nt':
        print("   activate.bat")
    else:
        print("   source activate.sh")
    print("\n2. Test the converter:")
    print("   python test_converter.py")
    print("\n3. Start converting:")
    print("   python simple_pdf2docx_converter.py input.pdf output.docx")
    print("   python web_interface.py  # For web interface")

if __name__ == "__main__":
    main()
