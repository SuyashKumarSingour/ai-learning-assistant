from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.auth.dependencies import get_current_user
from app.services.conversation_service import (
    add_message,
    create_conversation,
    get_conversation,
    update_conversation_timestamp,
)
from app.services.rag_service import answer_question


router = APIRouter()


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=2000,
        description="Message of the user",
    )
    document_id: str | None = None
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    status: str
    conversation_id: str


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    user_id: str = Depends(get_current_user),
):
    conversation_id = request.conversation_id

    # Create a new conversation when this is the first message.
    if conversation_id is None:
        conversation = create_conversation(
            user_id=user_id,
            document_id=request.document_id,
            title=request.message[:80],
        )

        conversation_id = conversation["id"]

    else:
        # Make sure this conversation belongs to the
        # authenticated user.
        conversation = get_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        if conversation is None:
            raise ValueError("Conversation not found.")

    # Save the user's message.
    add_message(
        conversation_id=conversation_id,
        role="user",
        content=request.message,
    )

    # Run the existing RAG pipeline.
    ai_response = answer_question(
        question=request.message,
        user_id=user_id,
        document_id=request.document_id,
    )

    # Save the AI response.
    add_message(
        conversation_id=conversation_id,
        role="assistant",
        content=ai_response,
    )

    update_conversation_timestamp(
        conversation_id=conversation_id,
        user_id=user_id,
    )

    return ChatResponse(
        response=ai_response,
        status="Success",
        conversation_id=conversation_id,
    )