import os
import json
from pathlib import Path

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import chromadb
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, CrossEncoder
from llm.gemini import generate_answer
from rag.prompt import build_prompt

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
chunks_file = PROJECT_ROOT / "data" / "processed" / "chunks.json"
chroma_path = PROJECT_ROOT / "chroma_db"

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
client = chromadb.PersistentClient(path=str(chroma_path))
collection = client.get_collection(name="constitution")

if not chunks_file.exists():
    raise FileNotFoundError("Run build_vector_db.py first to create chunks.json")

with open(chunks_file, "r", encoding="utf-8") as f:
    data = json.load(f)

raw_documents = data["documents"]
corpus_metadatas = data["metadatas"]
tokenized_corpus = [doc.lower().split() for doc in raw_documents]
bm25 = BM25Okapi(tokenized_corpus)

def expand_query(query: str) -> str:
    """Expands short article queries to ensure dense retrieval matches main statutory bodies."""
    clean_q = query.strip().lower()
    if clean_q.startswith("article ") and len(clean_q.split()) <= 3:
        art_num = clean_q.replace("article", "").strip()
        return f"Article {art_num}. protection rights provision state law"
    return query

def answer_question(question: str, top_candidates: int = 50, final_top_k: int = 12):
    search_query = expand_query(question)
    
    # BM25 Sparse Search
    tokenized_query = search_query.lower().split()
    bm25_scores = bm25.get_scores(tokenized_query)
    bm25_indices = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)[:top_candidates]

    # Dense Vector Search
    query_vector = embedding_model.encode([search_query]).tolist()
    vector_results = collection.query(query_embeddings=query_vector, n_results=top_candidates)

    # Merging Candidates
    candidate_docs = []
    seen_texts = set()

    for idx in bm25_indices:
        text = raw_documents[idx]
        if text not in seen_texts:
            seen_texts.add(text)
            candidate_docs.append((text, corpus_metadatas[idx]))

    for idx, text in enumerate(vector_results["documents"][0]):
        if text not in seen_texts:
            seen_texts.add(text)
            meta = vector_results["metadatas"][0][idx]
            candidate_docs.append((text, meta))

    # Cross-Encoder Re-Ranking
    pairs = [[question, doc[0]] for doc in candidate_docs]
    scores = reranker.predict(pairs)
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:final_top_k]

    context_parts = []
    used_metadata = []
    
    for rank_idx, idx in enumerate(ranked_indices):
        text, meta = candidate_docs[idx]
        context_parts.append(f"[Source {rank_idx + 1}] (Page {meta.get('page', 'N/A')}):\n{text}")
        used_metadata.append(meta)

    context = "\n\n---\n\n".join(context_parts)
    prompt = build_prompt(question, context)
    answer = generate_answer(prompt)
    
    return answer, used_metadata