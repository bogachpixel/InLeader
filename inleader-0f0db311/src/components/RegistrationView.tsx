import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { useTelegram } from "@/hooks/useTelegram";

const API = "/api/inleader/registration";

interface RegistrationViewProps {
  onBack: () => void;
  onSuccess?: () => void;
}

export default function RegistrationView({ onBack, onSuccess }: RegistrationViewProps) {
  const { userId } = useTelegram();
  const [loading, setLoading] = useState(true);
  const [text, setText] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!userId) return;
    setLoading(true);
    setError(null);
    fetch(`${API}/instruction`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId }),
    })
      .then(async (r) => {
        const d = await r.json().catch(() => ({}));
        if (r.status === 402) {
          setError(d.detail || "Недостаточно InCoins.");
          return;
        }
        if (d.ok && d.text) {
          setText(d.text);
          onSuccess?.();
        } else {
          setError("Ошибка загрузки инструкции.");
        }
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Ошибка"))
      .finally(() => setLoading(false));
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userId]);

  if (loading) {
    return (
      <div className="glass-card glow-border p-4 flex flex-col items-center justify-center min-h-[200px] animate-fade-in">
        <p className="text-sm text-[#666]">⏳ Готовлю пошаговую инструкцию по регистрации, секунду...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass-card glow-border p-4 flex flex-col gap-4 animate-fade-in">
        <p className="text-sm text-red-600">{error}</p>
        <button onClick={onBack} className="w-full neu-button py-3 text-[var(--gold-primary)] font-semibold">
          ← Назад
        </button>
      </div>
    );
  }

  return (
    <div className="glass-card glow-border p-4 flex flex-col gap-4 animate-fade-in">
      <div className="prose prose-sm max-w-none text-[#333] prose-headings:text-[#333] prose-p:text-[#333] prose-li:text-[#333] prose-strong:text-[var(--gold-primary)]">
        <ReactMarkdown>{text || ""}</ReactMarkdown>
      </div>
      <button onClick={onBack} className="w-full neu-button py-3 text-[var(--gold-primary)] font-semibold">
        ← Назад
      </button>
    </div>
  );
}
