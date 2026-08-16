"use client";

import { useEffect, useState } from "react";

import {
  deleteDocument,
  getDocuments,
  type Document,
} from "@/lib/api";

export default function DocumentList() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [deletingId, setDeletingId] = useState<string | null>(null);

  useEffect(() => {
    async function loadDocuments() {
      try {
        setError("");

        const data = await getDocuments();

        setDocuments(data);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load documents.",
        );
      } finally {
        setLoading(false);
      }
    }

    loadDocuments();
  }, []);

  async function handleDelete(documentId: string) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this document? This will permanently remove its data from the system.",
    );

    if (!confirmed) {
      return;
    }

    try {
      setError("");
      setDeletingId(documentId);

      await deleteDocument(documentId);

      setDocuments((current) =>
        current.filter((document) => document.id !== documentId),
      );
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to delete document.",
      );
    } finally {
      setDeletingId(null);
    }
  }

  if (loading) {
    return (
      <section className="w-full max-w-md rounded-lg border p-6">
        <h2 className="mb-4 text-lg font-semibold">
          Your Documents
        </h2>

        <p className="text-sm text-gray-500">
          Loading documents...
        </p>
      </section>
    );
  }

  if (error && documents.length === 0) {
    return (
      <section className="w-full max-w-md rounded-lg border p-6">
        <h2 className="mb-4 text-lg font-semibold">
          Your Documents
        </h2>

        <p className="text-sm text-red-600">
          {error}
        </p>
      </section>
    );
  }

  return (
    <section className="w-full max-w-md rounded-lg border p-6">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold">
          Your Documents
        </h2>

        <span className="text-sm text-gray-500">
          {documents.length}
        </span>
      </div>

      {error && (
        <div className="mb-4 rounded-md border border-red-200 bg-red-50 p-3">
          <p className="text-sm text-red-600">
            {error}
          </p>
        </div>
      )}

      {documents.length === 0 ? (
        <p className="text-sm text-gray-500">
          You have no uploaded documents yet.
        </p>
      ) : (
        <div className="space-y-3">
          {documents.map((document) => {
            const isDeleting = deletingId === document.id;

            return (
              <div
                key={document.id}
                className="flex items-center justify-between gap-4 rounded-lg border p-4"
              >
                <div className="min-w-0">
                  <p className="truncate text-sm font-medium">
                    {document.filename}
                  </p>

                  <p className="mt-1 text-xs text-gray-500">
                    {document.chunks_count} chunks
                  </p>
                </div>

                <button
                  type="button"
                  onClick={() => handleDelete(document.id)}
                  disabled={isDeleting}
                  className="shrink-0 rounded-md border border-red-300 px-3 py-2 text-sm font-medium text-red-600 transition hover:bg-red-50 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {isDeleting ? "Deleting..." : "Delete"}
                </button>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}