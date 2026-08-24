"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Play } from "lucide-react";

import { Spinner } from "@/components/ui";

/**
 * Botão "Experimentar demonstração". Chama o endpoint de demo do BFF (que
 * define o cookie de sessão httpOnly) e leva o visitante ao workspace demo,
 * sem exigir credenciais nem expor contas administrativas.
 */
export function DemoButton({ className = "button primary", label = "Experimentar demonstração" }: { className?: string; label?: string }) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function entrarDemo() {
    setLoading(true);
    setError("");
    try {
      const response = await fetch("/api/auth/demo", { method: "POST" });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.detail ?? "Não foi possível abrir a demonstração.");
      router.replace("/dashboard");
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Não foi possível abrir a demonstração.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ display: "grid", gap: "8px" }}>
      <button className={className} onClick={entrarDemo} disabled={loading}>
        {loading ? <Spinner /> : <Play size={17} />}
        {label}
      </button>
      {error && <p className="form-error" role="alert">{error}</p>}
    </div>
  );
}
