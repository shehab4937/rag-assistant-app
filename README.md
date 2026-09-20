# UniGuide AI — RAG-Powered University Information Assistant

UniGuide AI is a **Retrieval-Augmented Generation (RAG)** application that answers questions about university policies, academic regulations, student procedures, and student support information.

The system retrieves relevant information from a collection of university documents and uses a local Large Language Model (LLM) through **Ollama** to generate grounded answers with document source references.

The project was developed as a local Windows application using a **FastAPI backend** and a **Streamlit frontend**.

---

## 1. Overview

### Main Features

* Retrieval-Augmented Generation (RAG)
* PDF document processing
* Text chunking with overlap
* Sentence Transformer embeddings
* ChromaDB vector store
* Local LLM generation using Ollama
* Source references in generated answers
* FastAPI REST API
* Streamlit chat interface
* Request validation
* Automated backend tests
* Evaluation using 10 representative questions
* Local and reproducible development setup

---

## 2. Architecture

```text
                         ┌─────────────────────┐
                         │    Streamlit UI      │
                         │   localhost:8501     │
                         └──────────┬──────────┘
                                    │
                                    │ HTTP POST /query
                                    ▼
                         ┌─────────────────────┐
                         │   FastAPI Backend   │
                         │   localhost:8000    │
                         └──────────┬──────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
            ┌─────────────────┐           ┌─────────────────┐
            │ Retrieval       │           │ Generation      │
            │ Service         │           │ Service         │
            └────────┬────────┘           └────────┬────────┘
                     │                             │
                     ▼                             ▼
            ┌─────────────────┐           ┌─────────────────┐
            │ ChromaDB        │           │ Ollama          │
            │ Vector Store    │           │ Llama 3         │
            └────────┬────────┘           └─────────────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ Document        │
            │ Embeddings      │
            │ all-MiniLM-     │
            │ L6-v2           │
            └─────────────────┘
```

### Document Processing Pipeline

```text
PDF Documents
      │
      ▼
PDF Text Extraction
      │
      ▼
Recursive Character Chunking
      │
      ▼
Sentence Transformer Embeddings
      │
      ▼
ChromaDB Vector Store
      │
      ▼
Semantic Retrieval
      │
      ▼
Ollama + Llama 3
      │
      ▼
Grounded Answer + Sources
```

---

## 3. Technology Stack

| Technology            | Purpose                     |
| --------------------- | --------------------------- |
| Python 3.11           | Main programming language   |
| FastAPI               | Backend REST API            |
| Uvicorn               | FastAPI application server  |
| Streamlit             | Frontend chat interface     |
| ChromaDB              | Vector database             |
| Sentence Transformers | Text embeddings             |
| all-MiniLM-L6-v2      | Embedding model             |
| Ollama                | Local LLM runtime           |
| Llama 3               | Local language model        |
| Pydantic              | Request/response validation |
| PyPDF                 | PDF text extraction         |
| Pytest                | Backend testing             |
| HTTPX                 | API testing                 |
| Git                   | Version control             |
| GitHub                | Source-code hosting         |

### RAG Configuration

| Setting         | Value                              |
| --------------- | ---------------------------------- |
| Chunking method | Recursive Character Text Splitting |
| Chunk size      | 500 characters                     |
| Chunk overlap   | 50 characters                      |
| Embedding model | `all-MiniLM-L6-v2`                 |
| Vector database | ChromaDB                           |
| LLM             | `llama3:latest`                    |
| Retrieval top-k | 5                                  |

---

## 4. Project Structure

```text
rag-assistant-app/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── query.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── schemas/
│   │   │   └── query.py
│   │   ├── services/
│   │   │   ├── retrieval.py
│   │   │   └── generation.py
│   │   ├── utils/
│   │   │   └── logging_config.py
│   │   └── main.py
│   │
│   ├── tests/
│   │   └── test_query.py
│   │
│   ├── data/
│   │   └── vector_store/
│   │
│   ├── requirements.txt
│   ├── .env.example
│   ├── Dockerfile
│   └── pytest.ini
│
├── frontend/
│   ├── app.py
│   ├── api_client.py
│   └── requirements.txt
│
├── data/
│   ├── phase1_data_verification.txt
│   └── rag_evaluation.csv
│
├── notebooks/
│   └── rag_pipeline.ipynb
│
├── src/
│   └── extract_pdfs.py
│
├── docs/
│   └── screenshots/
│
├── .gitignore
├── verify_pdfs.py
└── README.md
```

