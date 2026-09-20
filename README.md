\# UniGuide AI — RAG-Powered University Information Assistant



\## 1. Overview



UniGuide AI is a Retrieval-Augmented Generation (RAG) application that answers questions about university policies, academic regulations, student procedures, and student support information.



The system retrieves relevant information from a collection of university documents and uses a local Large Language Model (LLM) through Ollama to generate grounded answers with source references.



The project was developed as a local Windows application using a FastAPI backend and a Streamlit frontend.



\### Main Features



\* Retrieval-Augmented Generation (RAG)

\* PDF document processing

\* Text chunking with overlap

\* Sentence Transformer embeddings

\* ChromaDB vector store

\* Local LLM generation using Ollama

\* Source/citation information in responses

\* FastAPI REST API

\* Streamlit chat interface

\* API validation and automated tests

\* Evaluation using 10 representative questions



\---



\## 2. Architecture



```text

&#x20;                   ┌─────────────────────┐

&#x20;                   │   Streamlit UI      │

&#x20;                   │   localhost:8501    │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                              │ HTTP POST /query

&#x20;                              ▼

&#x20;                   ┌─────────────────────┐

&#x20;                   │    FastAPI Backend  │

&#x20;                   │   localhost:8000    │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                ┌─────────────┴─────────────┐

&#x20;                │                           │

&#x20;                ▼                           ▼

&#x20;       ┌─────────────────┐         ┌─────────────────┐

&#x20;       │ Retrieval       │         │ Generation      │

&#x20;       │ Service         │         │ Service         │

&#x20;       └────────┬────────┘         └────────┬────────┘

&#x20;                │                           │

&#x20;                ▼                           ▼

&#x20;       ┌─────────────────┐         ┌─────────────────┐

&#x20;       │ ChromaDB        │         │ Ollama          │

&#x20;       │ Vector Store    │         │ Llama 3         │

&#x20;       └────────┬────────┘         └─────────────────┘

&#x20;                │

&#x20;                ▼

&#x20;       ┌─────────────────┐

&#x20;       │ Document        │

&#x20;       │ Embeddings      │

&#x20;       │ all-MiniLM-L6-v2│

&#x20;       └─────────────────┘



Document Pipeline:



PDF Documents

&#x20;    │

&#x20;    ▼

PDF Text Extraction

&#x20;    │

&#x20;    ▼

Recursive Character Chunking

&#x20;    │

&#x20;    ▼

Embeddings

&#x20;    │

&#x20;    ▼

ChromaDB

```



\---



\## 3. Tech Stack



| Technology            | Purpose                     |

| --------------------- | --------------------------- |

| Python 3.11           | Main programming language   |

| FastAPI               | Backend REST API            |

| Uvicorn               | FastAPI server              |

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



\### RAG Configuration



\* Chunking method: Recursive Character Text Splitting

\* Chunk size: 500 characters

\* Chunk overlap: 50 characters

\* Embedding model: `all-MiniLM-L6-v2`

\* Vector database: ChromaDB

\* LLM: `llama3:latest`

\* Retrieval top-k: 5



\---



\## 4. Project Structure



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

│   │   │   └── logging\_config.py

│   │   └── main.py

│   │

│   ├── tests/

│   │   └── test\_query.py

│   │

│   ├── data/

│   │   └── vector\_store/

│   │

│   ├── requirements.txt

│   ├── .env.example

│   ├── Dockerfile

│   └── pytest.ini

│

├── frontend/

│   ├── app.py

│   ├── api\_client.py

│   └── requirements.txt

│

├── data/

│   ├── phase1\_data\_verification.txt

│   └── rag\_evaluation.csv

│

├── notebooks/

│   └── rag\_pipeline.ipynb

│

├── src/

│   └── extract\_pdfs.py

│

├── .gitignore

├── verify\_pdfs.py

└── README.md

```



The raw PDF corpus, processed text files, local environment files, virtual environments, and persisted vector store are excluded from GitHub.



\---



\## 5. Domain and Data



The project focuses on university academic and student-support information.



The document collection includes materials related to:



\* Student Charter

\* Undergraduate Academic Regulations

\* Student Attendance Policy

\* Academic Misconduct Procedure

\* Academic Appeal Procedure

\* Student Complaints Procedure

\* Personal Academic Tutor Policy

\* Reasonable Adjustments Procedure

\* Early Identification of At-Risk Students and Support of Weak Students Protocol

\* BUE Student Academic Handbook



The documents are used as the knowledge base for the RAG pipeline.



\### Raw Corpus



The original PDF documents are not committed to this repository.



They should be obtained from the official British University in Egypt (BUE) sources and placed locally in:



```text

