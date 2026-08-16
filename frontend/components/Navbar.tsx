"use client";

import { useRouter } from "next/navigation";

import { signOut } from "@/lib/auth";

export default function Navbar() {
  const router = useRouter();

  async function handleLogout() {
    try {
      await signOut();
      router.replace("/login");
    } catch (error) {
      console.error("Logout failed:", error);
    }
  }

  return (
    <nav className="flex w-full items-center justify-between border-b px-6 py-4">
      <h1 className="text-xl font-semibold">
        AI Learning Assistant
      </h1>

      <button
        onClick={handleLogout}
        className="rounded-md border px-4 py-2 text-sm font-medium hover:bg-gray-100"
      >
        Logout
      </button>
    </nav>
  );
}