The following files and directories are intentionally excluded from GitHub:

* Raw PDF documents
* Processed document files
* Virtual environments
* Environment variables
* ChromaDB vector store
* Python cache files
* Log files

---

## 5. Domain and Data

The project focuses on **university academic and student-support information**.

The document collection includes materials related to:

* Student Charter
* Undergraduate Academic Regulations
* Student Attendance Policy
* Academic Misconduct Procedure
* Academic Appeal Procedure
* Student Complaints Procedure
* Personal Academic Tutor Policy
* Reasonable Adjustments Procedure
* Early Identification of At-Risk Students and Support of Weak Students Protocol
* BUE Student Academic Handbook

These documents form the knowledge base used by the RAG pipeline.

### Raw Corpus

The original PDF documents are not committed to the repository.

They should be obtained from the official **British University in Egypt (BUE)** sources and placed locally in:

```text
data/raw/
```

Extracted and processed text should be placed in:

```text
data/processed/
```

Both directories are excluded by `.gitignore`.

### Rebuilding the Knowledge Base

After obtaining the source documents, the PDF extraction and RAG pipeline can be used to:

1. Extract text from the PDF documents.
2. Split the text into chunks.
3. Generate document embeddings.
4. Store the embeddings in ChromaDB.
5. Persist the local vector store.

The RAG pipeline notebook is located at:

```text
notebooks/rag_pipeline.ipynb
```

The local vector store is generated at:

```text
backend/data/vector_store/uniguide_chroma
```

The vector store is intentionally excluded from GitHub and can be rebuilt locally from the source documents.

---

## 6. Environment Variables

### Backend

Create:

```text
backend/.env
```

using:

```text
backend/.env.example
```

as a template.

| Variable            | Example                             | Description                   |
| ------------------- | ----------------------------------- | ----------------------------- |
| `OLLAMA_HOST`       | `http://127.0.0.1:11434`            | Ollama server address         |
| `OLLAMA_MODEL`      | `llama3:latest`                     | Local LLM used for generation |
| `CHROMA_PATH`       | `data/vector_store/uniguide_chroma` | ChromaDB storage path         |
| `CHROMA_COLLECTION` | `uniguide_documents`                | ChromaDB collection name      |
| `EMBEDDING_MODEL`   | `all-MiniLM-L6-v2`                  | Embedding model               |
| `FRONTEND_ORIGIN`   | `http://localhost:4200`             | Allowed frontend origin       |

### Frontend

Create:

```text
frontend/.env
```

with:

```env
API_BASE_URL=http://localhost:8000
```

Environment files are not committed to GitHub.

---

## 7. Backend Setup

### Requirements

Install the following:

* Python 3.10 or later
* Ollama
* Git

### 7.1 Open the Project

```powershell
cd D:\rag-assistant-project
```

### 7.2 Create the Backend Virtual Environment

```powershell
cd backend
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 7.3 Install Dependencies

```powershell
pip install -r requirements.txt
```

### 7.4 Configure Environment Variables

Create:

```text
backend/.env
```

using `.env.example` as the template.

Configure the required values described in the Environment Variables section.

### 7.5 Check Ollama

Make sure Ollama is installed and running.

Check the available models:

```powershell
ollama list
```

The project uses:

```text
llama3:latest
```

If the model is not installed:

```powershell
ollama pull llama3:latest
```

### 7.6 Start the FastAPI Backend

From:

```text
D:\rag-assistant-project\backend
```

run:

```powershell
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

---

## 8. Frontend Setup

Open another PowerShell window.

### 8.1 Open the Frontend Directory

```powershell
cd D:\rag-assistant-project\frontend
```

### 8.2 Create the Frontend Virtual Environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 8.3 Install Dependencies

```powershell
pip install -r requirements.txt
```

### 8.4 Configure the Backend URL

Create:

```text
frontend/.env
```

with:

```env
API_BASE_URL=http://localhost:8000
```

### 8.5 Start Streamlit

Run:

```powershell
streamlit run app.py
```

The frontend will normally be available at:

```text
http://localhost:8501
```

---

## 9. API Reference

### GET `/health`

Checks whether the backend is running.

Request:

```text
GET http://localhost:8000/health
```

Example response:

```json
{
  "status": "healthy"
}
```

### POST `/query`

Sends a question to the RAG system.

