from app.clients.google_client import client
from app.config import settings


def generate_answer(question: str, context: str) -> str:

    prompt = f"""
You are an AI learning assistant.

Answer the user's question using only the provided context.

If the answer cannot be found in the context, say:
"I couldn't find the answer in the provided documents."

Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
    )

    return response.text