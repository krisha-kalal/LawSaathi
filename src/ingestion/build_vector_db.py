import os
import json
import chromadb
from sentence_transformers import SentenceTransformer
from chunker import extract_clean_chunks

PDF_PATH = "data/raw/constitution_of_india.pdf"

if not os.path.exists(PDF_PATH):
    raise FileNotFoundError(f"Missing source file at {PDF_PATH}")

documents, metadatas, ids = extract_clean_chunks(PDF_PATH)

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="chroma_db")

try:
    client.delete_collection(name="constitution")
except Exception:
    pass

collection = client.create_collection(name="constitution")

print(f"Generating embeddings for {len(documents)} cleaned body chunks...")
embeddings = model.encode(documents, show_progress_bar=True).tolist()

os.makedirs("data/processed", exist_ok=True)
with open("data/processed/chunks.json", "w", encoding="utf-8") as f:
    json.dump({"documents": documents, "metadatas": metadatas, "ids": ids}, f, indent=2, ensure_ascii=False)

collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)
print(f"Index clean. Total indexed chunks: {collection.count()}")