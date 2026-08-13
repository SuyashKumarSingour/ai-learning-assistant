from app.services.retrieval_service import retrieve_chunks


def test_retrieve_chunks():
    query = "What is Python used for in artificial intelligence?"

    results = retrieve_chunks(query, limit=3)

    assert len(results) > 0
    assert results[0].score > 0
    assert results[0].payload["text"]
    assert "chunk_index" in results[0].payload