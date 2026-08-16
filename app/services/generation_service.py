import time

from google.genai.errors import ServerError

from app.clients.google_client import client
from app.config import settings


def generate_answer(
    question: str,
    context: str,
) -> str:

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

    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return response.text

        except ServerError as error:
            # Gemini 503 errors are often temporary.
            if attempt == max_attempts - 1:
                raise RuntimeError(
                    "The AI service is temporarily unavailable. "
                    "Please try again in a moment."
                ) from error

            # Wait 2 seconds, then 4 seconds before retrying.
            wait_seconds = 2 ** (attempt + 1)
            time.sleep(wait_seconds)