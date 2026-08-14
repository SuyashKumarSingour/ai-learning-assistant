from uuid import uuid4
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from app.auth.dependencies import get_current_user
from app.services.ingestion_service import ingest_document


router = APIRouter()

UPLOAD_DIR = Path("app/documents")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user),
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="A filename is required.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    file_content = await file.read()

    if not file_content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="The file size must not exceed 10 MB.",
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    safe_filename = f"{uuid4()}.pdf"
    file_path = UPLOAD_DIR / safe_filename

    with file_path.open("wb") as buffer:
        buffer.write(file_content)

    try:
        result = ingest_document(
            str(file_path),
            user_id,
        )
    except ValueError as exc:
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return {
        "message": "Document uploaded and ingested successfully.",
        "document_id": result["document_id"],
        "chunks_inserted": result["chunks_inserted"],
    }