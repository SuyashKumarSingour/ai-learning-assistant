import requests

from app.clients.supabase_client import (
    get_supabase_headers,
    get_supabase_url,
)


def create_document(
    document_id: str,
    user_id: str,
    filename: str,
    file_path: str,
    file_size: int,
    chunks_count: int,
) -> dict:

    url = f"{get_supabase_url()}/documents"

    payload = {
        "id": document_id,
        "user_id": user_id,
        "filename": filename,
        "file_path": file_path,
        "file_size": file_size,
        "chunks_count": chunks_count,
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


def list_documents(user_id: str) -> list[dict]:

    url = f"{get_supabase_url()}/documents"

    params = {
        "user_id": f"eq.{user_id}",
        "select": "id,filename,file_size,chunks_count,created_at",
        "order": "created_at.desc",
    }

    response = requests.get(
        url,
        headers=get_supabase_headers(),
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def get_document(
    document_id: str,
    user_id: str,
) -> dict | None:

    url = f"{get_supabase_url()}/documents"

    params = {
        "id": f"eq.{document_id}",
        "user_id": f"eq.{user_id}",
        "select": "id,filename,file_path,file_size,chunks_count,created_at",
    }

    response = requests.get(
        url,
        headers=get_supabase_headers(),
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    documents = response.json()

    if not documents:
        return None

    return documents[0]


def delete_document(
    document_id: str,
    user_id: str,
) -> bool:

    url = f"{get_supabase_url()}/documents"

    params = {
        "id": f"eq.{document_id}",
        "user_id": f"eq.{user_id}",
    }

    response = requests.delete(
        url,
        headers={
            **get_supabase_headers(),
            "Prefer": "return=representation",
        },
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    deleted_documents = response.json()

    return len(deleted_documents) > 0