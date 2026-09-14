import os
import sys
from pathlib import Path

# Silence HuggingFace warnings before imports
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

sys.path.append(str(Path(__file__).resolve().parent))

from rag.pipeline import answer_question

if __name__ == "__main__":
    question = input("Ask LawSaathi: ")
    print("\nProcessing query via Re-Ranked Hybrid Pipeline...\n")
    answer, sources = answer_question(question)
    
    print("=" * 60)
    print("ANSWER")
    print("=" * 60)
    print(answer)
    print("\n" + "=" * 60)
    print("SOURCES USED")
    print("=" * 60)
    
    seen_pages = set()
    for source in sources:
        page = source.get("page", "N/A")
        doc_name = source.get("source", "Constitution of India")
        if page not in seen_pages:
            seen_pages.add(page)
            print(f"- {doc_name} (Page {page})")