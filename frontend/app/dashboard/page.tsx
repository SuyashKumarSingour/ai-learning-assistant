"use client";

import { useState } from "react";

import AuthGuard from "@/components/AuthGuard";
import Navbar from "@/components/Navbar";
import DocumentList from "@/components/DocumentList";
import UploadDocument from "@/components/UploadDocument";
import Chat from "@/components/Chat";
import ConversationList from "@/components/ConversationList";

export default function DashboardPage() {
  const [refreshKey, setRefreshKey] = useState(0);
  const [activeConversationId, setActiveConversationId] =
    useState<string | null>(null);

  function handleUploaded() {
    setRefreshKey((current) => current + 1);
  }

  function handleConversationChange(
    conversationId?: string,
  ) {
    setRefreshKey((current) => current + 1);

    if (conversationId) {
      setActiveConversationId(conversationId);
    }
  }

  function handleNewConversation() {
    setActiveConversationId(null);
  }

  return (
    <AuthGuard>
      <main className="min-h-screen">
        <Navbar />

        <div className="mx-auto max-w-7xl p-8">
          <div className="grid gap-6 lg:grid-cols-[18rem_1fr]">
            <ConversationList
              refreshKey={refreshKey}
              activeConversationId={activeConversationId}
              onSelect={setActiveConversationId}
              onNewConversation={handleNewConversation}
            />

            <div className="flex min-w-0 flex-col gap-6">
              <Chat
                selectedConversationId={activeConversationId}
                onConversationChange={
                  handleConversationChange
                }
              />

              <UploadDocument
                onUploaded={handleUploaded}
              />

              <DocumentList key={refreshKey} />
            </div>
          </div>
        </div>
      </main>
    </AuthGuard>
  );
}