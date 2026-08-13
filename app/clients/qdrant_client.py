from qdrant_client import QdrantClient

from app.config import settings


client = QdrantClient(
    host=settings.QDRANT_HOST,
    port=settings.QDRANT_PORT,
)