from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [
    "The Supreme Court is the highest court in India.",
    "India has a Supreme Court.",
    "Pizza is a popular food."
]

embeddings = model.encode(texts)

print("Number of embeddings:", len(embeddings))
print("Embedding size:", len(embeddings[0]))

similarity = cosine_similarity(
    [embeddings[0]],
    embeddings[1:]
)

print(similarity)