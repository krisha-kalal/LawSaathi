from pypdf import PdfReader
from chunker import chunk_text

pdf_path = "data/raw/constitution_of_india.pdf"

reader = PdfReader(pdf_path)

all_text = ""

for page in reader.pages:
    text = page.extract_text()

    if text:
        all_text += text + "\n"

chunks = chunk_text(all_text)

print("Total characters:", len(all_text))
print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks[:3]):
    print(f"\n--- Chunk {i + 1} ---")
    print(chunk[:500])