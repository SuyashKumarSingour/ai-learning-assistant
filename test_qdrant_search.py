from app.clients.qdrant_client import client
from app.services.embedding_service import generate_embedding


query = "What is Python?"


query_vector = generate_embedding(query)


results = client.query_points(
    collection_name="document_chunks",
    query=query_vector,
    limit=1,
)


print(results)