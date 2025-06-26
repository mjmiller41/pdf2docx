#!/bin/bash
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
