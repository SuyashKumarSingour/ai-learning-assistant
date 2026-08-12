from app.clients.qdrant_client import client


points, next_page = client.scroll(
    collection_name="document_chunks",
    limit=20,
    with_payload=True,
    with_vectors=False,
)


print("Number of points:", len(points))

for point in points:
    print("\nID:", point.id)
    print("Payload:", point.payload)