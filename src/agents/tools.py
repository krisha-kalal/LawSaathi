from langchain_core.tools import tool
from rag.pipeline import answer_question

@tool
def constitution_retrieval_tool(query: str) -> str:
    """
    Useful for answering questions about the Constitution of India, Articles, 
    Fundamental Rights, Fundamental Duties, and legal provisions.
    """
    answer, metadata = answer_question(query, top_candidates=50, final_top_k=12)
    
    pages = list(set(m.get("page", "N/A") for m in metadata))
    sources_str = ", ".join([f"Page {p}" for p in pages])
    
    return f"{answer}\n\n[Retrieved Pages: {sources_str}]"