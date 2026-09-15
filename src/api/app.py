import os
import sys
from pathlib import Path

# Fix import paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT / "src"))

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from api.schemas import QueryRequest, QueryResponse, SourceItem
from rag.pipeline import answer_question

app = FastAPI(
    title="LawSaathi Legal RAG API",
    description="REST API for querying the Constitution of India via Hybrid RAG",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy", "service": "LawSaathi API"}

@app.post("/query", response_model=QueryResponse)
def query_legal_doc(payload: QueryRequest):
    try:
        answer, metadata_list = answer_question(
            question=payload.question,
            top_candidates=payload.top_candidates,
            final_top_k=payload.final_top_k
        )
        
        sources = [
            SourceItem(
                source=meta.get("source", "Constitution of India"),
                page=meta.get("page", 0)
            )
            for meta in metadata_list
        ]
        
        return QueryResponse(
            question=payload.question,
            answer=answer,
            sources=sources
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pipeline processing error: {str(e)}"
        )