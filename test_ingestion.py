from app.services.ingestion_service import ingest_document


def test_ingest_document():
    file_path = "app/documents/python_language_5_pages.pdf"

    result = ingest_document(file_path)

    assert result["document_id"]
    assert result["chunks_inserted"] > 0