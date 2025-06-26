"""
PDF Extraction Module
Handles all PDF parsing, content extraction, and structure detection
"""

import fitz  # PyMuPDF
from typing import Dict, List, Optional
import logging

class PDFExtractor:
    """Extracts content from PDF files with layout preservation"""
    
    def __init__(self):
        self.pdf_document = None
        self.conversion_stats = {
            'pages_processed': 0,
            'text_blocks_extracted': 0,
            'images_extracted': 0
        }
        self.logger = logging.getLogger('pdf_extraction')
        
    def extract_content(self, pdf_path: str, password: str = None,
                      start_page: int = 0, end_page: int = None,
                      pages: List[int] = None) -> Dict:
        """Main extraction method"""
        try:
            self.pdf_document = fitz.open(pdf_path)
            
            # Handle password protection
            if self.pdf_document.needs_pass:
                if password:
                    if not self.pdf_document.authenticate(password):
                        raise ValueError("Invalid password provided")
                else:
                    raise ValueError("PDF is encrypted but no password provided")
            
            total_pages = len(self.pdf_document)
            self.logger.info(f"PDF has {total_pages} pages")
            
            # Determine which pages to process
            if pages:
                page_indices = [p for p in pages if 0 <= p < total_pages]
            else:
                start = max(0, start_page)
                end = min(total_pages, end_page) if end_page else total_pages
                page_indices = list(range(start, end))
            
            extracted_content = {
                'pages': [],
                'total_pages': len(page_indices),
                'page_indices': page_indices
            }
            
            # Extract content from each page
            for page_idx in page_indices:
                page = self.pdf_document[page_idx]
                page_content = self._extract_page_content(page, page_idx)
                extracted_content['pages'].append(page_content)
                self.conversion_stats['pages_processed'] += 1
            
            self.logger.info(f"Extracted content from {len(page_indices)} pages")
            return extracted_content
            
        except Exception as e:
            self.logger.error(f"Extraction failed: {e}")
            return {}
        finally:
            if hasattr(self, 'pdf_document'):
                self.pdf_document.close()
            
    def _extract_page_content(self, page, page_idx: int) -> Dict:
        """Extract text and images from a single PDF page"""
        page_content = {
            'page_number': page_idx,
            'text_blocks': [],
            'images': [],
            'page_size': {
                'width': float(page.mediabox.width),
                'height': float(page.mediabox.height)
            }
        }
        
        # Extract text with positioning information
        text_blocks = self._extract_text_with_layout(page)
        page_content['text_blocks'] = text_blocks
        self.conversion_stats['text_blocks_extracted'] += len(text_blocks)
        
        # Extract images
        images = self._extract_images_from_page(page, page_idx)
        page_content['images'] = images
        self.conversion_stats['images_extracted'] += len(images)
        
        return page_content
        
    def _extract_text_with_layout(self, page) -> List[Dict]:
        """Extract text with layout information using PyMuPDF with proper spacing"""
        text_blocks = []
        
        try:
            # Use PyMuPDF blocks method for better text spacing
            blocks = page.get_text("blocks")
            page_text_parts = []
            
            for block in blocks:
                if len(block) >= 5 and block[4].strip():  # Text block
                    text = block[4].strip()
                    bbox = block[:4]  # x0, y0, x1, y1
                    
                    page_text_parts.append({
                        'text': text,
                        'x': bbox[0],
                        'y': bbox[1],
                        'bbox': bbox
                    })
            
            # Sort by position (top to bottom, left to right)
            # In PDF coordinates, Y increases downward, so we sort by Y ascending
            page_text_parts.sort(key=lambda p: (p['y'], p['x']))
            
            # Combine text parts with proper spacing
            if page_text_parts:
                combined_text = ' '.join([part['text'] for part in page_text_parts])
                
                text_blocks.append({
                    'text': combined_text.strip(),
                    'x': page_text_parts[0]['x'],
                    'y': page_text_parts[0]['y'],
                    'font_name': 'Unknown',
                    'font_size': 12.0,
                    'matrix': [1, 0, 0, 1, 0, 0],
                    'parts': page_text_parts
                })
            
        except Exception as e:
            self.logger.warning(f"PyMuPDF text extraction failed: {e}")
            # Fallback to simple extraction
            try:
                text = page.get_text()
                if text.strip():
                    text_blocks.append({
                        'text': text.strip(),
                        'x': 0,
                        'y': 0,
                        'font_name': 'Unknown',
                        'font_size': 12.0,
                        'matrix': [1, 0, 0, 1, 0, 0]
                    })
            except Exception as e2:
                self.logger.error(f"Fallback text extraction also failed: {e2}")
        
        return text_blocks
        
    def _extract_images_from_page(self, page, page_idx: int) -> List[Dict]:
        """Extract images from a PDF page using PyMuPDF"""
        from io import BytesIO
        from PIL import Image
        
        images = []
        
        try:
            image_list = page.get_images()
            
            for img_idx, img in enumerate(image_list):
                try:
                    # Get image reference
                    xref = img[0]
                    
                    # Extract image data
                    base_image = self.pdf_document.extract_image(xref)
                    image_data = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # Create image name
                    image_name = f"image_{page_idx}_{img_idx}.{image_ext}"
                    
                    # Try to get image dimensions
                    try:
                        pil_image = Image.open(BytesIO(image_data))
                        width, height = pil_image.size
                        format_type = pil_image.format
                    except Exception:
                        width, height = 100, 100  # Default size
                        format_type = image_ext.upper()
                    
                    image_info = {
                        'name': image_name,
                        'data': image_data,
                        'width': width,
                        'height': height,
                        'format': format_type,
                        'page_number': page_idx,
                        'index': img_idx
                    }
                    
                    images.append(image_info)
                    
                except Exception as e:
                    self.logger.warning(f"Failed to extract image {img_idx} from page {page_idx}: {e}")
                    
        except Exception as e:
            self.logger.warning(f"Failed to extract images from page {page_idx}: {e}")
        
        return images
        
    def detect_document_structure(self, page) -> Dict:
        """Detects headings, paragraphs, lists, etc."""
        # [Implementation of structure detection]
        
    def extract_text_with_layout(self, page) -> List[Dict]:
        """Extracts text with positioning information"""
        # [Implementation from modern_pdf2docx_converter.py]
        
    # Other extraction methods...
