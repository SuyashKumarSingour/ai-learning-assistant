import os

from google import genai
from dotenv import load_dotenv


load_dotenv()

client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_response(user_message:str)->str:
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_message,
    )

    return response.text