from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.rag_service import answer_question


router = APIRouter()


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=2000,
        description="Message of the user",
    )
    document_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    status: str


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    ai_response = answer_question(
        question=request.message,
        document_id=request.document_id,
    )

    return ChatResponse(
        response=ai_response,
        status="Success",
    )