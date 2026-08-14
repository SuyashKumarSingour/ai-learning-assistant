import requests

from app.config import settings


def get_supabase_headers() -> dict[str, str]:
    return {
        "apikey": settings.SUPABASE_SECRET_KEY,
        "Authorization": f"Bearer {settings.SUPABASE_SECRET_KEY}",
        "Content-Type": "application/json",
    }


def get_supabase_url() -> str:
    return f"{settings.SUPABASE_URL}/rest/v1"