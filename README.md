# PDF to DOCX Converter Suite

A comprehensive solution for converting PDF files to DOCX format with proper text extraction, layout preservation, and formatting.

## Features

- **Modern Conversion Engine**: Uses PyMuPDF for superior text extraction
- **Layout Preservation**: Maintains original document structure and formatting
- **Template Support**: Apply custom DOCX templates for consistent styling
- **Multi-page Processing**: Handles documents of any length
- **Web Interface**: User-friendly web UI for easy conversions
- **Comparison Tools**: Validate conversion quality against original PDFs

## Key Components

### Converters
- `modern_pdf2docx_converter.py` - Main modern converter (recommended)
- `advanced_pdf2docx_converter.py` - Advanced converter with OCR support
- `simple_pdf2docx_converter.py` - Basic converter for simple documents
- `pdf2docx_converter.py` - Legacy converter for reference

### Core Functionality
- `core/pdf_extraction.py` - Core PDF text extraction logic
- `enhanced_text_extractor.py` - Multi-method text extraction tester
- `pdf_docx_comparator.py` - PDF/DOCX comparison tool

### Web Interface
- `web_interface.py` - Flask-based web application
- `templates/` - HTML templates for web UI

### Testing
- `test_final_extraction.py` - Text extraction tests
- `test_multipage.py` - Multi-page processing tests
- `test_converter.py` - Converter functionality tests
- `final_comparison.py` - Before/after comparison tool

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/pdf2docx.git
cd pdf2docx

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Command Line
```bash
# Basic conversion
python modern_pdf2docx_converter.py input.pdf output.docx

# With template and custom fonts
python modern_pdf2docx_converter.py input.pdf output.docx \
  --template template.dotx \
  --fonts font1.ttf font2.otf
```

### Web Interface
```bash
python web_interface.py
# Access at http://localhost:4000
```

## Documentation
- [Solution Summary](SOLUTION_SUMMARY.md)
- [Technical Implementation Details](PROJECT_SUMMARY.md)

## License
MIT License - see [LICENSE](LICENSE) for details
