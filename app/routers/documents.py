from uuid import uuid4
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from app.auth.dependencies import get_current_user
from app.services.ingestion_service import ingest_document
from app.services.document_service import (
    create_document,
    list_documents,
    get_document,
    delete_document,
)
from app.services.retrieval_service import delete_document_chunks


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

    original_filename = file.filename

    safe_filename = f"{uuid4()}.pdf"
    file_path = UPLOAD_DIR / safe_filename

    with file_path.open("wb") as buffer:
        buffer.write(file_content)

    document_id = str(uuid4())

    try:
        result = ingest_document(
            str(file_path),
            user_id,
            document_id,
        )

        document = create_document(
            document_id=document_id,
            user_id=user_id,
            filename=original_filename,
            file_path=str(file_path),
            file_size=len(file_content),
            chunks_count=result["chunks_inserted"],
        )

    except ValueError as exc:
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail=f"Document upload failed: {str(exc)}",
        ) from exc

    return {
        "message": "Document uploaded and ingested successfully.",
        "document_id": document["id"],
        "chunks_inserted": result["chunks_inserted"],
    }


@router.get("/documents")
def get_documents(
    user_id: str = Depends(get_current_user),
):
    try:
        documents = list_documents(user_id)

        return {
            "documents": documents,
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve documents.",
        )


@router.get("/documents/{document_id}")
def get_document_by_id(
    document_id: str,
    user_id: str = Depends(get_current_user),
):
    try:
        document = get_document(
            document_id=document_id,
            user_id=user_id,
        )

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found.",
            )

        return {
            "document": document,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve document.",
        )


@router.delete("/documents/{document_id}")
def delete_document_by_id(
    document_id: str,
    user_id: str = Depends(get_current_user),
):
    try:
        document = get_document(
            document_id=document_id,
            user_id=user_id,
        )

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found.",
            )

        delete_document_chunks(
            document_id=document_id,
            user_id=user_id,
        )

        deleted = delete_document(
            document_id=document_id,
            user_id=user_id,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Document not found.",
            )

        return {
            "message": "Document deleted successfully.",
            "document_id": document_id,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to delete document.",
        )