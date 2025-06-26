#!/usr/bin/env python3
import fitz

def test_blocks_extraction(pdf_path):
    doc = fitz.open(pdf_path)
    
    for page_num in range(min(2, len(doc))):  # Test first 2 pages
        page = doc[page_num]
        print(f"\nPage {page_num + 1}:")
        print("=" * 40)
        
        # Test blocks method
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
                print(f"Block: '{text}' at ({bbox[0]:.1f}, {bbox[1]:.1f})")
        
        # Sort by position (top to bottom, left to right)
        # In PDF coordinates, Y increases downward, so we sort by Y ascending
        page_text_parts.sort(key=lambda p: (p['y'], p['x']))
        
        # Combine text parts with proper spacing
        combined_text = ' '.join([part['text'] for part in page_text_parts])
        
        print(f"\nCombined text: '{combined_text}'")
    
    doc.close()

if __name__ == "__main__":
    test_blocks_extraction("first_hundred/the first hundred years Book pg 1-10.pdf")
