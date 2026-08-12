from app.services.retrieval_service import retrieve_chunks
from app.services.generation_service import generate_answer


def answer_question(
    question: str,
    document_id: str | None = None,
) -> str:

    results = retrieve_chunks(
        query=question,
        limit=3,
        document_id=document_id,
    )

    context_parts = []

    for result in results:
        context_parts.append(result.payload["text"])

    context = "\n\n".join(context_parts)

    answer = generate_answer(
        question=question,
        context=context,
    )

    return answer