from app.services.rag_service import answer_question


question = "What is Python used for in artificial intelligence?"


answer = answer_question(
    question=question,
    document_id="0cde7147-ef27-4365-9b1f-5e85308ff2eb",
)


print("\n--- Answer ---")
print(answer)