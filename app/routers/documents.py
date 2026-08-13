from fastapi import APIRouter, UploadFile, File, HTTPException
import os

from app.services.ingestion_service import ingest_document


router = APIRouter()


@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    upload_dir = "app/documents"

    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    result = ingest_document(file_path)

    return {
        "message": "Document uploaded and ingested successfully.",
        "document_id": result["document_id"],
        "chunks_inserted": result["chunks_inserted"],
    }