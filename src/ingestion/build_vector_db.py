import os
import json
import re
import pymupdf  # Replaces deprecated fitz import
import chromadb
from sentence_transformers import SentenceTransformer

RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"

# Ensure required directories exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

pdf_files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith(".pdf")]

if not pdf_files:
    raise FileNotFoundError(
        f"No PDF files found inside '{RAW_DATA_DIR}'. "
        "Ensure constitution_of_india.pdf is committed and present."
    )

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="chroma_db")

try:
    client.delete_collection(name="constitution")
except Exception:
    pass

collection = client.create_collection(name="constitution")

documents, metadatas, ids = [], [], []
chunk_count = 0

def is_toc_page(text: str) -> bool:
    dot_leaders = len(re.findall(r'\.{4,}\s*\d+', text))
    if dot_leaders > 3 or "ARRANGEMENT OF ARTICLES" in text.upper():
        return True
    return False

print(f"Found {len(pdf_files)} PDF file(s) in {RAW_DATA_DIR}: {pdf_files}\n")

for pdf_name in pdf_files:
    pdf_path = os.path.join(RAW_DATA_DIR, pdf_name)
    doc_title = pdf_name.replace(".pdf", "").replace("_", " ").title()
    doc = pymupdf.open(pdf_path)

    print(f"Processing '{doc_title}' ({len(doc)} pages)...")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        
        # Strip Hindi/Devanagari script if present
        english_text = re.sub(r'[\u0900-\u097F]+', '', text).strip()

        if is_toc_page(english_text) or len(english_text) < 150:
            continue

        chunk_size = 1800
        overlap = 300
        start = 0
        
        while start < len(english_text):
            end = start + chunk_size
            chunk_text = english_text[start:end].strip()
            
            if len(chunk_text) > 100:
                documents.append(chunk_text)
                metadatas.append({
                    "source": doc_title,
                    "page": page_num + 1,
                    "file_name": pdf_name
                })
                ids.append(f"chunk_{chunk_count}")
                chunk_count += 1
                
            start += chunk_size - overlap

print(f"\nGenerating embeddings for {len(documents)} total document chunks...")
embeddings = model.encode(documents, show_progress_bar=True).tolist()

# Save processed text chunks
with open(os.path.join(PROCESSED_DATA_DIR, "chunks.json"), "w", encoding="utf-8") as f:
    json.dump({"documents": documents, "metadatas": metadatas, "ids": ids}, f, indent=2, ensure_ascii=False)

collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)
print(f"Vector database built successfully! Total indexed chunks: {collection.count()}")