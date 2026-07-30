from ScraperMain.extract.extract import run_extraction
from ScraperMain.scrape import mca
from ScraperMain.services.gemini import run_gemini_structuring

def main():
    print("\n--- Running  Web Scraper ---")
    mca.run_scraper()

    print("\n--- Running PDF Markdown Extraction ---")
    run_extraction()
    
  
    print("\n--- Running Gemini Structured Analysis ---")
    run_gemini_structuring()
    
    print("\nEntire workflow pipeline executed successfully!")

if __name__ == "__main__":
    main()
