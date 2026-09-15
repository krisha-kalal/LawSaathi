# LawSaathi 

**LawSaathi** is an open-source AI-powered legal question-answering system built using **Retrieval-Augmented Generation (RAG)**. It processes the Constitution of India, retrieves relevant legal information, and generates grounded answers with source references.

The project focuses on understanding and implementing modern AI concepts including **embeddings, vector databases, BM25, hybrid retrieval, re-ranking, LLMs, and prompt engineering**.

## 🚀 Features

* 📄 PDF document ingestion and text extraction
* 🧹 Layout-aware cleaning and noise/TOC filtering
* ✂️ Overlapping text chunking
* 🔎 Semantic search using embeddings
* 🗂️ ChromaDB vector database
* 🔤 BM25 keyword-based retrieval
* 🔀 Hybrid retrieval using RRF
* 🎯 Cross-Encoder re-ranking
* 🤖 Gemini-powered answer generation
* 📚 Source and page-level citations
* 🛡️ Context-grounded prompting to reduce hallucinations

## 🛠️ Tech Stack

**Python · PyMuPDF · Sentence Transformers · ChromaDB · BM25 · Cross-Encoder · Google Gemini · Git/GitHub**

## 📁 Project Structure

```text
Lawsaathi/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── ingestion/
│   ├── retrieval/
│   ├── rag/
│   ├── llm/
│   └── main.py
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Setup

```bash
git clone https://github.com/your-username/Lawsaathi.git
cd Lawsaathi

python -m venv .venv
```

Activate the virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

## ▶️ Run

Build the vector database:

```bash
python src/ingestion/build_vector_db.py
```

Start LawSaathi:

```bash
python src/main.py
```

## 📈 Development Progress

* [x] **Day 1:** Project setup, PDF extraction & text chunking
* [x] **Day 2:** Embeddings & ChromaDB vector search
* [x] **Day 3:** Basic RAG pipeline & Gemini integration
* [x] **Day 4:** Source metadata, citations & grounding
* [x] **Day 5:** BM25 + dense hybrid retrieval
* [x] **Day 6:** Cross-Encoder re-ranking
* [x] FastAPI API
* [x] Agentic workflows with LangGraph
* [x] RAG evaluation & retrieval metrics
* [x] Testing, Docker & CI/CD

## 🌱 Open Source

LawSaathi is being developed as an open-source project to explore and implement practical **Generative AI and RAG engineering concepts**.

## ⚠️ Disclaimer

LawSaathi is an educational AI project and does not provide professional legal advice. Always verify legal information using authoritative sources.
