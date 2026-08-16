import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = "gemini-2.5-flash"
    EMBEDDING_MODEL = "gemini-embedding-001"

    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")


settings = Settings()