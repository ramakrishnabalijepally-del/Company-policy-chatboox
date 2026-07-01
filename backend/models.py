from pydantic import BaseModel
from typing import List, Optional


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    query: str
    chat_history: Optional[List[ChatMessage]] = []


class SourceReference(BaseModel):
    file: str
    page: int


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceReference]


class IngestResponse(BaseModel):
    status: str
    chunks_indexed: int
    filename: str


class DocumentListResponse(BaseModel):
    documents: List[str]


class HealthResponse(BaseModel):
    status: str
    chroma_collection_count: int
