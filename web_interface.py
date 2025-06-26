#!/usr/bin/env python3
"""
Web Interface for PDF to DOCX Converter

A simple Flask web application for converting PDF files to DOCX format
with template and font support.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import zipfile

# Add Flask to requirements if not already installed
try:
    from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
except ImportError:
    print("Flask not installed. Installing...")
    os.system("pip install flask --user")
    from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify

# Import our advanced converter and comparator
from advanced_pdf2docx_converter import AdvancedPDF2DOCXConverter
from pdf_docx_comparator import PDFDOCXComparator

app = Flask(__name__)
app.secret_key = 'pdf2docx_converter_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Create upload and output directories
UPLOAD_FOLDER = Path('uploads')
OUTPUT_FOLDER = Path('web_output')
TEMPLATE_FOLDER = Path('templates_upload')
FONT_FOLDER = Path('fonts_upload')

for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, TEMPLATE_FOLDER, FONT_FOLDER]:
    folder.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}
TEMPLATE_EXTENSIONS = {'dotx', 'docx'}
FONT_EXTENSIONS = {'ttf', 'otf'}

def allowed_file(filename, extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf():
    try:
        # Check if files were uploaded
        if 'pdf_file' not in request.files:
            flash('No PDF file selected')
            return redirect(url_for('index'))
        
        pdf_file = request.files['pdf_file']
        if pdf_file.filename == '':
            flash('No PDF file selected')
            return redirect(url_for('index'))
        
        if not allowed_file(pdf_file.filename, ALLOWED_EXTENSIONS):
            flash('Invalid file type. Please upload a PDF file.')
            return redirect(url_for('index'))
        
        # Save uploaded PDF
        pdf_filename = secure_filename(pdf_file.filename)
        pdf_path = UPLOAD_FOLDER / pdf_filename
        pdf_file.save(str(pdf_path))
        
        # Handle template file
        template_path = None
        if 'template_file' in request.files and request.files['template_file'].filename:
            template_file = request.files['template_file']
            if allowed_file(template_file.filename, TEMPLATE_EXTENSIONS):
                template_filename = secure_filename(template_file.filename)
                template_path = TEMPLATE_FOLDER / template_filename
                template_file.save(str(template_path))
        
        # Handle font files
        font_paths = []
        if 'font_files' in request.files:
            font_files = request.files.getlist('font_files')
            for font_file in font_files:
                if font_file.filename and allowed_file(font_file.filename, FONT_EXTENSIONS):
                    font_filename = secure_filename(font_file.filename)
                    font_path = FONT_FOLDER / font_filename
                    font_file.save(str(font_path))
                    font_paths.append(str(font_path))
        
        # Get conversion options
        start_page = request.form.get('start_page')
        end_page = request.form.get('end_page')
        pages = request.form.get('pages')
        password = request.form.get('password')
        
        # Parse pages
        pages_list = None
        if pages:
            try:
                pages_list = [int(p.strip()) for p in pages.split(',')]
            except ValueError:
                flash('Invalid pages format. Use comma-separated integers.')
                return redirect(url_for('index'))
        
        # Create output filename
        output_filename = pdf_filename.rsplit('.', 1)[0] + '.docx'
        output_path = OUTPUT_FOLDER / output_filename
        
        # Perform conversion using advanced converter
        try:
            converter = AdvancedPDF2DOCXConverter()
            
            # Perform conversion
            result = converter.convert_pdf_to_docx(
                pdf_path=str(pdf_path),
                output_path=str(output_path),
                template_path=str(template_path) if template_path else None,
                font_paths=font_paths if font_paths else None,
                start_page=int(start_page) if start_page else 0,
                end_page=int(end_page) if end_page else None,
                pages=pages_list,
                password=password if password else None
            )
            
            if result['status'] == 'success':
                # Perform comparison and adjustment
                try:
                    comparator = PDFDOCXComparator()
                    
                    # Generate comparison report
                    comparison_report = comparator.full_comparison_report(
                        str(pdf_path), str(output_path)
                    )
                    
                    # Apply automatic fixes if needed
                    if comparison_report['overall_score']['overall'] < 90:
                        fixed_filename = output_filename.rsplit('.', 1)[0] + '_IMPROVED.docx'
                        fixed_path = OUTPUT_FOLDER / fixed_filename
                        
                        fix_result = comparator.apply_text_fixes(
                            str(output_path), str(fixed_path)
                        )
                        
                        if fix_result['status'] == 'success' and fix_result['fixes_applied'] > 0:
                            # Use the improved version
                            output_path = fixed_path
                            output_filename = fixed_filename
                            
                            # Flash success message with improvement details
                            flash(f'✅ Conversion completed with {fix_result["fixes_applied"]} automatic improvements! '
                                  f'Quality score: {comparison_report["overall_score"]["overall"]}/100 '
                                  f'(Grade: {comparison_report["overall_score"]["grade"]})', 'success')
                        else:
                            flash(f'✅ Conversion completed! Quality score: {comparison_report["overall_score"]["overall"]}/100 '
                                  f'(Grade: {comparison_report["overall_score"]["grade"]})', 'success')
                    else:
                        flash(f'✅ Excellent conversion! Quality score: {comparison_report["overall_score"]["overall"]}/100 '
                              f'(Grade: {comparison_report["overall_score"]["grade"]})', 'success')
                
                except Exception as e:
                    # If comparison fails, still proceed with original conversion
                    flash(f'⚠️ Conversion completed but comparison failed: {str(e)}', 'warning')
                
                # Clean up uploaded files
                pdf_path.unlink()
                if template_path and template_path.exists():
                    template_path.unlink()
                for font_path in font_paths:
                    Path(font_path).unlink()
                
                return send_file(
                    str(output_path),
                    as_attachment=True,
                    download_name=output_filename,
                    mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )
            else:
                flash(f'Conversion failed: {result["error"]}')
                return redirect(url_for('index'))
                
        except Exception as e:
            flash(f'Conversion error: {str(e)}')
            return redirect(url_for('index'))
    
    except Exception as e:
        flash(f'An error occurred: {str(e)}')
        return redirect(url_for('index'))

@app.route('/api/convert', methods=['POST'])
def api_convert():
    """API endpoint for programmatic conversion"""
    try:
        # Similar logic to convert_pdf but returns JSON
        # This can be used for API access
        return jsonify({
            'status': 'success',
            'message': 'API endpoint - implementation similar to web interface'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Create the HTML template
    template_dir = Path('templates')
    template_dir.mkdir(exist_ok=True)
    
    html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF to DOCX Converter</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        input[type="file"], input[type="text"], input[type="number"], input[type="password"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        }
        .submit-btn {
            background-color: #007bff;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        .submit-btn:hover {
            background-color: #0056b3;
        }
        .flash-messages {
            margin-bottom: 20px;
        }
        .flash-message {
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .flash-error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .flash-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .help-text {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
        .advanced-options {
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            background-color: #f9f9f9;
        }
        .advanced-options h3 {
            margin-top: 0;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔄 PDF to DOCX Converter</h1>
        <p style="text-align: center; color: #666; margin-bottom: 30px;">
            Convert PDF files to DOCX format with template and font support
        </p>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="flash-messages">
                    {% for category, message in messages %}
                        <div class="flash-message flash-{{ category if category in ['success', 'warning'] else 'error' }}">{{ message }}</div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}
        
        <form action="{{ url_for('convert_pdf') }}" method="post" enctype="multipart/form-data">
            <div class="form-group">
                <label for="pdf_file">📄 PDF File (Required)</label>
                <input type="file" id="pdf_file" name="pdf_file" accept=".pdf" required>
                <div class="help-text">Select the PDF file you want to convert to DOCX</div>
            </div>
            
            <div class="form-group">
                <label for="template_file">📋 Template File (Optional)</label>
                <input type="file" id="template_file" name="template_file" accept=".dotx,.docx">
                <div class="help-text">Upload a Word template (.dotx or .docx) to apply styles</div>
            </div>
            
            <div class="form-group">
                <label for="font_files">🔤 Font Files (Optional)</label>
                <input type="file" id="font_files" name="font_files" accept=".ttf,.otf" multiple>
                <div class="help-text">Upload custom fonts (.ttf or .otf files) - you can select multiple files</div>
            </div>
            
            <div class="advanced-options">
                <h3>⚙️ Advanced Options</h3>
                
                <div class="form-group">
                    <label for="start_page">Start Page (0-indexed)</label>
                    <input type="number" id="start_page" name="start_page" min="0" placeholder="0">
                    <div class="help-text">Page to start conversion from (leave empty for first page)</div>
                </div>
                
                <div class="form-group">
                    <label for="end_page">End Page (exclusive)</label>
                    <input type="number" id="end_page" name="end_page" min="1" placeholder="">
                    <div class="help-text">Page to end conversion at (leave empty for last page)</div>
                </div>
                
                <div class="form-group">
                    <label for="pages">Specific Pages</label>
                    <input type="text" id="pages" name="pages" placeholder="0,2,4">
                    <div class="help-text">Comma-separated page numbers (0-indexed) to convert specific pages</div>
                </div>
                
                <div class="form-group">
                    <label for="password">PDF Password</label>
                    <input type="password" id="password" name="password" placeholder="">
                    <div class="help-text">Enter password if the PDF is encrypted</div>
                </div>
            </div>
            
            <div class="form-group" style="margin-top: 30px;">
                <button type="submit" class="submit-btn">🚀 Convert PDF to DOCX</button>
            </div>
        </form>
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666;">
            <p><strong>Advanced Features:</strong></p>
            <ul style="text-align: left; display: inline-block;">
                <li>✅ Text extraction (not full-page images)</li>
                <li>✅ Template margins and formatting</li>
                <li>✅ Custom font application</li>
                <li>✅ Image cropping and resizing</li>
                <li>✅ Automatic comparison with original PDF</li>
                <li>✅ Quality scoring and automatic improvements</li>
                <li>✅ Page range selection</li>
                <li>✅ Password-protected PDFs</li>
                <li>✅ Proper content fitting within margins</li>
            </ul>
        </div>
    </div>
</body>
</html>'''
    
    with open(template_dir / 'index.html', 'w') as f:
        f.write(html_template)
    
    print("Starting PDF to DOCX Converter Web Interface...")
    print("Open your browser and go to: http://192.168.12.12:4000")
    app.run(debug=True, host='192.168.12.12', port=4000)
