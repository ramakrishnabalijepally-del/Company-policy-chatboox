# Company Policy Chatbot

A production-ready RAG chatbot for querying company policy documents using Google Gemini, ChromaDB, FastAPI, and Streamlit.

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.11+ |
| Docker & Docker Compose | Latest |
| Google AI Studio API Key | Required |

---

## Quick Start (Docker — Recommended)

### 1. Clone & configure
```bash
git clone <your-repo-url>
cd company-policy-chatbot
cp .env.example .env
# Edit .env and set your GOOGLE_API_KEY
```

### 2. Build and run
```bash
docker compose up --build
```

### 3. Open the app
- Frontend: http://localhost:8501
- Backend API docs: http://localhost:8000/docs

---

## Local Development (No Docker)

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt

set GOOGLE_API_KEY=your_key_here   # Windows
# export GOOGLE_API_KEY=your_key   # Mac/Linux
set CHROMA_PATH=../chroma_db

uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

set BACKEND_URL=http://localhost:8000
streamlit run app.py
```

### Generate sample policy PDFs
```bash
pip install fpdf2
python data/generate_sample_policies.py
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| POST | /ingest | Upload and index a PDF |
| POST | /chat | Query the chatbot |
| GET | /documents | List indexed documents |
| DELETE | /documents | Clear knowledge base |

### Example: Chat request
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "How many days of annual leave do I get?", "chat_history": []}'
```

---

## Deployment

### Build and push to Docker Hub
```bash
docker build -t yourdockerid/policy-backend ./backend
docker build -t yourdockerid/policy-frontend ./frontend
docker push yourdockerid/policy-backend
docker push yourdockerid/policy-frontend
```

### Google Cloud Run
```bash
# Backend
gcloud run deploy policy-backend \
  --image yourdockerid/policy-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=your_key,CHROMA_PATH=/tmp/chroma_db \
  --port 8000

# Frontend
gcloud run deploy policy-frontend \
  --image yourdockerid/policy-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars BACKEND_URL=https://your-backend-url \
  --port 8501
```

> Note: For persistent ChromaDB on Cloud Run, mount a Google Cloud Storage bucket or use Cloud SQL instead of the local filesystem.

### Railway (Easiest alternative)
1. Push code to GitHub
2. Go to railway.app → New Project → Deploy from GitHub
3. Add `GOOGLE_API_KEY` as an environment variable in the Railway dashboard
4. Deploy backend and frontend as separate services

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| GOOGLE_API_KEY | Google AI Studio API key | Yes |
| BACKEND_URL | URL of the FastAPI backend | Frontend only |
| CHROMA_PATH | Path to persist ChromaDB data | Backend only |

---

## Project Structure

```
company-policy-chatbot/
├── backend/
│   ├── main.py              # FastAPI app with all endpoints
│   ├── rag_pipeline.py      # PDF parsing, embedding, retrieval, generation
│   ├── models.py            # Pydantic request/response schemas
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app.py               # Streamlit chat UI
│   ├── requirements.txt
│   └── Dockerfile
├── data/
│   ├── policies/            # Place your PDF files here
│   └── generate_sample_policies.py
├── chroma_db/               # Auto-created: persisted vector store
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Getting a Google AI Studio API Key

1. Go to https://aistudio.google.com
2. Sign in with your Google account
3. Click "Get API Key" → "Create API key"
4. Copy the key and paste it into your `.env` file
