from app.clients.qdrant_client import client
from app.services.embedding_service import generate_embedding
from qdrant_client.models import Filter, FieldCondition, MatchValue


COLLECTION_NAME = "document_chunks"


def retrieve_chunks(
    query: str,
    limit: int = 3,
    document_id: str | None = None,
):

    query_vector = generate_embedding(query)

    query_filter = None

    if document_id:
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchValue(value=document_id),
                )
            ]
        )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=query_filter,
        limit=limit,
        with_payload=True,
    )

    return results.points