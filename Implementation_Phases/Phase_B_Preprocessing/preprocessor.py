import os
import json
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_paths():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_raw_dir = os.path.join(base_dir, "data", "raw")
    metadata_path = os.path.join(data_raw_dir, "scraping_metadata.json")
    processed_dir = os.path.join(base_dir, "data", "processed")
    return data_raw_dir, metadata_path, processed_dir

def clean_text(text):
    """Remove noise, redundant whitespace and generic headers/footers placeholders"""
    # Remove repetitive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove lines that look like page numbers
    text = re.sub(r'Page \d+ of \d+', '', text)
    return text.strip()

def identify_scheme(url):
    """Extract scheme name from URL/Filename"""
    schemes = {
        "bluechip": "SBI Bluechip Fund",
        "flexicap": "SBI Flexicap Fund",
        "long-term-equity": "SBI Long Term Equity Fund (ELSS)",
        "expense-ratio": "SBI Mutual Fund - TER",
        "load-structure": "SBI Mutual Fund - Load Structure"
    }
    url_lower = url.lower()
    for key, val in schemes.items():
        if key in url_lower:
            return val
    return "General Mutual Fund Information"

def identify_section(text):
    """Identify section based on keywords in text"""
    sections = {
        "Expense Ratio": ["expense ratio", "ter", "total expense"],
        "Exit Load": ["exit load", "redemption load"],
        "Investment Objective": ["objective", "aims to provide"],
        "Risk": ["risk", "riskometer", "volatility"],
        "Taxation": ["tax", "capital gains", "elss"]
    }
    text_lower = text.lower()
    for section, keywords in sections.items():
        if any(kw in text_lower for kw in keywords):
            return section
    return "General Info"

def preprocess_all():
    raw_dir, meta_path, processed_dir = get_paths()
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
        
    if not os.path.exists(meta_path):
        print("Scraper metadata not found.")
        return

    with open(meta_path, 'r', encoding='utf-8') as f:
        metadata_map = json.load(f)

    # Use actual TOKENS for splitting as per Architecture
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=400, # Mid-range of 300-500 tokens
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    all_chunks = []

    for url, meta in metadata_map.items():
        if meta["status"] != "success":
            continue
            
        filepath = meta["file_path"]
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        cleaned = clean_text(content)
        scheme_name = identify_scheme(url)
        
        # Split into chunks
        chunks = text_splitter.split_text(cleaned)
        
        for i, chunk_text in enumerate(chunks):
            # Identifying section per chunk
            section_name = identify_section(chunk_text)
            
            # Phase 7: Extract page number from text markers
            page_num = "N/A"
            page_match = re.search(r'\[SOURCE_PAGE_(\d+)\]', chunk_text)
            if page_match:
                page_num = page_match.group(1)

            chunk_data = {
                "text": chunk_text,
                "metadata": {
                    "scheme_name": scheme_name,
                    "document_type": meta["document_type"],
                    "source_url": url,
                    "section": section_name,
                    "page_number": page_num,
                    "last_updated": meta["last_scraped"],
                    "chunk_id": f"{scheme_name}_{i}".replace(" ", "_")
                }
            }
            all_chunks.append(chunk_data)

    output_path = os.path.join(processed_dir, "chunks.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, indent=4)
        
    print(f"Preprocessing complete! Created {len(all_chunks)} chunks in {output_path}")

if __name__ == "__main__":
    preprocess_all()
