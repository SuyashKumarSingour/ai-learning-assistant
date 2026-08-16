import requests

from app.clients.supabase_client import (
    get_supabase_headers,
    get_supabase_url,
)


def create_conversation(
    user_id: str,
    document_id: str | None = None,
    title: str = "New Conversation",
) -> dict:
    url = f"{get_supabase_url()}/conversations"

    payload = {
        "user_id": user_id,
        "document_id": document_id,
        "title": title,
    }

    response = requests.post(
        url,
        headers={
            **get_supabase_headers(),
            "Prefer": "return=representation",
        },
        json=payload,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()[0]


def get_conversation(
    conversation_id: str,
    user_id: str,
) -> dict | None:
    url = f"{get_supabase_url()}/conversations"

    params = {
        "id": f"eq.{conversation_id}",
        "user_id": f"eq.{user_id}",
        "select": "id,user_id,document_id,title,created_at,updated_at",
    }

    response = requests.get(
        url,
        headers=get_supabase_headers(),
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    conversations = response.json()

    if not conversations:
        return None

    return conversations[0]


def list_conversations(
    user_id: str,
) -> list[dict]:
    url = f"{get_supabase_url()}/conversations"

    params = {
        "user_id": f"eq.{user_id}",
        "select": "id,user_id,document_id,title,created_at,updated_at",
        "order": "updated_at.desc",
    }

    response = requests.get(
        url,
        headers=get_supabase_headers(),
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def update_conversation_timestamp(
    conversation_id: str,
    user_id: str,
) -> dict | None:
    url = f"{get_supabase_url()}/conversations"

    params = {
        "id": f"eq.{conversation_id}",
        "user_id": f"eq.{user_id}",
    }

    payload = {
        "updated_at": "now()",
    }

    response = requests.patch(
        url,
        headers={
            **get_supabase_headers(),
            "Prefer": "return=representation",
        },
        params=params,
        json=payload,
        timeout=10,
    )

    response.raise_for_status()

    conversations = response.json()

    if not conversations:
        return None

    return conversations[0]


def add_message(
    conversation_id: str,
    role: str,
    content: str,
) -> dict:
    if role not in {"user", "assistant"}:
        raise ValueError("Invalid message role.")

    url = f"{get_supabase_url()}/messages"

    payload = {
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
    }

    response = requests.post(
        url,
        headers={
            **get_supabase_headers(),
            "Prefer": "return=representation",
        },
        json=payload,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()[0]


def list_messages(
    conversation_id: str,
    user_id: str,
) -> list[dict]:
    conversation = get_conversation(
        conversation_id=conversation_id,
        user_id=user_id,
    )

    if conversation is None:
        return []

    url = f"{get_supabase_url()}/messages"

    params = {
        "conversation_id": f"eq.{conversation_id}",
        "select": "id,conversation_id,role,content,created_at",
        "order": "created_at.asc",
    }

    response = requests.get(
        url,
        headers=get_supabase_headers(),
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()