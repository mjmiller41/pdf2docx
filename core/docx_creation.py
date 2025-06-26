"""
DOCX Creation Module
Handles document assembly, formatting, and template application
"""

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.section import WD_ORIENT
from typing import Dict, List, Any
import logging

class DOCXCreator:
    """Creates DOCX documents from extracted PDF content"""
    
    def __init__(self, template_path: str = None):
        self.template_path = template_path
        self.docx_document = None
        self.custom_fonts = []
        self.logger = logging.getLogger('docx_creation')
        
    def create_from_pdf_data(self, pdf_data: Dict) -> Document:
        """Create DOCX from extracted PDF content"""
        if self.template_path:
            self.docx_document = Document(self.template_path)
            # Clear existing content but keep styles
            for element in list(self.docx_document.element.body):
                if element.tag.endswith(('sectPr', 'sectPr')):
                    continue
                self.docx_document.element.body.remove(element)
        else:
            self.docx_document = Document()
            
        self._apply_template_formatting(pdf_data)
        self._add_content(pdf_data)
        return self.docx_document
        
    def _apply_template_formatting(self, pdf_data: Dict) -> None:
        """Apply template formatting to document"""
        # [Implementation from modern_pdf2docx_converter.py]
        
    def _add_content(self, pdf_data: Dict) -> None:
        """Add content to document"""
        # [Implementation from modern_pdf2docx_converter.py]
        
    def save(self, output_path: str) -> None:
        """Save document to file"""
        if self.docx_document:
            self.docx_document.save(output_path)
            
    # Other document creation methods...
