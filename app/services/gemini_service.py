

from fastapi import HTTPException
from google.genai import types
from app.memory.conversation import conversation_history
from app.config import settings
from google import genai





client = genai.Client(api_key=settings.GEMINI_API_KEY)


def generate_response(user_message: str) -> str:
    try:

        conversation_history.append(
            {
                "role": "user",
                "message": user_message      # Changed from "parts" to "message"
            }
        )

        gemini_contents = convert_to_gemini(conversation_history)

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=gemini_contents,
        )

        conversation_history.append(
            {
                "role": "model",
                "message": response.text     # Changed from "parts" to "message"
            }
        )

        return response.text

    except Exception as e:

        print(f"Gemini error: {e}")

        raise HTTPException(
        status_code=500,
        detail="Unable to connect to Gemini."
    )


def convert_to_gemini(conversation_history):

    gemini_contents = []

    for message in conversation_history:

        content = types.Content(

            role=message["role"],

            parts=[
                types.Part.from_text(
                    text=message["message"]
                )
            ]
        )

        gemini_contents.append(content)

    return gemini_contents