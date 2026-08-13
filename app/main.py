from fastapi import FastAPI

from app.routers.chat import router as chat_router
from app.routers.health import router as health_router
from app.routers.documents import router as documents_router


app = FastAPI()


app.include_router(chat_router)
app.include_router(health_router)
app.include_router(documents_router)