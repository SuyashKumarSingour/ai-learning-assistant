"use client";

import {
  FormEvent,
  useEffect,
  useState,
} from "react";

import {
  getConversationMessages,
  getConversations,
  sendChatMessage,
  type ChatMessage,
} from "@/lib/api";

type Message = {
  role: "user" | "assistant";
  content: string;
};

type ChatProps = {
  selectedConversationId: string | null;
  onConversationChange?: (conversationId?: string) => void;
};

export default function Chat({
  selectedConversationId,
  onConversationChange,
}: ChatProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [conversationId, setConversationId] = useState<string | null>(
    selectedConversationId,
  );
  const [loading, setLoading] = useState(false);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [error, setError] = useState("");

  async function loadConversation(
    selectedId: string,
  ) {
    try {
      setError("");
      setLoadingHistory(true);

      const history = await getConversationMessages(
        selectedId,
      );

      const restoredMessages: Message[] = history.map(
        (message: ChatMessage) => ({
          role: message.role,
          content: message.content,
        }),
      );

      setConversationId(selectedId);
      setMessages(restoredMessages);
    } catch (err) {
      console.error(
        "Failed to load conversation:",
        err,
      );

      setError(
        err instanceof Error
          ? err.message
          : "Failed to load conversation.",
      );
    } finally {
      setLoadingHistory(false);
    }
  }

  useEffect(() => {
    if (!selectedConversationId) {
      setConversationId(null);
      setMessages([]);
      setError("");
      setLoadingHistory(false);
      return;
    }

    loadConversation(selectedConversationId);
  }, [selectedConversationId]);

  useEffect(() => {
    async function loadLatestConversation() {
      if (selectedConversationId) {
        setLoadingHistory(false);
        return;
      }

      try {
        setError("");

        const conversations = await getConversations();

        if (conversations.length === 0) {
          setConversationId(null);
          setMessages([]);
          return;
        }

        const latestConversation = conversations[0];

        await loadConversation(latestConversation.id);

        onConversationChange?.(
          latestConversation.id,
        );
      } catch (err) {
        console.error(
          "Failed to load conversations:",
          err,
        );

        setError(
          err instanceof Error
            ? err.message
            : "Failed to load conversation history.",
        );
      } finally {
        setLoadingHistory(false);
      }
    }

    loadLatestConversation();
  }, []);

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    const trimmedInput = input.trim();

    if (!trimmedInput || loading) {
      return;
    }

    setError("");
    setLoading(true);

    const userMessage: Message = {
      role: "user",
      content: trimmedInput,
    };

    setMessages((current) => [
      ...current,
      userMessage,
    ]);

    setInput("");

    try {
      const result = await sendChatMessage(
        trimmedInput,
        undefined,
        conversationId ?? undefined,
      );

      if (!conversationId) {
        setConversationId(result.conversation_id);
      }

      const assistantMessage: Message = {
        role: "assistant",
        content: result.response,
      };

      setMessages((current) => [
        ...current,
        assistantMessage,
      ]);

      onConversationChange?.(
        result.conversation_id,
      );
    } catch (err) {
      console.error("Chat request failed:", err);

      setError(
        err instanceof Error
          ? err.message
          : "Failed to get an answer.",
      );

      setMessages((current) => current.slice(0, -1));
    } finally {
      setLoading(false);
    }
  }

  if (loadingHistory) {
    return (
      <section className="w-full rounded-lg border p-6">
        <h2 className="mb-4 text-lg font-semibold">
          AI Learning Assistant
        </h2>

        <p className="text-sm text-gray-500">
          Loading conversation history...
        </p>
      </section>
    );
  }

  return (
    <section className="w-full rounded-lg border p-6">
      <h2 className="mb-4 text-lg font-semibold">
        AI Learning Assistant
      </h2>

      <div className="mb-4 min-h-32 space-y-4">
        {messages.length === 0 ? (
          <p className="text-sm text-gray-500">
            Ask a question to get started.
          </p>
        ) : (
          messages.map((message, index) => (
            <div
              key={`${message.role}-${index}`}
              className="rounded-md bg-gray-50 p-4"
            >
              <p className="mb-1 text-sm font-semibold">
                {message.role === "user"
                  ? "You"
                  : "AI"}
              </p>

              <p className="whitespace-pre-wrap text-sm text-gray-700">
                {message.content}
              </p>
            </div>
          ))
        )}

        {loading && (
          <div className="rounded-md bg-gray-50 p-4">
            <p className="text-sm text-gray-500">
              Thinking...
            </p>
          </div>
        )}
      </div>

      {error && (
        <p className="mb-4 rounded-md bg-red-50 p-3 text-sm text-red-600">
          {error}
        </p>
      )}

      <form
        onSubmit={handleSubmit}
        className="flex gap-2"
      >
        <input
          type="text"
          value={input}
          onChange={(event) =>
            setInput(event.target.value)
          }
          disabled={loading}
          placeholder="Ask a question..."
          className="flex-1 rounded-md border px-3 py-2 outline-none focus:ring-2"
        />

        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="rounded-md bg-black px-4 py-2 font-medium text-white disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? "Sending..." : "Send"}
        </button>
      </form>
    </section>
  );
}