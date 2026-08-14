import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = "gemini-2.5-flash"
    EMBEDDING_MODEL = "gemini-embedding-001"

    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))

    SUPABASE_URL = os.getenv("SUPABASE_URL")


settings = Settings()