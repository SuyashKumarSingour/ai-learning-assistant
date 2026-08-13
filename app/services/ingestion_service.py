from uuid import uuid4

from qdrant_client.models import PointStruct, VectorParams, Distance

from app.clients.qdrant_client import client
from app.services.extraction_service import extract_pdf
from app.services.chunking_service import chunk_text
from app.services.embedding_service import generate_embedding


COLLECTION_NAME = "document_chunks"
VECTOR_SIZE = 3072


def ingest_document(file_path: str) -> dict:

    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

    document_id = str(uuid4())

    text = extract_pdf(file_path)

    chunks = chunk_text(text)

    points = []

    for index, chunk in enumerate(chunks):

        vector = generate_embedding(chunk)

        point = PointStruct(
            id=str(uuid4()),
            vector=vector,
            payload={
                "document_id": document_id,
                "text": chunk,
                "source": file_path,
                "chunk_index": index,
            },
        )

        points.append(point)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    return {
        "document_id": document_id,
        "chunks_inserted": len(points),
    }