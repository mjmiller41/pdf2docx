#!/usr/bin/env python3
"""
Test script for basic text extraction using our modern converter
"""

import fitz  # PyMuPDF
from converters.modern_pdf2docx_converter import ModernPDF2DOCXConverter

def test_basic_text_extraction():
    print("Testing basic text extraction...")
    converter = ModernPDF2DOCXConverter()
    
    # Create sample PDF in memory
    doc = fitz.open()
    page = doc.new_page()
    text = "Hello World! This is a basic text extraction test."
    page.insert_text((72, 72), text, fontsize=12)
    pdf_path = "samples/basic-text.pdf"
    doc.save(pdf_path)
    doc.close()
    print(f"Created sample PDF: {pdf_path}")
    
    # Convert sample PDF
    result = converter.convert_pdf_to_docx(
        pdf_path=pdf_path,
        output_path="output/basic-text-converted.docx"
    )
    
    if result['status'] == 'success':
        print("\n✅ Conversion successful!")
        print(f"Output: {result['output_path']}")
        print(f"Pages converted: {result['pages_converted']}")
        print(f"Stats: {result['stats']}")
        
        # Additional text extraction for verification
        from docx import Document
        doc = Document(result['output_path'])
        extracted_text = "\n".join([p.text for p in doc.paragraphs])
        
        print("\nExtracted text from DOCX:")
        print("=" * 50)
        print(extracted_text)
        print("=" * 50)
        
        # Save extracted text to file
        with open("output/basic-text-extracted.txt", "w") as f:
            f.write(extracted_text)
        print("\n✅ Extracted text saved to: output/basic-text-extracted.txt")
    else:
        print(f"\n❌ Conversion failed: {result['error']}")

if __name__ == "__main__":
    test_basic_text_extraction()
