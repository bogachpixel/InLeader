import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { useTelegram } from "@/hooks/useTelegram";

const API = "/api/inleader/onboarding";

interface NewbieNavigatorViewProps {
  onBack: () => void;
  onSuccess?: () => void;
}

export default function NewbieNavigatorView({ onBack, onSuccess }: NewbieNavigatorViewProps) {
  const { userId } = useTelegram();
  const [step, setStep] = useState(0);
  const [texts, setTexts] = useState<Record<string, string>>({});
  const [a1, setA1] = useState("");
  const [a2, setA2] = useState("");
  const [a3, setA3] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!userId) return;
    fetch(`/api/inleader/onboarding/texts?user_id=${userId}`)
      .then((r) => r.json())
      .then(setTexts)
      .catch(() => setTexts({}));
  }, [userId]);

  const questions = [texts.nav_q1, texts.nav_q2, texts.nav_q3].filter(Boolean);
  const defaults = [
    "1️⃣ Какая твоя главная цель на ближайшие 30 дней?",
    "2️⃣ Какой у тебя опыт в MLM или прямых продажах?",
    "3️⃣ Сколько времени в неделю готов уделять развитию?",
  ];

  const q = questions[step] || defaults[step];
  const answers = [a1, a2, a3];

  const handleSubmit = async () => {
    if (!userId || loading) return;
    setLoading(true);
    setError(null);
    try {
      const r = await fetch(`${API}/navigator`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, a1, a2, a3 }),
      });
      const d = await r.json().catch(() => ({}));
      if (r.status === 402) {
        setError(d.detail || "Недостаточно InCoins.");
        return;
      }
      if (d.ok && d.text) {
        setResult(d.text);
        onSuccess?.();
      } else {
        setError("Ошибка генерации плана.");
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Ошибка");
    } finally {
      setLoading(false);
    }
  };

  if (result) {
    return (
      <div className="glass-card glow-border p-4 flex flex-col gap-4 animate-fade-in">
        <div className="prose prose-sm max-w-none text-[#333]">
          <ReactMarkdown>{result}</ReactMarkdown>
        </div>
        <button onClick={onBack} className="w-full neu-button py-3 text-[var(--gold-primary)] font-semibold">
          ← Назад
        </button>
      </div>
    );
  }

  return (
    <div className="glass-card glow-border p-4 flex flex-col gap-4 animate-fade-in">
      <p className="text-sm text-[#333]">{q}</p>
      {step < 3 ? (
        <>
          <textarea
            value={answers[step]}
            onChange={(e) => {
              if (step === 0) setA1(e.target.value);
              else if (step === 1) setA2(e.target.value);
              else setA3(e.target.value);
            }}
            placeholder="Введи ответ..."
            disabled={loading}
            className="neu-button px-4 py-3 text-sm min-h-[80px] resize-none outline-none placeholder:text-[#999]"
          />
          <div className="flex gap-2">
            {step > 0 && (
              <button onClick={() => setStep(step - 1)} className="flex-1 neu-button py-2.5 text-sm">
                Назад
              </button>
            )}
            <button
              onClick={() => (step < 2 ? setStep(step + 1) : handleSubmit())}
              disabled={loading || !answers[step]?.trim()}
              className="flex-1 neu-button py-2.5 text-sm text-[var(--gold-primary)] font-semibold disabled:opacity-50"
            >
              {loading ? "..." : step < 2 ? "Далее" : "Получить план"}
            </button>
          </div>
        </>
      ) : null}
      {error && <p className="text-sm text-red-600">{error}</p>}
    </div>
  );
}
