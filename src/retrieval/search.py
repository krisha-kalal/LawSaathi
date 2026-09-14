import os
import sys
import json
from pathlib import Path
import chromadb
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, CrossEncoder
from dotenv import load_dotenv
from google import genai

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY missing from environment.")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_collection(name="constitution")
ai_client = genai.Client(api_key=api_key)

chunks_file = Path("data/processed/chunks.json")
with open(chunks_file, "r", encoding="utf-8") as f:
    data = json.load(f)

raw_documents = data["documents"]
corpus_metadatas = data["metadatas"]
tokenized_corpus = [doc.lower().split() for doc in raw_documents]
bm25 = BM25Okapi(tokenized_corpus)

def rerank_hybrid_search(query: str, top_candidates: int = 30, final_top_k: int = 10) -> str:
    # Sparse BM25
    tokenized_query = query.lower().split()
    bm25_scores = bm25.get_scores(tokenized_query)
    bm25_indices = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)[:top_candidates]
    
    # Dense Vector
    query_vector = embedding_model.encode([query]).tolist()
    vector_results = collection.query(query_embeddings=query_vector, n_results=top_candidates)
    
    # Merge candidates
    candidate_docs = []
    seen_texts = set()

    for idx in bm25_indices:
        text = raw_documents[idx]
        if text not in seen_texts:
            seen_texts.add(text)
            candidate_docs.append((text, corpus_metadatas[idx].get("page", "N/A")))

    for idx, text in enumerate(vector_results["documents"][0]):
        if text not in seen_texts:
            seen_texts.add(text)
            page_num = vector_results["metadatas"][0][idx].get("page", "N/A")
            candidate_docs.append((text, page_num))

    # Cross-Encoder Re-rank
    pairs = [[query, doc[0]] for doc in candidate_docs]
    scores = reranker.predict(pairs)
    
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:final_top_k]
    
    context_blocks = []
    for idx in ranked_indices:
        text, page_num = candidate_docs[idx]
        context_blocks.append(f"[Page {page_num}]:\n{text}")

    return "\n\n---\n\n".join(context_blocks)

def generate_rag_response(query: str) -> str:
    context = rerank_hybrid_search(query)
    
    prompt = f"""
You are LawSaathi, an expert Indian legal assistant.
Answer the user's question accurately using ONLY the retrieved constitutional context below.

Context:
{context}

User Question: {query}

Instructions:
- Provide an accurate, detailed explanation based strictly on the context.
- Quote specific Article numbers, Clauses, and page citations provided.
- Do NOT state that information is missing if it is answered within the retrieved context.
"""
    
    response = ai_client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    user_query = input("Ask a legal question: ")
    print("\nExecuting Re-Ranked Hybrid Search...\n")
    answer = generate_rag_response(user_query)
    print("=" * 60)
    print("LawSaathi Response:")
    print("=" * 60)
    print(answer)