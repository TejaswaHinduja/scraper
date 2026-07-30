import os
import glob
from pathlib import Path

import pymupdf4llm


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "frontend" / "public"
OUTPUT_FILE = OUTPUT_DIR / "output.md"

def run_extraction():
    pdf_files = glob.glob("downloads/*.pdf")
    
    if not pdf_files:
        print("Error: No PDF files found to extract.")
        return
        
    
    newest_pdf = max(pdf_files, key=os.path.getmtime)
    print(f"Extracting markdown text from: {newest_pdf}")

    markdown = pymupdf4llm.to_markdown(newest_pdf)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(markdown)
        
    print(f"Extraction successful! Saved to {OUTPUT_FILE}")