Request:

```json
{
  "question": "What are the rules for student attendance?"
}
```

Example response:

```json
{
  "answer": "According to the provided documents...",
  "sources": [
    "14_UG Academic Regulations 2024-2028 p.6",
    "09_Student Attendance Policy p.3",
    "09_Student Attendance Policy p.4"
  ]
}
```

The response contains:

* The generated answer
* The retrieved document sources

---

## 10. cURL Examples

### Health Check

```powershell
curl http://localhost:8000/health
```

### Query

On Windows PowerShell:

```powershell
curl.exe -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d "{\"question\":\"What are the rules for student attendance?\"}"
```

---

## 11. Testing

The backend includes automated tests covering:

1. Valid query handling
2. Invalid request validation

Run the tests from the backend directory:

```powershell
pytest
```

Current test result:

```text
2 passed
```

The tests verify that:

* A valid question returns HTTP 200.
* The response contains an answer.
* The response contains a sources list.
* Invalid input is rejected with HTTP 422.

---

## 12. Evaluation

The RAG system was evaluated using **10 representative questions** covering the main document categories.

The evaluation questions include:

1. What are the rules for student attendance?
2. What is academic misconduct?
3. How can a student make an academic appeal?
4. How can a student submit a complaint?
5. What support is available for weak students?
6. What is the role of the Personal Academic Tutor?
7. What reasonable adjustments can students receive?
8. What are the academic regulations for undergraduate students?
9. What are the consequences of academic misconduct?
10. Where can students find important academic information?

The evaluation data is stored in:

```text
data/rag_evaluation.csv
```

The evaluation records retrieved sources and generated answers. Retrieval relevance, groundedness, and correctness were left for manual verification rather than being reported as automated accuracy metrics.

---

## 13. System Workflow

The complete UniGuide AI workflow is:

```text
User Question
      │
      ▼
Streamlit Frontend
      │
      │ POST /query
      ▼
FastAPI Backend
      │
      ▼
Query Validation
      │
      ▼
ChromaDB Retrieval
      │
      ▼
Relevant Document Chunks
      │
      ▼
Ollama + Llama 3
      │
      ▼
Generated Grounded Answer
      │
      ▼
Document Sources
      │
      ▼
Streamlit Response
```

---

## 14. Screenshots

Project screenshots are available in:

```text
docs/screenshots/
```

The screenshots demonstrate the user interface, generated answers, and retrieved document sources.

### Question 1

* `uniguide-home.png`
* `uniguide-answer.png`
* `uniguide-sources.png`

### Question 2

* `Screenshot 2026-09-20 170335.png`
* `Screenshot 2026-09-20 170357.png`

### Question 3

* `Screenshot 2026-09-20 170535.png`
* `Screenshot 2026-09-20 170549.png`
* `Screenshot 2026-09-20 170630.png`

---

## 15. Limitations

* The system depends on the quality and completeness of the source documents.
* The original PDF corpus is not included in the GitHub repository.
* The ChromaDB vector store must be rebuilt when setting up the project from scratch.
* Local LLM responses may vary slightly between executions.
* Some PDF documents may contain formatting or text-extraction issues.
* Evaluation correctness and groundedness require manual verification.

---

## 16. Reproducibility

To reproduce the project on another Windows machine:

1. Clone the repository.
2. Install Python 3.10 or later.
3. Install Git.
4. Install and run Ollama.
5. Pull the `llama3:latest` model.
6. Download the required university PDF documents from the official BUE sources.
7. Place the documents in `data/raw/`.
8. Run the PDF extraction and RAG pipeline.
9. Rebuild the ChromaDB vector store.
10. Create the backend `.env` file.
11. Create the frontend `.env` file.
12. Install backend dependencies.
13. Install frontend dependencies.
14. Start the FastAPI backend.
15. Start the Streamlit frontend.
16. Open the Streamlit application in a browser.

---

## 17. Project Status

The current implementation includes:

* Complete RAG pipeline
* PDF document processing
* Text chunking
* Sentence Transformer embeddings
* ChromaDB vector store
* Local Llama 3 generation through Ollama
* FastAPI backend
* Streamlit frontend
* API request validation
* Automated backend tests
* 10-question evaluation dataset
* Source references in generated answers
* Project screenshots
* GitHub repository
* Reproducibility documentation

---

## Repository

GitHub:

https://github.com/shehab4937/rag-assistant-app
