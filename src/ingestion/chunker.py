import re
import fitz  # PyMuPDF

def extract_clean_chunks(pdf_path: str) -> tuple[list[str], list[dict], list[str]]:
    doc = fitz.open(pdf_path)
    documents, metadatas, ids = [], [], []
    chunk_count = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        
        # Filter out Devnagari/Hindi script
        english_text = re.sub(r'[\u0900-\u097F]+', '', text).strip()

        # Reject TOC pages via dot-leader count or explicit headers
        dot_leaders = len(re.findall(r'\.{4,}\s*\d+', english_text))
        if dot_leaders > 3 or "ARRANGEMENT OF ARTICLES" in english_text.upper():
            continue

        if len(english_text) < 150:
            continue

        # Overlapping parent chunks
        chunk_size = 1800
        overlap = 300
        start = 0
        
        while start < len(english_text):
            end = start + chunk_size
            chunk_text = english_text[start:end].strip()
            
            if len(chunk_text) > 100:
                documents.append(chunk_text)
                metadatas.append({
                    "source": "Constitution of India",
                    "page": page_num + 1,
                    "document_type": "constitution"
                })
                ids.append(f"doc_chunk_{chunk_count}")
                chunk_count += 1
                
            start += chunk_size - overlap

    return documents, metadatas, ids