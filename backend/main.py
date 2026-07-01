import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import (
    ChatRequest, ChatResponse, IngestResponse,
    DocumentListResponse, HealthResponse, SourceReference,
)
import rag_pipeline

app = FastAPI(title="Company Policy Chatbot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health_check():
    collection = rag_pipeline.get_or_create_collection()
    return HealthResponse(status="ok", chroma_collection_count=collection.count())


@app.post("/ingest", response_model=IngestResponse)
async def ingest_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")
    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    try:
        chunks_indexed = rag_pipeline.ingest_pdf(file_bytes, file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
    return IngestResponse(
        status="success",
        chunks_indexed=chunks_indexed,
        filename=file.filename,
    )


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    try:
        history = [m.dict() for m in request.chat_history]
        result = rag_pipeline.generate_answer(request.query, history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")
    sources = [SourceReference(file=s["file"], page=s["page"]) for s in result["sources"]]
    return ChatResponse(answer=result["answer"], sources=sources)


@app.get("/documents", response_model=DocumentListResponse)
def list_documents():
    docs = rag_pipeline.get_indexed_documents()
    return DocumentListResponse(documents=docs)


@app.delete("/documents")
def clear_documents():
    try:
        rag_pipeline.clear_collection()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clear failed: {str(e)}")
    return {"status": "success", "message": "Knowledge base cleared."}
