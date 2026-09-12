import chromadb
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    name="constitution"
)


query = input("Ask a legal question: ")

query_embedding = model.encode(
    [query]
).tolist()


results = collection.query(
    query_embeddings=query_embedding,
    n_results=5
)


for i in range(len(results["documents"][0])):

    print("\n-----------------------------")

    print("Result:", i + 1)

    print(
        "Source:",
        results["metadatas"][0][i]["source"]
    )

    print(
        "Page:",
        results["metadatas"][0][i]["page"]
    )

    print(
        "\n",
        results["documents"][0][i]
    )