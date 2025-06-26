#!/bin/bash
# PDF to DOCX Converter - Test Script

echo "🧪 Running PDF to DOCX Converter tests..."
echo ""

# Test modern PDF to DOCX converter
python3 test_basic_text_extraction.py
python3 test_final_extraction.py
python3 test_multipage.py

# Test extraction methods
python3 enhanced_text_extractor.py "first_hundred/the first hundred years Book pg 1-10.pdf" --compare

# Final comparison
python3 final_comparison.py
