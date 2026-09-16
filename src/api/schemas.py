from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, example="What constitutes a valid contract?")
    document_filter: Optional[str] = Field(default=None, example="Indian Contract Act")
    top_candidates: int = Field(default=50, ge=10, le=100)
    final_top_k: int = Field(default=12, ge=1, le=20)

class SourceItem(BaseModel):
    source: str
    page: int

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceItem]