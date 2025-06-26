#!/usr/bin/env python3
"""
Enhanced Text Extraction Tool

Tests multiple PDF text extraction methods to find the best approach
for proper text extraction without word scrambling.
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple
import logging

# Multiple PDF libraries for comparison
try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    from pdfminer.high_level import extract_text
    from pdfminer.layout import LAParams
    PDFMINER_AVAILABLE = True
except ImportError:
    PDFMINER_AVAILABLE = False

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

class EnhancedTextExtractor:
    """Test multiple text extraction methods to find the best approach"""
    
    def __init__(self):
        self.extraction_methods = []
        self._register_available_methods()
    
    def _register_available_methods(self):
        """Register all available extraction methods"""
        if PYPDF_AVAILABLE:
            self.extraction_methods.append(('pypdf_simple', self._extract_pypdf_simple))
            self.extraction_methods.append(('pypdf_visitor', self._extract_pypdf_visitor))
        
        if PYMUPDF_AVAILABLE:
            self.extraction_methods.append(('pymupdf_simple', self._extract_pymupdf_simple))
            self.extraction_methods.append(('pymupdf_dict', self._extract_pymupdf_dict))
            self.extraction_methods.append(('pymupdf_blocks', self._extract_pymupdf_blocks))
        
        if PDFPLUMBER_AVAILABLE:
            self.extraction_methods.append(('pdfplumber', self._extract_pdfplumber))
        
        if PDFMINER_AVAILABLE:
            self.extraction_methods.append(('pdfminer', self._extract_pdfminer))
        
        logger.info(f"Registered {len(self.extraction_methods)} extraction methods")
    
    def _extract_pypdf_simple(self, pdf_path: str) -> Dict:
        """Extract text using pypdf simple method"""
        try:
            reader = PdfReader(pdf_path)
            text_blocks = []
            
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text.strip():
                    text_blocks.append({
                        'page': page_num,
                        'text': text.strip(),
                        'method': 'simple_extraction'
                    })
            
            return {
                'status': 'success',
                'text_blocks': text_blocks,
                'total_text': '\n'.join([block['text'] for block in text_blocks])
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _extract_pypdf_visitor(self, pdf_path: str) -> Dict:
        """Extract text using pypdf visitor method with layout preservation"""
        try:
            reader = PdfReader(pdf_path)
            text_blocks = []
            
            for page_num, page in enumerate(reader.pages):
                page_text_parts = []
                
                def text_visitor(text, user_matrix, tm_matrix, font_dict, font_size):
                    if text.strip():
                        x, y = tm_matrix[4], tm_matrix[5]
                        page_text_parts.append({
                            'text': text,
                            'x': float(x),
                            'y': float(y),
                            'font_size': float(font_size) if font_size else 12.0
                        })
                
                try:
                    page.extract_text(visitor_text=text_visitor)
                    
                    # Sort by position (top to bottom, left to right)
                    page_text_parts.sort(key=lambda p: (-p['y'], p['x']))
                    
                    # Combine text parts
                    page_text = ' '.join([part['text'] for part in page_text_parts])
                    
                    if page_text.strip():
                        text_blocks.append({
                            'page': page_num,
                            'text': page_text.strip(),
                            'method': 'visitor_extraction',
                            'parts': page_text_parts
                        })
                except Exception as e:
                    logger.warning(f"Visitor extraction failed for page {page_num}: {e}")
                    # Fallback to simple extraction
                    text = page.extract_text()
                    if text.strip():
                        text_blocks.append({
                            'page': page_num,
                            'text': text.strip(),
                            'method': 'visitor_fallback'
                        })
            
            return {
                'status': 'success',
                'text_blocks': text_blocks,
                'total_text': '\n'.join([block['text'] for block in text_blocks])
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _extract_pymupdf_simple(self, pdf_path: str) -> Dict:
        """Extract text using PyMuPDF simple method"""
        try:
            doc = fitz.open(pdf_path)
            text_blocks = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                if text.strip():
                    text_blocks.append({
                        'page': page_num,
                        'text': text.strip(),
                        'method': 'pymupdf_simple'
                    })
            
            doc.close()
            return {
                'status': 'success',
                'text_blocks': text_blocks,
                'total_text': '\n'.join([block['text'] for block in text_blocks])
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _extract_pymupdf_dict(self, pdf_path: str) -> Dict:
        """Extract text using PyMuPDF dict method with layout info"""
        try:
            doc = fitz.open(pdf_path)
            text_blocks = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text_dict = page.get_text("dict")
                
                page_text_parts = []
                for block in text_dict["blocks"]:
                    if "lines" in block:  # Text block
                        for line in block["lines"]:
                            line_text = ""
                            for span in line["spans"]:
                                if span["text"].strip():
                                    line_text += span["text"]
                            
                            if line_text.strip():
                                bbox = line["bbox"]
                                page_text_parts.append({
                                    'text': line_text,
                                    'x': bbox[0],
                                    'y': bbox[1],
                                    'bbox': bbox
                                })
                
                # Sort by position
                page_text_parts.sort(key=lambda p: (-p['y'], p['x']))
                page_text = ' '.join([part['text'] for part in page_text_parts])
                
                if page_text.strip():
                    text_blocks.append({
                        'page': page_num,
                        'text': page_text.strip(),
                        'method': 'pymupdf_dict',
                        'parts': page_text_parts
                    })
            
            doc.close()
            return {
                'status': 'success',
                'text_blocks': text_blocks,
                'total_text': '\n'.join([block['text'] for block in text_blocks])
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _extract_pymupdf_blocks(self, pdf_path: str) -> Dict:
        """Extract text using PyMuPDF blocks method"""
        try:
            doc = fitz.open(pdf_path)
            text_blocks = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                blocks = page.get_text("blocks")
                
                page_text_parts = []
                for block in blocks:
                    if len(block) >= 5 and block[4].strip():  # Text block
                        text = block[4].strip()
                        bbox = block[:4]
                        page_text_parts.append({
                            'text': text,
                            'x': bbox[0],
                            'y': bbox[1],
                            'bbox': bbox
                        })
                
                # Sort by position
                page_text_parts.sort(key=lambda p: (-p['y'], p['x']))
                page_text = ' '.join([part['text'] for part in page_text_parts])
                
                if page_text.strip():
                    text_blocks.append({
                        'page': page_num,
                        'text': page_text.strip(),
                        'method': 'pymupdf_blocks',
                        'parts': page_text_parts
                    })
            
            doc.close()
            return {
                'status': 'success',
                'text_blocks': text_blocks,
                'total_text': '\n'.join([block['text'] for block in text_blocks])
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _extract_pdfplumber(self, pdf_path: str) -> Dict:
        """Extract text using pdfplumber"""
        try:
            text_blocks = []
            
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text and text.strip():
                        text_blocks.append({
                            'page': page_num,
                            'text': text.strip(),
                            'method': 'pdfplumber'
                        })
            
            return {
                'status': 'success',
                'text_blocks': text_blocks,
                'total_text': '\n'.join([block['text'] for block in text_blocks])
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _extract_pdfminer(self, pdf_path: str) -> Dict:
        """Extract text using pdfminer"""
        try:
            # Try with different layout parameters
            laparams = LAParams(
                line_margin=0.5,
                word_margin=0.1,
                char_margin=2.0,
                boxes_flow=0.5,
                all_texts=False
            )
            
            text = extract_text(pdf_path, laparams=laparams)
            
            if text and text.strip():
                text_blocks = [{
                    'page': 0,  # pdfminer extracts all pages together
                    'text': text.strip(),
                    'method': 'pdfminer'
                }]
            else:
                text_blocks = []
            
            return {
                'status': 'success',
                'text_blocks': text_blocks,
                'total_text': text.strip() if text else ''
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def compare_extraction_methods(self, pdf_path: str) -> Dict:
        """Compare all available extraction methods"""
        logger.info(f"Testing {len(self.extraction_methods)} extraction methods on {pdf_path}")
        
        results = {}
        
        for method_name, method_func in self.extraction_methods:
            logger.info(f"Testing {method_name}...")
            try:
                result = method_func(pdf_path)
                results[method_name] = result
                
                if result['status'] == 'success':
                    text_length = len(result['total_text'])
                    word_count = len(result['total_text'].split())
                    logger.info(f"  ✅ {method_name}: {text_length} chars, {word_count} words")
                else:
                    logger.warning(f"  ❌ {method_name}: {result['error']}")
                    
            except Exception as e:
                logger.error(f"  💥 {method_name}: {str(e)}")
                results[method_name] = {'status': 'error', 'error': str(e)}
        
        return results
    
    def find_best_extraction_method(self, pdf_path: str, reference_text: str = None) -> Tuple[str, Dict]:
        """Find the best extraction method based on various criteria"""
        results = self.compare_extraction_methods(pdf_path)
        
        # Score each method
        method_scores = {}
        
        for method_name, result in results.items():
            if result['status'] != 'success':
                method_scores[method_name] = 0
                continue
            
            score = 0
            text = result['total_text']
            
            # Basic scoring criteria
            score += len(text)  # Longer text usually better
            score += len(text.split()) * 10  # Word count is important
            
            # Penalize obvious issues
            if 'THEFIRST' in text:  # Missing spaces
                score -= 100
            if text.count(' ') < len(text.split()) - 1:  # Not enough spaces
                score -= 50
            
            # Bonus for proper formatting
            if 'THE FIRST' in text:  # Proper spacing
                score += 200
            if 'AVON PARK' in text:  # Proper place names
                score += 100
            
            # If we have reference text, compare similarity
            if reference_text:
                # Simple similarity check
                ref_words = set(reference_text.lower().split())
                text_words = set(text.lower().split())
                similarity = len(ref_words & text_words) / len(ref_words | text_words)
                score += similarity * 1000
            
            method_scores[method_name] = score
        
        # Find best method
        if method_scores:
            best_method = max(method_scores.items(), key=lambda x: x[1])
            return best_method[0], results[best_method[0]]
        else:
            return None, None
    
    def extract_with_best_method(self, pdf_path: str) -> Dict:
        """Extract text using the best available method"""
        best_method_name, best_result = self.find_best_extraction_method(pdf_path)
        
        if best_method_name:
            logger.info(f"Best extraction method: {best_method_name}")
            return {
                'best_method': best_method_name,
                'result': best_result,
                'text': best_result['total_text']
            }
        else:
            return {
                'best_method': None,
                'result': None,
                'text': '',
                'error': 'No extraction method succeeded'
            }

def main():
    """Command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Enhanced PDF Text Extraction Tool')
    parser.add_argument('pdf_path', help='PDF file to extract text from')
    parser.add_argument('--compare', action='store_true', help='Compare all extraction methods')
    parser.add_argument('--best', action='store_true', help='Find and use best extraction method')
    parser.add_argument('--method', help='Use specific extraction method')
    parser.add_argument('--output', help='Save extracted text to file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    extractor = EnhancedTextExtractor()
    
    if args.compare:
        print(f"\n🔍 Comparing all extraction methods for: {args.pdf_path}")
        print("=" * 60)
        
        results = extractor.compare_extraction_methods(args.pdf_path)
        
        for method_name, result in results.items():
            print(f"\n📋 Method: {method_name}")
            if result['status'] == 'success':
                text = result['total_text']
                print(f"   Status: ✅ Success")
                print(f"   Length: {len(text)} characters")
                print(f"   Words: {len(text.split())} words")
                print(f"   Preview: {text[:100]}...")
            else:
                print(f"   Status: ❌ Error - {result['error']}")
    
    elif args.best:
        print(f"\n🎯 Finding best extraction method for: {args.pdf_path}")
        print("=" * 60)
        
        result = extractor.extract_with_best_method(args.pdf_path)
        
        if result['best_method']:
            print(f"✅ Best method: {result['best_method']}")
            print(f"📄 Extracted text:")
            print("-" * 40)
            print(result['text'])
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(result['text'])
                print(f"\n💾 Text saved to: {args.output}")
        else:
            print("❌ No extraction method succeeded")
    
    elif args.method:
        print(f"\n🔧 Using method '{args.method}' for: {args.pdf_path}")
        print("=" * 60)
        
        # Find the method
        method_func = None
        for name, func in extractor.extraction_methods:
            if name == args.method:
                method_func = func
                break
        
        if method_func:
            result = method_func(args.pdf_path)
            if result['status'] == 'success':
                print(f"✅ Success!")
                print(f"📄 Extracted text:")
                print("-" * 40)
                print(result['total_text'])
                
                if args.output:
                    with open(args.output, 'w', encoding='utf-8') as f:
                        f.write(result['total_text'])
                    print(f"\n💾 Text saved to: {args.output}")
            else:
                print(f"❌ Error: {result['error']}")
        else:
            print(f"❌ Unknown method: {args.method}")
            print(f"Available methods: {[name for name, _ in extractor.extraction_methods]}")
    
    else:
        print("Please specify --compare, --best, or --method")
        print(f"Available methods: {[name for name, _ in extractor.extraction_methods]}")

if __name__ == "__main__":
    main()
