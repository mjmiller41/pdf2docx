#!/usr/bin/env python3
import fitz

def extract_all_pages(pdf_path):
    doc = fitz.open(pdf_path)
    all_text = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text().strip()
        if text:
            print(f"Page {page_num + 1}:")
            print(text)
            print("-" * 40)
            all_text.append(text)
    
    doc.close()
    return '\n\n'.join(all_text)

if __name__ == "__main__":
    pdf_path = "first_hundred/the first hundred years Book pg 1-10.pdf"
    full_text = extract_all_pages(pdf_path)
    print("\nCOMBINED TEXT:")
    print("=" * 50)
    print(full_text)
