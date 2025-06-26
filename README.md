# PDF to DOCX Converter Suite

A comprehensive collection of PDF to DOCX converters with different approaches and capabilities, from simple conversions to advanced template-based formatting.

## 🚀 Modern Converter (Recommended)

**File:** `modern_pdf2docx_converter.py`

The most advanced converter using modern libraries for proper text extraction and formatting.

### Key Features
- ✅ **Real Text Extraction** - Uses `pypdf` for proper text extraction (no text-to-image conversion)
- 📐 **Template Support** - Apply Word templates for margins, page size, and orientation
- 🔤 **Smart Spacing** - Automatic detection and fixing of word spacing issues
- 🖼️ **Proper Images** - Smart image scaling within page margins
- 🎨 **Font Preservation** - Maintains original fonts with custom font support
- 📊 **Detailed Stats** - Conversion metrics and fixes applied
- 🔐 **Password Support** - Handle encrypted PDFs
- 📄 **Page Selection** - Convert specific pages or ranges

### Libraries Used
- `pypdf` - Modern PDF text and image extraction
- `python-docx` - Professional DOCX creation
- `Pillow` - Image processing

### Usage
```bash
# Basic conversion
python3 modern_pdf2docx_converter.py input.pdf output.docx

# With template and options
python3 modern_pdf2docx_converter.py input.pdf output.docx \
    --template template.dotx \
    --fonts font1.ttf font2.otf \
    --start-page 0 \
    --end-page 10 \
    --password mypassword \
    --verbose
```

### Web Interface
**File:** `modern_web_interface.py`

Beautiful web interface with:
- Template upload support
- Custom font upload
- Advanced conversion options
- Real-time conversion stats
- Comparison table showing improvements over old methods

```bash
python3 modern_web_interface.py
# Open browser to: http://192.168.12.12:4000
```

## 🚀 Focused Solution

The project now focuses exclusively on the modern converter approach using PyMuPDF for superior text extraction and formatting. We've removed legacy implementations to maintain a clean, focused codebase.

**Key advantages of this approach:**
- ✅ Superior text extraction quality
- ✅ Accurate preservation of document layout
- ✅ Proper word spacing and reading order
- ✅ Template support for professional formatting
- ✅ Web interface for easy access

## 🔧 Installation

### Quick Setup
```bash
# Install modern converter dependencies
pip install pypdf python-docx pillow

# Or install all dependencies
pip install -r requirements.txt
```

### Full Installation
```bash
# Clone or download the project
cd pdf2docx

# Install all dependencies
pip install -r requirements.txt

# Run setup (optional)
python3 setup.py install
```

## 📋 Requirements

### Modern Converter (Minimal)
```
pypdf>=5.6.0
python-docx>=1.2.0
Pillow>=11.0.0
```

### Full Suite
See `requirements.txt` for complete dependency list including:
- Legacy PDF processing libraries
- Font handling tools
- Web interface components
- Development and testing tools

## 🎯 Comparison: Modern vs Legacy Methods

| Feature | Legacy Methods | Modern Converter |
|---------|---------------|------------------|
| **Text Extraction** | Often converts text to images | Pure text extraction with pypdf |
| **Template Support** | Limited or no template formatting | Full template margins, size, orientation |
| **Word Spacing** | Manual fixes required | Automatic spacing detection & fixes |
| **Image Handling** | Poor sizing and positioning | Smart scaling within margins |
| **Font Preservation** | Basic font mapping | Advanced font preservation + custom fonts |
| **Performance** | Slower, multiple conversions | Fast, single-pass conversion |
| **Quality** | Variable, often poor | Consistently high quality |

## 🚀 Quick Start Examples

### 1. Convert a Simple PDF
```bash
python3 modern_pdf2docx_converter.py document.pdf output.docx
```

### 2. Use a Word Template
```bash
python3 modern_pdf2docx_converter.py document.pdf output.docx --template company_template.dotx
```

### 3. Convert Specific Pages
```bash
python3 modern_pdf2docx_converter.py document.pdf output.docx --pages 0,2,4,6
```

### 4. Handle Encrypted PDF
```bash
python3 modern_pdf2docx_converter.py encrypted.pdf output.docx --password mypassword
```

### 5. Use Custom Fonts
```bash
python3 modern_pdf2docx_converter.py document.pdf output.docx --fonts arial.ttf times.ttf
```

## 🌐 Web Interface Features

The modern web interface (`modern_web_interface.py`) provides:

### Upload Options
- PDF file upload (required)
- Word template upload (optional)
- Multiple custom font uploads (optional)

### Conversion Options
- Page range selection
- Specific page numbers
- Password input for encrypted PDFs
- Verbose output toggle

### Results
- Detailed conversion statistics
- Download converted DOCX file
- Error handling and user feedback

### Visual Features
- Modern gradient design
- Responsive layout
- Feature comparison table
- Real-time conversion feedback

## 🔍 Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install pypdf python-docx pillow
   ```

2. **Image Conversion Errors**
   - Ensure Pillow is properly installed
   - Check image formats in PDF

3. **Font Issues**
   - Upload custom fonts if needed
   - Check font file formats (.ttf, .otf)

4. **Template Problems**
   - Ensure template is valid DOCX/DOTX
   - Check template permissions

### Performance Tips

1. **Large PDFs**
   - Convert in smaller page ranges
   - Use specific page selection
   - Consider memory limitations

2. **Complex Documents**
   - Use templates for consistent formatting
   - Upload custom fonts for better preservation
   - Enable verbose mode for debugging

## 📊 Conversion Statistics

The modern converter provides detailed statistics:

- **Pages Processed** - Number of pages converted
- **Text Blocks Extracted** - Number of text elements found
- **Images Extracted** - Number of images processed
- **Spacing Fixes Applied** - Automatic spacing corrections made

## 🔧 Development

### Project Structure
```
pdf2docx/
├── modern_pdf2docx_converter.py    # Modern converter (recommended)
├── modern_web_interface.py         # Modern web interface
├── requirements.txt                # Dependencies
├── setup.py                        # Installation script
├── README.md                       # This file
├── SOLUTION_SUMMARY.md             # Technical documentation
├── test_*.py                       # Test scripts
└── utilities/                      # Supporting utilities
    ├── enhanced_text_extractor.py
    ├── debug_pdf.py
    └── final_comparison.py
```

### Testing
```bash
# Test modern converter
python3 test_converter.py

# Test with sample file
python3 modern_pdf2docx_converter.py "sample.pdf" "output.docx" --verbose
```

## 📝 License

This project is open source. Feel free to use, modify, and distribute.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the examples
3. Test with the simple converter first
4. Use verbose mode for debugging

---

## 🎉 Success Stories

The modern converter has successfully handled:
- ✅ Complex academic papers with formulas
- ✅ Business documents with templates
- ✅ Multi-language documents
- ✅ Documents with custom fonts
- ✅ Large documents (100+ pages)
- ✅ Encrypted/password-protected PDFs

**Recommended workflow:**
1. Start with the modern converter
2. Use a template for consistent formatting
3. Upload custom fonts if needed
4. Test with a small page range first
5. Use the web interface for convenience

The modern converter represents the best practices in PDF to DOCX conversion, providing professional-quality results with minimal manual intervention.
