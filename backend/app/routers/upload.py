import os
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.pdf_service import extract_text_from_pdf
from app.services.text_splitter import split_text_into_chunks
from app.services.embedding_service import create_embeddings
from app.services.vector_store import store_chunks

router = APIRouter()

UPLOAD_DIR = "uploads"


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_path)

    chunks = split_text_into_chunks(extracted_text)

    embeddings = create_embeddings(chunks)

    stored_chunks = store_chunks(
        chunks=chunks,
        embeddings=embeddings,
        filename=file.filename
    )

    return {
        "message": "File uploaded, processed, and stored in vector database successfully",
        "filename": file.filename,
        "path": file_path,
        "text_preview": extracted_text[:500],
        "chunk_count": len(chunks),
        "embedding_count": len(embeddings),
        "stored_chunks": stored_chunks,
        "embedding_dimension": len(embeddings[0]) if embeddings else 0,
        "first_chunk": chunks[0] if chunks else "",
        "first_embedding_preview": embeddings[0][:5] if embeddings else []
    }