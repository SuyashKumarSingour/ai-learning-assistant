"use client";

import { useEffect, useState, type ReactNode } from "react";
import { useRouter } from "next/navigation";

import { supabase } from "@/lib/supabase";

type AuthGuardProps = {
  children: ReactNode;
};

export default function AuthGuard({ children }: AuthGuardProps) {
  const router = useRouter();
  const [checkingAuth, setCheckingAuth] = useState(true);

  useEffect(() => {
    let mounted = true;

    async function checkAuth() {
      const { data, error } = await supabase.auth.getSession();

      if (error) {
        console.error("Authentication check failed:", error);

        if (mounted) {
          setCheckingAuth(false);
        }

        router.replace("/login");
        return;
      }

      if (!data.session) {
        if (mounted) {
          setCheckingAuth(false);
        }

        router.replace("/login");
        return;
      }

      if (mounted) {
        setCheckingAuth(false);
      }
    }

    checkAuth();

    return () => {
      mounted = false;
    };
  }, [router]);

  if (checkingAuth) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <p>Checking authentication...</p>
      </main>
    );
  }

  return <>{children}</>;
}