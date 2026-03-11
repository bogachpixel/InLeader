import { useState, useEffect } from "react";
import { useTelegram } from "@/hooks/useTelegram";

type CalcType = "tourist" | "cruise" | "conversion" | "free";

interface CalcChatProps {
  calcType: CalcType;
  onBack: () => void;
}

const CalcChat = ({ calcType, onBack }: CalcChatProps) => {
  const { userId } = useTelegram();
  const [step, setStep] = useState<number>(0);
  const [input1, setInput1] = useState("");
  const [input2, setInput2] = useState("");
  const [result, setResult] = useState<{ text: string; image?: string; caption?: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [texts, setTexts] = useState<Record<string, string>>({});

  useEffect(() => {
    const fetchTexts = async () => {
      if (!userId) return;
      try {
        const r = await fetch(`/api/inleader/calculator/texts?user_id=${userId}`);
        if (r.ok) {
          const data = await r.json();
          setTexts(data);
        }
      } catch (e) {
        console.error(e);
      }
    };
    fetchTexts();
  }, [userId]);

  const API = "/api/inleader/calculator";

  const handleFree = async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await fetch(`${API}/free?user_id=${userId}`);
      if (!r.ok) throw new Error("Ошибка");
      const data = await r.json();
      setResult({ text: data.text });
    } catch (e) {
      setError(e instanceof Error ? e.message : "Ошибка");
    } finally {
      setLoading(false);
    }
  };

  const handleTourist = async () => {
    const raw = input1.trim();
    if (!raw || !/^\d+$/.test(raw) || parseInt(raw, 10) <= 0) {
      setError(texts.calc_bad_number || "⚠️ Введи целое положительное число.");
      return;
    }
    let months = parseInt(raw, 10);
    if (months > 120) months = 120;
    setLoading(true);
    setError(null);
    try {
      const r = await fetch(`${API}/tourist`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, months }),
      });
      if (!r.ok) throw new Error("Ошибка");
      const data = await r.json();
      setResult({ text: data.text, image: data.image, caption: data.caption });
    } catch (e) {
      setError(e instanceof Error ? e.message : "Ошибка");
    } finally {
      setLoading(false);
    }
  };

  const handleCruise = async () => {
    if (step === 0) {
      const raw = input1.replace(/,/g, ".").replace(/\s/g, "");
      const price = parseFloat(raw);
      if (isNaN(price) || price <= 0) {
        setError(texts.calc_bad_number || "⚠️ Введи положительное число.");
        return;
      }
      setInput2("");
      setStep(1);
      setError(null);
      return;
    }
    const raw = input2.replace(/\s/g, "");
    const rp = parseInt(raw, 10);
    if (isNaN(rp) || rp < 0) {
      setError(texts.calc_bad_number || "⚠️ Введи целое неотрицательное число.");
      return;
    }
    const price = parseFloat(input1.replace(/,/g, ".").replace(/\s/g, ""));
    setLoading(true);
    setError(null);
    try {
      const resp = await fetch(`${API}/cruise`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, price, rp }),
      });
      if (!resp.ok) throw new Error("Ошибка");
      const data = await resp.json();
      setResult({ text: data.text, image: data.image, caption: data.caption });
    } catch (e) {
      setError(e instanceof Error ? e.message : "Ошибка");
    } finally {
      setLoading(false);
    }
  };

  const handleConversion = async () => {
    if (!input1.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const r = await fetch(`${API}/conversion`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, text: input1.trim() }),
      });
      const data = await r.json().catch(() => ({}));
      if (!r.ok) {
        throw new Error(data.detail || "Ошибка");
      }
      setResult({ text: data.text, image: data.image, caption: data.caption });
    } catch (e) {
      setError(e instanceof Error ? e.message : "Ошибка");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (calcType === "free" && userId) {
      setLoading(true);
      fetch(`/api/inleader/calculator/free?user_id=${userId}`)
        .then((r) => r.json())
        .then((data) => setResult({ text: data.text }))
        .catch(() => setError("Ошибка"))
        .finally(() => setLoading(false));
    }
  }, [calcType, userId]);

  if (calcType === "free") {
    return (
      <div className="glass-card glow-border p-4 flex flex-col h-[80vh] max-h-[700px] animate-fade-in">
        <div className="glass-header rounded-2xl px-4 py-3 mb-3">
          <h2 className="text-sm font-display font-bold text-[#333]">🧮 Калькулятор</h2>
          <p className="text-xs text-[#666]">Безоплатное членство</p>
        </div>
        <div className="flex-1 overflow-y-auto">
          {loading && <p className="text-[#666]">Загрузка...</p>}
          {result && (
            <div className="glass rounded-2xl px-4 py-3 text-sm text-[#333] whitespace-pre-wrap">
              {result.text}
            </div>
          )}
        </div>
        <button onClick={onBack} className="neu-button py-3 mt-3 text-[var(--gold-primary)] font-bold text-sm">
          ← Назад
        </button>
      </div>
    );
  }

  if (result) {
    return (
      <div className="glass-card glow-border p-4 flex flex-col h-[80vh] max-h-[700px] animate-fade-in">
        <div className="flex-1 overflow-y-auto space-y-3 mb-3">
          <div className="glass rounded-2xl px-4 py-3 text-sm text-[#333] whitespace-pre-wrap">{result.text}</div>
          {result.image && (
            <div>
              <img
                src={`data:image/png;base64,${result.image}`}
                alt="Результат"
                className="rounded-2xl w-full max-h-80 object-contain"
              />
              {result.caption && <p className="text-xs text-[#666] mt-1">{result.caption}</p>}
            </div>
          )}
        </div>
        <button onClick={() => { setResult(null); setStep(0); setInput1(""); setInput2(""); }} className="neu-button py-2 mb-2 text-sm">
          Новый расчёт
        </button>
        <button onClick={onBack} className="neu-button py-3 text-[var(--gold-primary)] font-bold text-sm">
          ← Назад
        </button>
      </div>
    );
  }

  const isTourist = calcType === "tourist";
  const isCruise = calcType === "cruise";
  const isConversion = calcType === "conversion";

  const prompt =
    isTourist
      ? texts.calc_tourist_ask || "🏖 Сколько месяцев ты планируешь копить баллы?\n\nВзнос: $100/мес → 200 Reward Points/мес."
      : isCruise && step === 0
        ? texts.calc_cruise_ask_price || "🚢 Введи заявленную цену круиза на inCruises (в USD)."
        : isCruise
          ? texts.calc_cruise_ask_rp || "Отлично! Теперь введи количество твоих накопленных Бонусных Баллов (ББ)."
          : texts.calc_conversion_ask ||
            "Напиши стоимость круиза и сумму налогов/сборов (если знаешь).\n\nНапример: «3500» или «каюта 3500, сборы 350».";

  const submit = isTourist ? handleTourist : isCruise ? handleCruise : handleConversion;
  const canSubmit = isTourist || isConversion ? input1.trim().length > 0 : step === 0 ? input1.trim().length > 0 : input2.trim().length > 0;

  return (
    <div className="glass-card glow-border p-4 flex flex-col h-[80vh] max-h-[700px] animate-fade-in">
      <div className="glass-header rounded-2xl px-4 py-3 mb-3">
        <h2 className="text-sm font-display font-bold text-[#333]">🧮 Калькулятор</h2>
        <p className="text-xs text-[#666]">
          {isTourist && "Калькулятор Туриста"}
          {isCruise && "Расчёт круиза ББ"}
          {isConversion && "Конвертация ББ"}
        </p>
      </div>
      <div className="flex-1 overflow-y-auto mb-3">
        <p className="text-sm text-[#333] whitespace-pre-wrap mb-4">{prompt}</p>
        <input
          value={input1}
          onChange={(e) => setInput1(e.target.value)}
          placeholder={isCruise && step === 0 ? "Например: 5845" : isConversion ? "Например: каюта 3500, сборы 350" : "Введите число"}
          disabled={loading || (isCruise && step === 1)}
          className="w-full neu-button px-4 py-3 text-sm text-[#333] outline-none placeholder:text-[#999]"
        />
        {isCruise && step === 1 && (
          <input
            value={input2}
            onChange={(e) => setInput2(e.target.value)}
            placeholder="Например: 1200"
            disabled={loading}
            className="w-full neu-button px-4 py-3 text-sm text-[#333] outline-none placeholder:text-[#999] mt-3"
          />
        )}
        {error && <p className="text-red-600 text-sm mt-2">{error}</p>}
      </div>
      <div className="flex gap-2">
        <button
          onClick={submit}
          disabled={loading || !canSubmit}
          className="flex-1 neu-button py-3 text-[var(--gold-primary)] font-bold text-sm disabled:opacity-50"
        >
          {loading ? "..." : "Рассчитать"}
        </button>
        <button onClick={onBack} className="neu-button py-3 px-4 text-[var(--gold-primary)] font-bold text-sm">
          ← Назад
        </button>
      </div>
    </div>
  );
};

export default CalcChat;
