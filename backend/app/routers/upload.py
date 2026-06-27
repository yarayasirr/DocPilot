import os
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.pdf_service import extract_text_from_pdf
from app.services.text_splitter import split_text_into_chunks

router = APIRouter()

UPLOAD_DIR = "uploads"


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Check if the uploaded file is a PDF
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Create uploads folder if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save the uploaded PDF
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from the PDF
    extracted_text = extract_text_from_pdf(file_path)

    # Split the extracted text into chunks
    chunks = split_text_into_chunks(extracted_text)

    # Return a preview
    return {
        "message": "File uploaded, text extracted, and chunks created successfully",
        "filename": file.filename,
        "path": file_path,
        "text_preview": extracted_text[:500],
        "chunk_count": len(chunks),
        "first_chunk": chunks[0] if chunks else ""
    }