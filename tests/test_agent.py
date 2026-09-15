import sys
from pathlib import Path

# Calculate project root and add 'src' to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from agents.law_agent import run_law_saathi_agent

print("--- Test 1: Legal Query (Triggers RAG Tool) ---")
q1 = "What is Article 19?"
print(f"User Query: {q1}\n")
response1 = run_law_saathi_agent(q1)
print(response1)

print("\n" + "=" * 60 + "\n")

print("--- Test 2: Non-Legal Query (Triggers Fallback Node) ---")
q2 = "Can you write me a recipe for chocolate cake?"
print(f"User Query: {q2}\n")
response2 = run_law_saathi_agent(q2)
print(response2)