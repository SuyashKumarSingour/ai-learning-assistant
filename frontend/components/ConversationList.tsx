"use client";

import { useEffect, useState } from "react";

import {
  getConversations,
  type Conversation,
} from "@/lib/api";

type ConversationListProps = {
  activeConversationId: string | null;
  onSelect: (conversationId: string) => void;
  onNewConversation: () => void;
  refreshKey?: number;
};

export default function ConversationList({
  activeConversationId,
  onSelect,
  onNewConversation,
  refreshKey = 0,
}: ConversationListProps) {
  const [conversations, setConversations] = useState<
    Conversation[]
  >([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadConversations() {
      try {
        setLoading(true);
        setError("");

        const data = await getConversations();

        setConversations(data);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load conversations.",
        );
      } finally {
        setLoading(false);
      }
    }

    loadConversations();
  }, [refreshKey]);

  return (
    <aside className="w-full rounded-lg border bg-white p-4 lg:w-72">
      <div className="mb-4 flex items-center justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold">
            Conversations
          </h2>

          <p className="mt-1 text-xs text-gray-500">
            Your saved chats
          </p>
        </div>

        <button
          type="button"
          onClick={onNewConversation}
          className="rounded-md bg-black px-3 py-2 text-xs font-medium text-white hover:bg-gray-800"
        >
          New Chat
        </button>
      </div>

      {loading && (
        <p className="text-sm text-gray-500">
          Loading conversations...
        </p>
      )}

      {error && (
        <p className="rounded-md bg-red-50 p-3 text-sm text-red-600">
          {error}
        </p>
      )}

      {!loading &&
        !error &&
        conversations.length === 0 && (
          <p className="text-sm text-gray-500">
            No conversations yet.
          </p>
        )}

      {!loading && !error && conversations.length > 0 && (
        <div className="space-y-2">
          {conversations.map((conversation) => (
            <button
              key={conversation.id}
              type="button"
              onClick={() => onSelect(conversation.id)}
              className={`w-full rounded-md border px-3 py-2 text-left text-sm transition ${
                activeConversationId === conversation.id
                  ? "bg-gray-100 font-medium"
                  : "hover:bg-gray-50"
              }`}
            >
              <p className="truncate">
                {conversation.title}
              </p>

              <p className="mt-1 text-xs text-gray-400">
                {new Date(
                  conversation.updated_at,
                ).toLocaleString()}
              </p>
            </button>
          ))}
        </div>
      )}
    </aside>
  );
}