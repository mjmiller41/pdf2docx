#!/usr/bin/env python3
import fitz
import sys

try:
    doc = fitz.open('first_hundred/the first hundred years Book pg 1-10.pdf')
    print(f'PDF has {len(doc)} pages')
    
    for i in range(min(3, len(doc))):
        page = doc[i]
        text = page.get_text().strip()
        print(f'Page {i+1}: {len(text)} characters')
        if text:
            print(f'  Preview: {text[:50]}...')
        else:
            print('  (No text content)')
    
    doc.close()
    print("Done")
    
except Exception as e:
    print(f"Error: {e}")
