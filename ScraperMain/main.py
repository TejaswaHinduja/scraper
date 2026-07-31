import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.circulars import router as circulars_router

app = FastAPI(title="Scraper Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(circulars_router)

def main():
    from extract.extract import run_extraction
    from scrape import mca
    from services.gemini import run_gemini_structuring

    print("\n--- Running  Web Scraper ---")
    mca.run_scraper()

    print("\n--- Running PDF Markdown Extraction ---")
    run_extraction()
    
  
    print("\n--- Running Gemini Structured Analysis ---")
    run_gemini_structuring()
    
    print("\nEntire workflow pipeline executed successfully!")

if __name__ == "__main__":
    main()
