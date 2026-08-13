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

    if not results:
        return "I could not find relevant information in the uploaded documents."

    context_parts = []

    for result in results:
        if result.payload and "text" in result.payload:
            context_parts.append(result.payload["text"])

    if not context_parts:
        return "I could not find relevant information in the uploaded documents."

    context = "\n\n".join(context_parts)

    answer = generate_answer(
        question=question,
        context=context,
    )

    return answer