data/raw/

```



The extracted/processed text files should be placed in:



```text

data/processed/

```



The raw and processed data directories are excluded by `.gitignore`.



\### Rebuilding the Knowledge Base



After obtaining the documents, the PDF extraction and RAG pipeline can be used to extract text, create chunks, generate embeddings, and persist the ChromaDB vector store.



The RAG pipeline notebook is located at:



```text

notebooks/rag\_pipeline.ipynb

```



The vector store is generated locally at:



```text

backend/data/vector\_store/uniguide\_chroma

```



The vector store is intentionally excluded from GitHub and can be rebuilt from the source documents.



\---



\## 6. Environment Variables



\### Backend



Create:



```text

backend/.env

```



using `backend/.env.example` as a template.



| Variable            | Example                             | Description                   |

| ------------------- | ----------------------------------- | ----------------------------- |

| `OLLAMA\_HOST`       | `http://127.0.0.1:11434`            | Ollama server address         |

| `OLLAMA\_MODEL`      | `llama3:latest`                     | Local LLM used for generation |

| `CHROMA\_PATH`       | `data/vector\_store/uniguide\_chroma` | ChromaDB storage path         |

| `CHROMA\_COLLECTION` | `uniguide\_documents`                | ChromaDB collection           |

| `EMBEDDING\_MODEL`   | `all-MiniLM-L6-v2`                  | Embedding model               |

| `FRONTEND\_ORIGIN`   | `http://localhost:8501`             | Allowed frontend origin       |



\### Frontend



The Streamlit frontend uses:



```text

API\_BASE\_URL=http://localhost:8000

```



The `.env` file is not committed to GitHub.



\---



\## 7. Backend Setup



\### Requirements



Install:



\* Python 3.10 or later

\* Ollama

\* Git



\### 7.1 Open the project



```powershell

cd D:\\rag-assistant-project

```



\### 7.2 Create the backend virtual environment



```powershell

cd backend

python -m venv .venv

```



Activate it:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



\### 7.3 Install dependencies



```powershell

pip install -r requirements.txt

```



\### 7.4 Configure environment variables



Copy:



```text

backend/.env.example

```



to:



```text

backend/.env

```



Then configure the required values.



\### 7.5 Check Ollama



Make sure Ollama is installed and running.



Check the available models:



```powershell

ollama list

```



The project uses:



```text

llama3:latest

```



If it is not installed:



```powershell

ollama pull llama3:latest

```



\### 7.6 Start the FastAPI backend



From:



```text

D:\\rag-assistant-project\\backend

```



run:



```powershell

uvicorn app.main:app --reload

```



The backend will run at:



```text

http://localhost:8000

```



Swagger API documentation:



```text

http://localhost:8000/docs

```



\---



\## 8. Frontend Setup



Open another PowerShell window.



Go to:



```powershell

cd D:\\rag-assistant-project\\frontend

```



\### 8.1 Create the frontend virtual environment



```powershell

python -m venv .venv

```



Activate it:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



\### 8.2 Install dependencies



```powershell

pip install -r requirements.txt

```



\### 8.3 Configure the backend URL



Create:



```text

frontend/.env

```



with:



```env

API\_BASE\_URL=http://localhost:8000

```



\### 8.4 Start Streamlit



Run:



```powershell

streamlit run app.py

```



The frontend will normally be available at:



```text

http://localhost:8501

```



\---



\## 9. API Reference



\### GET `/health`



Checks whether the backend is running.



Request:



```text

GET http://localhost:8000/health

```



Example response:



```json

{

&#x20; "status": "healthy"

}

```



\---



\### POST `/query`



Sends a question to the RAG system.



Request:



```json

{

&#x20; "question": "What are the rules for student attendance?"

}

```



Example response:



```json

{

&#x20; "answer": "According to the provided documents...",

&#x20; "sources": \[

&#x20;   "14\_UG Academic Regulations 2024-2028 p.6",

&#x20;   "09\_Student Attendance Policy p.3",

&#x20;   "09\_Student Attendance Policy p.4"

&#x20; ]

}

```



The response contains the generated answer and the retrieved document sources.



\---



\## 10. cURL Example



\### Health check



```powershell

curl http://localhost:8000/health

```



\### Query



On Windows PowerShell:



```powershell

curl.exe -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d "{\\"question\\":\\"What are the rules for student attendance?\\"}"

```



\---



\## 11. Testing



The backend includes automated tests for:



1\. A valid query

2\. Invalid

