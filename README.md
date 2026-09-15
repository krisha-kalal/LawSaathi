# LawSaathi ⚖️

**LawSaathi** is an open-source, full-stack AI-powered legal question-answering system built using **Retrieval-Augmented Generation (RAG)**. It processes legal documents like the Constitution of India, retrieves relevant statutory provisions, and generates grounded answers with exact source citations.

The project focuses on building and evaluating modern RAG architecture concepts including **layout-aware text cleaning, dense vector embeddings, ChromaDB, BM25 keyword search, hybrid retrieval, Cross-Encoder re-ranking, LLM prompt grounding, REST APIs, agentic tool routing, automated retrieval evaluation, Docker containerization, and a Streamlit web interface**.

## 🚀 Features

* 📄 **Layout-Aware PDF Ingestion**: Text extraction using PyMuPDF with automated Table of Contents (TOC) dot-leader filtering and Devanagari/Hindi script stripping.
* ✂️ **Overlapping Parent Chunking**: Structured text splitting to preserve statutory context boundaries.
* 🔎 **Dense Semantic Search**: Vector embeddings generated via `all-MiniLM-L6-v2` stored in ChromaDB.
* 🔤 **Sparse BM25 Search**: Keyword-based retrieval via `rank_bm25` to capture exact statutory numbers and terms.
* 🔀 **Hybrid Retrieval Pipeline**: Combines dense semantic vectors and sparse BM25 scores.
* 🎯 **Two-Stage Re-Ranking**: Employs a Cross-Encoder (`ms-marco-MiniLM-L-6-v2`) to re-score candidates for high-precision context selection.
* 🤖 **Gemini 3.6 Flash Integration**: Fast LLM generation constrained by strict grounding rules to eliminate hallucinations.
* 📚 **Source & Page Citations**: Formats all factual assertions with clear `[Source X] (Page Y)` citations.
* ⚡ **FastAPI REST API**: Asynchronous API server with structured Pydantic schemas and interactive Swagger UI documentation.
* 🤖 **Agentic Tool Routing**: Intelligent workflow node using LangChain/LangGraph concepts to route legal vs. non-legal queries.
* 📊 **Automated Evaluation Metrics**: Evaluation engine calculating Recall@K and Mean Reciprocal Rank (MRR) over benchmark query datasets.
* 🖥️ **Streamlit Chat Interface**: Web UI featuring chat history, page-level citation badges, and real-time retrieval parameter sliders.
* 🐳 **Production Polish & Docker**: Complete containerized environment with Dockerfile and GitHub Actions CI workflow setup.

## 🛠️ Tech Stack

**Python · PyMuPDF · Sentence Transformers · ChromaDB · BM25 · Cross-Encoder · Google Gemini API · FastAPI · LangChain/LangGraph · Streamlit · Docker · GitHub Actions**

## 📁 Project Structure

```text
Lawsaathi/
├── .github/
│   └── workflows/
│       └── test.yml            # GitHub Actions CI workflow
├── chroma_db/                  # Local persistent ChromaDB storage
├── data/
│   ├── processed/
│   │   └── chunks.json         # Text chunks and metadata index cache
│   └── raw/
│       └── constitution_of_india.pdf
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
│   │   ├── build_vector_db.py  # DB population script
│   │   └── chunker.py          # TOC-filtering & layout-aware text splitter
│   ├── llm/
│   │   └── gemini.py           # Gemini 3.6 Flash client integration
│   ├── rag/
│   │   ├── pipeline.py         # Re-ranked hybrid retrieval pipeline
│   │   └── prompt.py           # Strict legal prompt grounding templates
│   ├── retrieval/
│   │   └── search.py           # Isolated search debugging script
│   ├── ui/
│   │   └── app.py              # Streamlit web application interface
│   └── main.py                 # Interactive CLI entry point
├── tests/
│   ├── eval_dataset.json       # Ground-truth evaluation dataset
│   └── test_agent.py          # Agent routing test script
├── .env
├── .gitignore
├── Dockerfile                  # Containerization specification
├── README.md
└── requirements.txt

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Lawsaathi.git
cd Lawsaathi
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not commit `.env` or expose your API key publicly.

## ▶️ Execution & Usage

### 1. Build the Vector Database

Extract, clean, chunk, embed, and index the Constitution:

```bash
python src/ingestion/build_vector_db.py
```

### 2. Run the CLI Interface

Start the interactive legal question-answering system:

```bash
python src/main.py
```

### 3. Start the FastAPI Backend

Launch the REST API:

```bash
uvicorn src.api:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### 4. Start the Streamlit Interface

Launch the browser-based LawSaathi interface:

```bash
streamlit run src/ui/app.py
```

### 5. Run Retrieval Evaluation

Run the evaluation pipeline:

```bash
python tests/evaluate_retrieval.py
```

The evaluation compares retrieval approaches using:

* Recall@K
* Mean Reciprocal Rank (MRR)

### 6. Run with Docker

Build the Docker image:

```bash
docker build -t lawsaathi .
```

Run the container:

```bash
docker run -p 8000:8000 --env-file .env lawsaathi
```

## 🌱 Open Source

LawSaathi is developed as an **open-source project** to explore practical Generative AI, RAG, information retrieval, agentic AI, API development, evaluation, and deployment concepts.

The project emphasizes:

* Modular architecture
* Reproducible experiments
* Retrieval evaluation
* Source-grounded generation
* Automated testing
* Containerized deployment
* Clear documentation
* Incremental development

Contributions, issues, and suggestions are welcome.

## ⚠️ Disclaimer

LawSaathi is an educational and research project and **does not provide formal legal advice**.

AI-generated responses should not be treated as a substitute for advice from a qualified legal professional. Legal information should always be verified against authoritative sources and official statutory publications.