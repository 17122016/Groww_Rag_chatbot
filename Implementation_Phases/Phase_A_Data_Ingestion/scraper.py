import os
import requests
from bs4 import BeautifulSoup
import pdfplumber
import io
import json
from datetime import datetime
from urllib.parse import urlparse

# Strict List of 20 URLs defined in the Output Architecture
TARGET_URLS = [
    "https://en.wikipedia.org/wiki/Mutual_fund",
    "https://en.wikipedia.org/wiki/Exchange-traded_fund"
]

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")
METADATA_FILE = os.path.join(DATA_DIR, "scraping_metadata.json")

# Pretend to be a regular browser to avoid superficial bot blocks
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def setup_directories():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def extract_pdf_content(url):
    response = requests.get(url, headers=HEADERS, stream=True)
    response.raise_for_status()
    
    with pdfplumber.open(io.BytesIO(response.content)) as pdf:
        text = ""
        for i, page in enumerate(pdf.pages):
            page_num = i + 1
            page_text = page.extract_text()
            if page_text:
                # Add page marker for forward compatibility with Phase 7 UI
                text += f"\n[SOURCE_PAGE_{page_num}]\n"
                text += page_text + "\n"
                
            # Specifically extract tables
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    clean_row = [str(cell).strip() if cell else "" for cell in row]
                    text += " | ".join(clean_row) + "\n"
                    
        return text

def extract_html_content(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Remove javascript and stylesheet code
    for script_or_style in soup(['script', 'style', 'nav', 'footer']):
        script_or_style.decompose()
        
    # Get text and clean up whitespaces
    text = soup.get_text(separator=' ')
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    cleaned_text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return cleaned_text

def run_scraper():
    setup_directories()
    
    print(f"Starting Scraper. Target URLs: {len(TARGET_URLS)}")
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    metadata = {}
    
    for idx, url in enumerate(TARGET_URLS):
        print(f"[{idx+1}/{len(TARGET_URLS)}] Processing: {url}")
        
        # Generate safe filename
        parsed_url = urlparse(url)
        safe_name = parsed_url.path.strip("/").replace("/", "_").replace(".pdf", "")
        if not safe_name:
            safe_name = "home"
        
        file_path = os.path.join(DATA_DIR, f"{safe_name}.txt")
        
        try:
            if url.lower().endswith('.pdf'):
                content = extract_pdf_content(url)
                doc_type = "PDF"
            else:
                content = extract_html_content(url)
                doc_type = "HTML"
                
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            metadata[url] = {
                "file_path": file_path,
                "document_type": doc_type,
                "last_scraped": date_str,
                "status": "success"
            }
            print(f"  -> Saved successfully to {safe_name}.txt")
            
        except Exception as e:
            print(f"  -> ERROR processing {url}: {e}")
            metadata[url] = {
                "document_type": "PDF" if url.lower().endswith('.pdf') else "HTML",
                "last_scraped": date_str,
                "status": "failed",
                "error": str(e)
            }
            
    # Save compilation metadata
    with open(METADATA_FILE, "w", encoding="utf-8") as mf:
        json.dump(metadata, mf, indent=4)
        
    print(f"\nScraping complete! Metadata saved to {METADATA_FILE}")

if __name__ == "__main__":
    run_scraper()
