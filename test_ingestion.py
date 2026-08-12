from app.services.ingestion_service import ingest_document


file_path = "app/documents/python_language_5_pages.pdf"

result = ingest_document(file_path)

print("Ingestion result:", result)