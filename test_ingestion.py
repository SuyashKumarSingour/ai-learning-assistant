from app.services.ingestion_service import ingest_document


def test_ingest_document():
    file_path = "app/documents/python_language_5_pages.pdf"
    user_id = "test-user-123"

    result = ingest_document(
        file_path,
        user_id,
    )

    assert result["document_id"]
    assert result["chunks_inserted"] > 0