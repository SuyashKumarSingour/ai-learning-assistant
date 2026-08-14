from app.clients.qdrant_client import client
from app.services.embedding_service import generate_embedding
from qdrant_client.models import Filter, FieldCondition, MatchValue


COLLECTION_NAME = "document_chunks"


def retrieve_chunks(
    query: str,
    user_id: str,
    limit: int = 3,
    document_id: str | None = None,
):

    query_vector = generate_embedding(query)

    conditions = [
        FieldCondition(
            key="user_id",
            match=MatchValue(value=user_id),
        )
    ]

    if document_id:
        conditions.append(
            FieldCondition(
                key="document_id",
                match=MatchValue(value=document_id),
            )
        )

    query_filter = Filter(
        must=conditions
    )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=query_filter,
        limit=limit,
        with_payload=True,
    )

    return results.points