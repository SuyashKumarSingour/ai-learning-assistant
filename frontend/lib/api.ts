import { supabase } from "./supabase";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export type Document = {
  id: string;
  filename: string;
  file_size: number;
  chunks_count: number;
  created_at: string;
};

type DocumentsResponse = {
  documents: Document[];
};

export async function getDocuments(): Promise<Document[]> {
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session) {
    throw new Error("You must be logged in.");
  }

  const response = await fetch(`${API_URL}/documents`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${session.access_token}`,
    },
  });

  if (!response.ok) {
    let message = "Failed to fetch documents.";

    try {
      const data = await response.json();

      if (data.detail) {
        message = data.detail;
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(message);
  }

  const data: DocumentsResponse = await response.json();

  return data.documents;
}

export async function uploadDocument(file: File): Promise<{
  message: string;
  document_id: string;
  chunks_inserted: number;
}> {
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session) {
    throw new Error("You must be logged in.");
  }

  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(`${API_URL}/documents/upload`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${session.access_token}`,
    },
    body: formData,
  });

  if (!response.ok) {
    let message = "Failed to upload document.";

    try {
      const data = await response.json();

      if (data.detail) {
        message = data.detail;
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(message);
  }

  return response.json();
}

export async function sendChatMessage(
  message: string,
  documentId?: string,
  conversationId?: string,
): Promise<{
  response: string;
  conversation_id: string;
}> {
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session) {
    throw new Error("You must be logged in.");
  }

  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${session.access_token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
      document_id: documentId ?? null,
      conversation_id: conversationId ?? null,
    }),
  });

  if (!response.ok) {
    let errorMessage = "Failed to get an answer.";

    try {
      const data = await response.json();

      if (data.detail) {
        errorMessage = data.detail;
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(errorMessage);
  }

  const data: {
    response: string;
    status: string;
    conversation_id: string;
  } = await response.json();

  return {
    response: data.response,
    conversation_id: data.conversation_id,
  };
}
export type ChatMessage = {
  id: string;
  conversation_id: string;
  role: "user" | "assistant";
  content: string;
  created_at: string;
};

export async function getConversationMessages(
  conversationId: string,
): Promise<ChatMessage[]> {
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session) {
    throw new Error("You must be logged in.");
  }

  const response = await fetch(
    `${API_URL}/conversations/${conversationId}/messages`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${session.access_token}`,
      },
    },
  );

  if (!response.ok) {
    let errorMessage = "Failed to load conversation history.";

    try {
      const data = await response.json();

      if (data.detail) {
        errorMessage = data.detail;
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(errorMessage);
  }

  const data: {
    messages: ChatMessage[];
  } = await response.json();

  return data.messages;
}


export type Conversation = {
  id: string;
  user_id: string;
  document_id: string | null;
  title: string;
  created_at: string;
  updated_at: string;
};

export async function getConversations(): Promise<Conversation[]> {
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session) {
    throw new Error("You must be logged in.");
  }

  const response = await fetch(`${API_URL}/conversations`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${session.access_token}`,
    },
  });

  if (!response.ok) {
    let errorMessage = "Failed to load conversations.";

    try {
      const data = await response.json();

      if (data.detail) {
        errorMessage = data.detail;
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(errorMessage);
  }

  const data: {
    conversations: Conversation[];
  } = await response.json();

  return data.conversations;
}



export async function deleteDocument(documentId: string): Promise<{
  message: string;
  document_id: string;
}> {
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session) {
    throw new Error("You must be logged in.");
  }

  const response = await fetch(
    `${API_URL}/documents/${documentId}`,
    {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${session.access_token}`,
      },
    },
  );

  if (!response.ok) {
    let message = "Failed to delete document.";

    try {
      const data = await response.json();

      if (data.detail) {
        message = data.detail;
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(message);
  }

  return response.json();
}