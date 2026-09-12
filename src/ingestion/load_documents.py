from pypdf import PdfReader

pdf_path = "data/raw/constitution_of_india.pdf"

reader = PdfReader(pdf_path)

print("Number of pages:", len(reader.pages))

for i, page in enumerate(reader.pages[:3]):
    text = page.extract_text()
    print(f"\n--- Page {i + 1} ---")
    print(text[:1000])