from qdrant_client.models import PointStruct

from app.clients.qdrant_client import client
from app.services.embedding_service import generate_embedding


text = "Python is a programming language."

vector = generate_embedding(text)


point = PointStruct(
    id=1,
    vector=vector,
    payload={
        "text": text,
        "source": "test",
    },
)


client.upsert(
    collection_name="document_chunks",
    points=[point],
)


print("Point inserted successfully.")