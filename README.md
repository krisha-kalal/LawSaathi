# LawSaathi ⚖️

**LawSaathi** is an open-source, full-stack AI-powered legal question-answering system built using **Retrieval-Augmented Generation (RAG)**. It processes legal corpora (including the Constitution of India and related statutory documents), retrieves relevant provisions via multi-stage hybrid search, and generates grounded answers with exact page-level source citations.

The project implements a modern RAG architecture featuring **layout-aware multi-document PDF ingestion, dense vector embeddings via ChromaDB, BM25 keyword search, Cross-Encoder re-ranking, LLM prompt grounding, FastAPI REST endpoints, LangGraph agentic tool routing, automated retrieval metrics (Recall@K / MRR), multi-container Docker Compose orchestration, and a Streamlit UI**.

---

## 🚀 Features

* 📄 **Multi-Document Ingestion**: Scalable PDF parsing using PyMuPDF (`pymupdf`) with automated Table of Contents (TOC) filtering and Devanagari/Hindi script stripping.
* ✂️ **Overlapping Parent Chunking**: Context-aware text splitting preserving statutory article and section boundaries.
* 🔎 **Dense Semantic Search**: Vector embeddings generated via `all-MiniLM-L6-v2` stored in ChromaDB.
* 🔤 **Sparse BM25 Search**: Exact keyword retrieval via `rank_bm25` targeting specific legal terms and article numbers.
* 🔀 **Hybrid Retrieval Engine**: Fuses dense semantic vector search with sparse BM25 sparse keyword rankings.
* 🎯 **Two-Stage Re-Ranking**: Employs a Cross-Encoder (`ms-marco-MiniLM-L-6-v2`) to re-score candidate chunks for high-precision context selection.
* 🤖 **Gemini 3.6 Flash Integration**: Fast LLM generation backed by strict grounding templates to eliminate hallucinations, complete with exponential backoff handling for server load spikes.
* 📚 **Source & Page Citations**: Formats all factual output assertions with clear `[Source X] (Page Y)` citations.
* ⚡ **FastAPI REST API**: Asynchronous API server with structured Pydantic schemas and interactive Swagger UI documentation.
* 🤖 **Agentic Tool Routing**: Intelligent workflow node using LangGraph concepts to handle domain routing and fallback logic.
* 📊 **Automated CI Evaluation**: Benchmark engine computing Recall@K and Mean Reciprocal Rank (MRR) over ground-truth evaluation datasets in GitHub Actions.
* 🖥️ **Streamlit Chat Interface**: Web UI featuring chat history, dynamic response tuning, and citation breakdown.
* 🐳 **Multi-Container Docker Stack**: Dual-container setup (`FastAPI` backend + `Streamlit` frontend) orchestrated seamlessly via `docker-compose`.

---

## 🛠️ Tech Stack

**Python · PyMuPDF · Sentence Transformers · ChromaDB · BM25 · Cross-Encoder · Google Gemini API · FastAPI · LangChain/LangGraph · Streamlit · Docker & Docker Compose · GitHub Actions**

---

## 📁 Project Structure

```text
Lawsaathi/
├── .github/
│   └── workflows/
│       └── test.yml            # GitHub Actions CI/CD workflow
├── chroma_db/                  # Local persistent ChromaDB vector store
├── data/
│   ├── processed/
│   │   └── chunks.json         # Processed chunks and metadata index cache
│   └── raw/
│       └── constitution_of_india.pdf  # Raw legal PDF documents
├── src/
│   ├── api/
│   │   ├── app.py              # FastAPI application server & routes
│   │   └── schemas.py          # Pydantic API request/response models
│   ├── agents/
│   │   ├── law_agent.py        # LangGraph workflow router node
│   │   └── tools.py            # LangChain wrapped retrieval tools
│   ├── evaluation/
│   │   └── evaluate_retrieval.py # Automated Recall@K & MRR evaluation engine
│   ├── ingestion/
│   │   ├── build_vector_db.py  # Multi-document ingestion script
│   │   └── chunker.py          # TOC-filtering & layout-aware text splitter
│   ├── llm/
│   │   └── gemini.py           # Gemini 3.6 Flash client integration
│   ├── rag/
│   │   ├── pipeline.py         # Re-ranked hybrid retrieval pipeline
│   │   └── prompt.py           # Strict legal prompt grounding templates
│   ├── retrieval/
│   │   └── search.py           # Standalone hybrid search module
│   ├── ui/
│   │   └── app.py              # Streamlit web application interface
│   └── main.py                 # Interactive CLI entry point
├── tests/
│   ├── eval_dataset.json       # Ground-truth retrieval benchmark dataset
│   └── test_agent.py          # Agent routing test suite
├── .dockerignore
├── .env
├── .gitignore
├── Dockerfile                  # CPU-optimized Docker build spec
├── docker-compose.yml          # Multi-container orchestration spec
├── README.md
└── requirements.txt
```

---

## ⚙️ Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Lawsaathi.git
cd Lawsaathi
```

### 2. Create and Activate Virtual Environment

Create the environment:

```bash
python -m venv .venv
```

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not commit `.env` or expose your API key publicly.

---

## ▶️ Execution & Usage

### 1. Build the Vector Database

Ingest, clean, chunk, embed, and index the PDF documents stored in `data/raw/`:

```bash
python src/ingestion/build_vector_db.py
```

### 2. Run Retrieval Benchmark Evaluation

Evaluate retrieval performance using Recall@K and MRR:

```bash
python src/evaluation/evaluate_retrieval.py
```

### 3. Launch the FastAPI REST API

```bash
uvicorn src.api.app:app --reload
```

**API:** `http://127.0.0.1:8000`

**Swagger Documentation:** `http://127.0.0.1:8000/docs`

### 4. Launch the Streamlit Web Interface

```bash
streamlit run src/ui/app.py
```

**UI:** `http://localhost:8501`

---

## 🐳 Docker Deployment

LawSaathi can be run as a multi-container application using Docker Compose.

### Start the Full Stack

```bash
docker compose up --build
```

This starts:

* **FastAPI backend**
* **Streamlit frontend**

### Access the Services

* 🌐 **Streamlit UI:** `http://localhost:8501`
* ⚡ **FastAPI API:** `http://localhost:8000`
* 📖 **Swagger Docs:** `http://localhost:8000/docs`

### Stop the Stack

```bash
docker compose down
```

---

## 🧪 CI/CD Pipeline

The repository includes automated testing through **GitHub Actions** using `.github/workflows/test.yml`.

The CI workflow runs on pushes and pull requests targeting the `main` branch.

The workflow:

1. Sets up a Python 3.11 environment on Ubuntu.
2. Installs the required dependencies.
3. Builds the ChromaDB vector index from the legal document corpus.
4. Runs the retrieval evaluation pipeline.
5. Executes automated tests.
6. Verifies the project before changes are merged.

---

## 🌱 Open Source

LawSaathi is developed as an **open-source project** to explore practical Generative AI, RAG, information retrieval, agentic AI, API development, evaluation, and deployment concepts.

The project emphasizes:

* Modular architecture
* Reproducible experiments
* Hybrid retrieval
* Retrieval evaluation
* Source-grounded generation
* Agentic workflows
* Automated testing
* Containerized deployment
* Clear documentation

Contributions, issues, and suggestions are welcome.

---

## ⚠️ Disclaimer

LawSaathi is an educational and research project and **does not provide formal legal advice**.

AI-generated responses should not be treated as a substitute for advice from a qualified legal professional. Legal information should always be verified against authoritative sources and official statutory publications.