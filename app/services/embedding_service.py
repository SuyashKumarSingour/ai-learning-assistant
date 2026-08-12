from app.clients.google_client import client
from app.config import settings


def generate_embedding(text: str) -> list[float]:

    response = client.models.embed_content(
        model=settings.EMBEDDING_MODEL,
        contents=text
    )

    return response.embeddings[0].values