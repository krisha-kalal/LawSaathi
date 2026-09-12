# LawSaathi 🇮🇳

> An open-source AI-powered legal research assistant for Indian legal documents.

LawSaathi is being built as an open-source Retrieval-Augmented Generation (RAG) project focused on Indian legal information.

The goal is to build a system that can retrieve relevant legal documents, provide evidence-grounded answers, and cite the sources used to generate each response.

## 🚧 Project Status

**Currently in development — Day 1**

The initial document ingestion and semantic retrieval pipeline is working.

### Completed

- [x] GitHub repository setup
- [x] Python virtual environment
- [x] Project structure
- [x] PDF document ingestion
- [x] Text extraction using PyPDF
- [x] Basic text chunking
- [x] Sentence embeddings
- [x] ChromaDB vector database
- [x] Semantic similarity search
- [x] Metadata storage for source and page information

### Current Pipeline

```text
Indian Legal PDF
       ↓
   PDF Extraction
       ↓
      Text
       ↓
    Chunking
       ↓
  Embedding Model
       ↓
    ChromaDB
       ↓
 Semantic Search