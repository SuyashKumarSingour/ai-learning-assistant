"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { signIn, signUp } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();

  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  function switchMode() {
    setIsSignUp((current) => !current);
    setError("");
    setSuccess("");
    setEmail("");
    setPassword("");
  }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      if (isSignUp) {
        const data = await signUp(email, password);

        if (data.session) {
          router.push("/dashboard");
        } else {
          setSuccess(
            "Account created successfully. Please check your email to confirm your account, then sign in.",
          );
        }
      } else {
        await signIn(email, password);
        router.push("/dashboard");
      }
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : isSignUp
            ? "Unable to create your account."
            : "Unable to sign in.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-50 p-6">
      <div className="w-full max-w-md rounded-xl border bg-white p-8 shadow-sm">
        <h1 className="text-2xl font-bold">
          AI Learning Assistant
        </h1>

        <p className="mt-2 text-sm text-gray-500">
          {isSignUp
            ? "Create an account to get started."
            : "Sign in to continue."}
        </p>

        <form
          onSubmit={handleSubmit}
          className="mt-6 space-y-4"
        >
          <div>
            <label
              htmlFor="email"
              className="mb-1 block text-sm font-medium"
            >
              Email
            </label>

            <input
              id="email"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
              autoComplete="email"
              className="w-full rounded-md border px-3 py-2 outline-none focus:ring-2"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label
              htmlFor="password"
              className="mb-1 block text-sm font-medium"
            >
              Password
            </label>

            <input
              id="password"
              type="password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              required
              minLength={6}
              autoComplete={
                isSignUp ? "new-password" : "current-password"
              }
              className="w-full rounded-md border px-3 py-2 outline-none focus:ring-2"
              placeholder="Your password"
            />
          </div>

          {error && (
            <p className="rounded-md bg-red-50 p-3 text-sm text-red-600">
              {error}
            </p>
          )}

          {success && (
            <p className="rounded-md bg-green-50 p-3 text-sm text-green-700">
              {success}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-md bg-black px-4 py-2 font-medium text-white disabled:opacity-50"
          >
            {loading
              ? isSignUp
                ? "Creating account..."
                : "Signing in..."
              : isSignUp
                ? "Create account"
                : "Sign in"}
          </button>
        </form>

        <div className="mt-6 text-center text-sm text-gray-600">
          {isSignUp
            ? "Already have an account?"
            : "Don't have an account?"}

          <button
            type="button"
            onClick={switchMode}
            className="ml-1 font-medium text-black underline"
          >
            {isSignUp ? "Sign in" : "Sign up"}
          </button>
        </div>
      </div>
    </main>
  );
}