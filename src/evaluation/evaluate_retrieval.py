import json
import re
import sys
from pathlib import Path
import numpy as np

# Calculate project root and add 'src' to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

# Import the core hybrid search function from your retrieval module
from retrieval.search import rerank_hybrid_search as retrieve_documents

def evaluate_retriever(dataset_path: Path, top_k: int = 10):
    if not dataset_path.exists():
        raise FileNotFoundError(f"Evaluation dataset missing at {dataset_path}")

    with open(dataset_path, "r", encoding="utf-8") as f:
        eval_set = json.load(f)

    recalls = []
    reciprocal_ranks = []

    print("=" * 60)
    print(f"RUNNING RETRIEVAL EVALUATION ({len(eval_set)} Queries | Top-K = {top_k})")
    print("=" * 60 + "\n")

    for item in eval_set:
        query = item["question"]
        target_page = int(item["expected_page"])

        # Run retrieval engine (returns a formatted string block of pages)
        retrieved_context = retrieve_documents(query, top_candidates=30, final_top_k=top_k)
        
        # Parse out all "[Page X]:" occurrences from the returned text block
        retrieved_pages = [int(p) for p in re.findall(r"\[Page (\d+)\]:", retrieved_context)]

        # Calculate Recall@K
        hit = target_page in retrieved_pages
        recalls.append(1.0 if hit else 0.0)

        # Calculate Mean Reciprocal Rank (MRR)
        if hit:
            rank = retrieved_pages.index(target_page) + 1
            rr = 1.0 / rank
        else:
            rr = 0.0
        reciprocal_ranks.append(rr)

        status = "HIT " if hit else "MISS"
        print(f"[{status}] Query: '{query}'")
        print(f"       Target Page: {target_page} | Retrieved Top Pages: {retrieved_pages[:5]}")
        print(f"       Reciprocal Rank: {rr:.3f}\n")

    mean_recall = np.mean(recalls) * 100
    mean_mrr = np.mean(reciprocal_ranks)

    print("=" * 60)
    print("RETRIEVAL EVALUATION RESULTS")
    print("=" * 60)
    print(f"Recall@{top_k}: {mean_recall:.2f}%")
    print(f"Mean Reciprocal Rank (MRR): {mean_mrr:.4f}")
    print("=" * 60)

if __name__ == "__main__":
    dataset_file = PROJECT_ROOT / "tests" / "eval_dataset.json"
    evaluate_retriever(dataset_file, top_k=10)
