"use client";

import { useState } from "react";

import { uploadDocument } from "@/lib/api";

type UploadDocumentProps = {
  onUploaded: () => void;
};

export default function UploadDocument({
  onUploaded,
}: UploadDocumentProps) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  function handleFileChange(
    event: React.ChangeEvent<HTMLInputElement>,
  ) {
    const selectedFile = event.target.files?.[0] ?? null;

    setFile(selectedFile);
    setError("");
    setSuccess("");
  }

  async function handleUpload() {
    if (!file) {
      return;
    }

    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const result = await uploadDocument(file);

      setSuccess(
        `Uploaded successfully. ${result.chunks_inserted} chunks created.`,
      );

      setFile(null);

      onUploaded();
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to upload document.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="w-full max-w-md rounded-lg border p-6">
      <h2 className="mb-4 text-lg font-semibold">
        Upload a Document
      </h2>

      <input
        type="file"
        accept=".pdf,application/pdf"
        onChange={handleFileChange}
        disabled={loading}
        className="w-full rounded-md border p-2 text-sm"
      />

      {file && (
        <p className="mt-3 text-sm text-gray-600">
          Selected: {file.name}
        </p>
      )}

      {error && (
        <p className="mt-3 rounded-md bg-red-50 p-3 text-sm text-red-600">
          {error}
        </p>
      )}

      {success && (
        <p className="mt-3 rounded-md bg-green-50 p-3 text-sm text-green-700">
          {success}
        </p>
      )}

      <button
        type="button"
        onClick={handleUpload}
        disabled={!file || loading}
        className="mt-4 w-full rounded-md bg-black px-4 py-2 font-medium text-white disabled:cursor-not-allowed disabled:opacity-50"
      >
        {loading ? "Uploading..." : "Upload PDF"}
      </button>
    </section>
  );
}