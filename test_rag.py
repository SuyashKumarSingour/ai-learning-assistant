from app.services.rag_service import answer_question


def test_answer_question():
    question = "What is Python used for in artificial intelligence?"

    answer = answer_question(question)

    assert answer
    assert isinstance(answer, str)