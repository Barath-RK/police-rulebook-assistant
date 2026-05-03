from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import tempfile
import os

app = FastAPI(title="Police Rulebook Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory storage
uploaded_docs = []
doc_chunks = []

class Question(BaseModel):
    query: str

class Answer(BaseModel):
    answer: str
    sources: List[str]

@app.get("/")
def root():
    return {"message": "Police Rulebook Assistant API - Week 1", "status": "running"}

@app.get("/status")
def get_status():
    return {
        "status": "running",
        "documents_loaded": len(uploaded_docs)
    }

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    global uploaded_docs, doc_chunks
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Only PDF files are supported")
    
    # Read file content
    content = await file.read()
    text_content = content.decode('latin-1', errors='ignore')[:5000]  # First 5000 chars
    
    # Store document info
    uploaded_docs.append({
        "filename": file.filename,
        "content": text_content
    })
    
    # Create chunks (500 chars each)
    chunks = [text_content[i:i+500] for i in range(0, len(text_content), 450)]
    for i, chunk in enumerate(chunks):
        doc_chunks.append({
            "filename": file.filename,
            "chunk_id": i,
            "text": chunk
        })
    
    return {
        "message": f"Successfully uploaded {file.filename}",
        "chunks_created": len(chunks),
        "total_documents": len(uploaded_docs)
    }

@app.post("/ask", response_model=Answer)
async def ask_question(question: Question):
    global doc_chunks
    
    if not doc_chunks:
        raise HTTPException(400, "No documents uploaded yet. Please upload a PDF first.")
    
    # Simple keyword search
    query_words = question.query.lower().split()
    relevant_chunks = []
    
    for chunk in doc_chunks:
        chunk_text = chunk["text"].lower()
        # Count how many query words appear in chunk
        score = sum(1 for word in query_words if word in chunk_text)
        if score > 0:
            relevant_chunks.append((score, chunk))
    
    # Sort by relevance
    relevant_chunks.sort(reverse=True, key=lambda x: x[0])
    
    if not relevant_chunks:
        return Answer(
            answer="I couldn't find relevant information. Please try different keywords.",
            sources=[]
        )
    
    # Get top 2 chunks
    top_chunks = relevant_chunks[:2]
    answer_text = "Based on the police rulebook:\n\n"
    sources = []
    
    for score, chunk in top_chunks:
        answer_text += f"• {chunk['text'][:300]}...\n\n"
        sources.append(chunk['filename'])
    
    return Answer(answer=answer_text, sources=list(set(sources)))