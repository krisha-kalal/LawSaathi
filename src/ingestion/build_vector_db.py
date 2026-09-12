import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


PDF_PATH = "data/raw/constitution_of_india.pdf"


def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


reader = PdfReader(PDF_PATH)

pages = []

for page_number, page in enumerate(reader.pages):
    text = page.extract_text()

    if text:
        pages.append({
            "page": page_number + 1,
            "text": text
        })


model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="constitution"
)


documents = []
metadatas = []
ids = []


for page in pages:

    chunks = chunk_text(page["text"])

    for chunk_number, chunk in enumerate(chunks):

        documents.append(chunk)

        metadatas.append({
            "source": "Constitution of India",
            "page": page["page"],
            "chunk": chunk_number
        })

        ids.append(
            f"page_{page['page']}_chunk_{chunk_number}"
        )


embeddings = model.encode(
    documents,
    show_progress_bar=True
).tolist()


collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)


print("Total documents:", collection.count())