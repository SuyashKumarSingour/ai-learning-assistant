from qdrant_client.models import Distance, VectorParams

from app.clients.qdrant_client import client


client.create_collection(
    collection_name="document_chunks",
    vectors_config=VectorParams(
        size=3072,
        distance=Distance.COSINE,
    ),
)

print("Collection created.")