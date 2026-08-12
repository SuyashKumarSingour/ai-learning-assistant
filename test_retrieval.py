from app.services.retrieval_service import retrieve_chunks


query = "What is Python used for in artificial intelligence?"


results = retrieve_chunks(
    query=query,
    limit=3,
    document_id="0cde7147-ef27-4365-9b1f-5e85308ff2eb",
)


for result in results:
    print("\n--- Result ---")
    print("Score:", result.score)
    print("Chunk index:", result.payload["chunk_index"])
    print("Text:", result.payload["text"])