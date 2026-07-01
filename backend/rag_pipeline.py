import os
import fitz  # PyMuPDF
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai
from typing import List, Dict, Any

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
COLLECTION_NAME = "company_policies"

SYSTEM_PROMPT = (
    "You are a helpful HR and Company Policy Assistant. "
    "Answer questions strictly based on the provided company policy documents. "
    "If the answer is not found in the documents, say: "
    "'I could not find this information in the available policy documents. "
    "Please contact HR directly.' "
    "Always cite the source document and page number at the end of your answer. "
    "Be concise, professional, and friendly."
)


def get_chroma_client():
    client = chromadb.PersistentClient(
        path=CHROMA_PATH,
        settings=Settings(anonymized_telemetry=False),
    )
    return client


def get_or_create_collection():
    client = get_chroma_client()
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    return collection


def extract_text_from_pdf(file_bytes: bytes) -> List[Dict[str, Any]]:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        if text.strip():
            pages.append({"text": text, "page_number": page_num + 1})
    doc.close()
    return pages


def chunk_pages(pages: List[Dict[str, Any]], chunk_size: int = 1000, overlap: int = 200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = []
    for page_data in pages:
        texts = splitter.split_text(page_data["text"])
        for idx, text in enumerate(texts):
            chunks.append({
                "text": text,
                "page_number": page_data["page_number"],
                "chunk_index": idx,
            })
    return chunks


def get_embedding(text: str) -> List[float]:
    result = genai.embed_content(
        model="models/gemini-embedding-2",
        content=text,
        task_type="retrieval_document",
    )
    return result["embedding"]


def get_query_embedding(text: str) -> List[float]:
    result = genai.embed_content(
        model="models/gemini-embedding-2",
        content=text,
        task_type="retrieval_query",
    )
    return result["embedding"]


def ingest_pdf(file_bytes: bytes, filename: str) -> int:
    pages = extract_text_from_pdf(file_bytes)
    chunks = chunk_pages(pages)
    collection = get_or_create_collection()

    ids, embeddings, documents, metadatas = [], [], [], []

    for i, chunk in enumerate(chunks):
        chunk_id = f"{filename}__chunk_{i}"
        embedding = get_embedding(chunk["text"])
        ids.append(chunk_id)
        embeddings.append(embedding)
        documents.append(chunk["text"])
        metadatas.append({
            "filename": filename,
            "page_number": chunk["page_number"],
            "chunk_index": chunk["chunk_index"],
        })

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )
    return len(chunks)


def retrieve_relevant_chunks(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    collection = get_or_create_collection()
    total = collection.count()
    if total == 0:
        return []
    query_embedding = get_query_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, total),
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    if results["documents"] and results["documents"][0]:
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            chunks.append({
                "text": doc,
                "filename": meta.get("filename", "unknown"),
                "page_number": meta.get("page_number", 0),
                "score": 1 - dist,
            })
    return chunks


def build_prompt(query: str, context_chunks: List[Dict], chat_history: List[Dict]) -> str:
    context_text = "\n\n---\n\n".join(
        f"[Source: {c['filename']}, Page {c['page_number']}]\n{c['text']}"
        for c in context_chunks
    )

    history_text = ""
    for msg in chat_history[-6:]:
        role = "Employee" if msg["role"] == "user" else "Assistant"
        history_text += f"{role}: {msg['content']}\n"

    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"## Retrieved Policy Context:\n{context_text}\n\n"
        f"## Conversation History:\n{history_text}\n"
        f"## Current Question:\nEmployee: {query}\nAssistant:"
    )
    return prompt


def generate_answer(query: str, chat_history: List[Dict]) -> Dict[str, Any]:
    context_chunks = retrieve_relevant_chunks(query)

    if not context_chunks:
        return {
            "answer": "I could not find this information in the available policy documents. Please contact HR directly.",
            "sources": [],
        }

    prompt = build_prompt(query, context_chunks, chat_history)
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    seen = set()
    sources = []
    for chunk in context_chunks:
        key = (chunk["filename"], chunk["page_number"])
        if key not in seen:
            seen.add(key)
            sources.append({"file": chunk["filename"], "page": chunk["page_number"]})

    return {
        "answer": response.text,
        "sources": sources,
    }


def get_indexed_documents() -> List[str]:
    collection = get_or_create_collection()
    if collection.count() == 0:
        return []
    results = collection.get(include=["metadatas"])
    filenames = list({m["filename"] for m in results["metadatas"] if "filename" in m})
    return sorted(filenames)


def clear_collection():
    client = get_chroma_client()
    client.delete_collection(COLLECTION_NAME)
    client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
