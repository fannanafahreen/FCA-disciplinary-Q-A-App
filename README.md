# 📄 Ask My Documents — FCA Regulatory Q&A App

A Retrieval-Augmented Generation (RAG) application that lets users ask plain-English questions about FCA (Financial Conduct Authority) enforcement final notices and receive accurate, source-grounded answers — instead of manually reading through dozens of pages of regulatory PDFs.

Built as part of dissertation research into FCA enforcement outcomes, and as a hands-on project to gain practical experience with LLMs, RAG pipelines, and AWS cloud deployment.

**🔗 Live demo:** `http://13.50.243.141:8000` *(hosted on AWS EC2 free tier — may be taken down after the free tier period ends)*

---

## What it does

1. Ingests real FCA final notice PDFs (enforcement documents detailing fines against firms/individuals)
2. Splits documents into searchable chunks and converts them into vector embeddings
3. When a user asks a question, retrieves the most relevant chunks using semantic search
4. Passes those chunks to an LLM, which generates a natural-language answer **grounded only in the retrieved text** — with source citations
5. If the answer isn't in the source documents, the model says so rather than guessing

Example questions the app can answer:
- *"Which firms were fined for anti-money laundering failures?"*
- *"What was Nationwide Building Society fined for?"*
- *"Summarise the case against Barclays Bank Plc"*

---

## Architecture

```
PDF documents
     ↓
Text extraction (pypdf)
     ↓
Chunking (500-word overlapping segments)
     ↓
Embeddings (sentence-transformers: all-MiniLM-L6-v2)
     ↓
Vector index (FAISS)
     ↓
User question → semantic search → top-k relevant chunks
     ↓
Amazon Bedrock (Nova 2 Lite) → grounded answer generation
     ↓
FastAPI backend → HTML/JS frontend
```

**Deployment:** AWS EC2 (Ubuntu), with IAM role-based permissions granting the instance secure access to Amazon Bedrock — no hardcoded credentials.

---

## Tech stack

| Layer | Technology |
|---|---|
| PDF processing | `pypdf`, `cryptography` |
| Embeddings | `sentence-transformers` (all-MiniLM-L6-v2) |
| Vector search | `FAISS` |
| LLM inference | Amazon Bedrock (Nova 2 Lite) |
| Backend | FastAPI, Uvicorn |
| Frontend | HTML, CSS, vanilla JavaScript |
| Cloud infrastructure | AWS EC2, IAM, Security Groups |
| Local dev fallback | Ollama (llama3.2:1b) for offline/free local testing |

---

## Project structure

```
├── data/                     # Source PDF documents
├── extracted_text/           # Plain-text extracted from PDFs
├── download_data.py          # Downloads FCA final notice PDFs
├── extract_text.py           # Extracts text from PDFs
├── chunk_text.py              # Splits text into overlapping chunks
├── build_embeddings.py       # Generates embeddings + builds FAISS index
├── chunks.json                # All text chunks with source metadata
├── chunks_store.pkl           # Pickled chunk data for fast loading
├── faiss_index.bin            # Pre-built FAISS vector index
├── app.py                     # FastAPI backend (Bedrock-powered)
├── index.html                 # Frontend UI
└── .gitignore
```

---

## Running it locally

### Prerequisites
- Python 3.10+
- pip

### Setup

```bash
git clone https://github.com/fannanafahreen/FCA-disciplinary-Q-A-App.git
cd FCA-disciplinary-Q-A-App
pip install fastapi uvicorn sentence-transformers faiss-cpu boto3
```

### Option A: Run with Amazon Bedrock (as deployed)
Requires AWS credentials configured with Bedrock access (`boto3` will pick up credentials from your environment or an attached IAM role).

```bash
python -m uvicorn app:app --reload
```

### Option B: Run fully locally and free with Ollama
Swap the Bedrock call in `app.py` for a local Ollama model — no AWS account needed.

```bash
# Install Ollama: https://ollama.com/download
ollama pull llama3.2:1b
pip install ollama
```

Then visit `http://127.0.0.1:8000`

---

## Rebuilding the data pipeline (optional)

If you want to add your own documents:

```bash
python download_data.py      # or manually add PDFs to /data
python extract_text.py       # extract text from PDFs
python chunk_text.py         # chunk the text
python build_embeddings.py   # rebuild the FAISS index
```

---

## Key design decisions & lessons learned

- **Grounded answers over fluency**: the system prompt explicitly instructs the model to say "I don't have enough information" rather than hallucinate — verified by testing out-of-scope questions
- **Local-first development**: built and validated the full RAG pipeline locally before touching cloud infrastructure, isolating logic bugs from infrastructure bugs
- **Migrated from self-hosted to managed inference**: initially ran Ollama directly on the EC2 instance, but a t3.micro's 1GB RAM made LLM inference impractically slow (several minutes per response). Migrated to Amazon Bedrock, which reduced response times to seconds — a real-world lesson in matching infrastructure to workload
- **Security-conscious deployment**: uses IAM roles for AWS service permissions rather than hardcoded API keys; scoped security groups to only the required ports

---

## Future improvements

- [ ] Expand the document set beyond financial penalties (e.g. license revocations, public censures)
- [ ] Add a persistent, database-backed conversation history
- [ ] Move to a managed vector database (e.g. OpenSearch) for larger-scale document sets
- [ ] Add automated tests for the retrieval pipeline
- [ ] Set up an Elastic IP for a stable, permanent URL

---

## Author

[Fannana Fahreen](https://github.com/fannanafahreen)
