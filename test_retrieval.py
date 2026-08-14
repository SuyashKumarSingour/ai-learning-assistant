from app.services.retrieval_service import retrieve_chunks


def test_retrieve_chunks():
    query = "What is Python used for in artificial intelligence?"
    user_id = "test-user-123"

    results = retrieve_chunks(
        query=query,
        user_id=user_id,
        limit=3,
    )

    assert len(results) > 0
    assert results[0].score > 0
    assert results[0].payload["text"]
    assert "chunk_index" in results[0].payload
    assert results[0].payload["user_id"] == user_id