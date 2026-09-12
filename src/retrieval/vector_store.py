import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="lawsaathi"
)

documents = [
    "The Supreme Court is the highest court in India.",
    "The Constitution guarantees fundamental rights.",
    "The President of India is the head of the Union executive."
]

embeddings = model.encode(documents).tolist()

collection.add(
    ids=["doc1", "doc2", "doc3"],
    documents=documents,
    embeddings=embeddings
)

print("Documents stored:", collection.count())

query = "What is India's highest court?"

query_embedding = model.encode([query]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=2
)

print(results["documents"])