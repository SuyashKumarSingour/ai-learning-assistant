from app.services.rag_service import answer_question


def test_answer_question():
    question = "What is Python used for in artificial intelligence?"
    user_id = "test-user-123"

    answer = answer_question(
        question=question,
        user_id=user_id,
    )

    assert answer
    assert isinstance(answer, str)