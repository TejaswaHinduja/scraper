import os
import glob
import pymupdf4llm

def run_extraction():
    pdf_files = glob.glob("downloads/*.pdf")
    
    if not pdf_files:
        print("Error: No PDF files found to extract.")
        return
        
    
    newest_pdf = max(pdf_files, key=os.path.getmtime)
    print(f"Extracting markdown text from: {newest_pdf}")

    markdown = pymupdf4llm.to_markdown(newest_pdf)

    with open("output.md", "w", encoding="utf-8") as f:
        f.write(markdown)
        
    print("Extraction successful! Saved to output.md")
