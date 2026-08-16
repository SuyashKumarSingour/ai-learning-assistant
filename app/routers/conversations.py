from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.services.conversation_service import (
    list_conversations,
    list_messages,
)


router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
)


@router.get("")
def get_conversations(
    user_id: str = Depends(get_current_user),
):
    return {
        "conversations": list_conversations(user_id),
    }


@router.get("/{conversation_id}/messages")
def get_conversation_messages(
    conversation_id: str,
    user_id: str = Depends(get_current_user),
):
    messages = list_messages(
        conversation_id=conversation_id,
        user_id=user_id,
    )

    if not messages:
        # We need to distinguish between an empty conversation
        # and a conversation that does not belong to this user.
        from app.services.conversation_service import get_conversation

        conversation = get_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found.",
            )

    return {
        "messages": messages,
    }