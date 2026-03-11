import { useState, useEffect } from "react";
import { useTelegram } from "@/hooks/useTelegram";

const API = "/api/inleader/crm";

interface Reminder {
  id: number;
  user_id: number;
  run_at: string;
  task_text: string;
}

interface CrmTexts {
  crm_title: string;
  crm_add_reminder: string;
  crm_list_reminders: string;
  crm_ask_task: string;
  crm_thinking: string;
  crm_confirmed: string;
  crm_parse_error: string;
  crm_past_date: string;
  crm_no_reminders: string;
  crm_list_header: string;
}

interface CrmViewProps {
  onBack: () => void;
  onReminderAdded?: () => void;
}

export default function CrmView({ onBack, onReminderAdded }: CrmViewProps) {
  const { userId } = useTelegram();
  const [texts, setTexts] = useState<CrmTexts | null>(null);
  const [mode, setMode] = useState<"menu" | "add" | "list">("menu");
  const [taskInput, setTaskInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ ok: boolean; message: string } | null>(null);
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [loadingList, setLoadingList] = useState(false);

  useEffect(() => {
    if (!userId) return;
    fetch(`${API}/texts?user_id=${userId}`)
      .then((r) => r.json())
      .then(setTexts)
      .catch(() => setTexts(null));
  }, [userId]);

  const fetchList = async () => {
    if (!userId) return;
    setLoadingList(true);
    try {
      const r = await fetch(`${API}/list?user_id=${userId}`);
      const d = await r.json();
      setReminders(d.reminders || []);
    } catch {
      setReminders([]);
    } finally {
      setLoadingList(false);
    }
  };

  const handleAddSubmit = async () => {
    if (!userId || !taskInput.trim() || loading) return;
    setLoading(true);
    setResult(null);
    try {
      const r = await fetch(`${API}/add`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, task_text: taskInput.trim() }),
      });
      const d = await r.json().catch(() => ({}));
      if (r.status === 402) {
        setResult({ ok: false, message: d.detail || "Недостаточно InCoins. Пополните баланс в боте." });
        return;
      }
      if (d.ok) {
        setResult({ ok: true, message: d.message });
        setTaskInput("");
        onReminderAdded?.();
      } else {
        setResult({ ok: false, message: d.message || d.detail || texts?.crm_parse_error || "Ошибка" });
      }
    } catch (e) {
      setResult({ ok: false, message: e instanceof Error ? e.message : "Ошибка" });
    } finally {
      setLoading(false);
    }
  };

  const formatRunAt = (runAt: string) => {
    try {
      const d = new Date(runAt);
      const pad = (n: number) => String(n).padStart(2, "0");
      return `${pad(d.getDate())}.${pad(d.getMonth() + 1)}.${d.getFullYear()} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
    } catch {
      return runAt;
    }
  };

  if (!texts) {
    return (
      <div className="glass-card glow-border p-4 flex flex-col items-center justify-center min-h-[200px]">
        <p className="text-[#666]">Загрузка...</p>
      </div>
    );
  }

  if (mode === "add") {
    return (
      <div className="glass-card glow-border p-4 flex flex-col gap-4 animate-fade-in">
        <p className="text-sm text-[#333] whitespace-pre-line">{texts.crm_ask_task}</p>
        <textarea
          value={taskInput}
          onChange={(e) => setTaskInput(e.target.value)}
          placeholder="Например: Завтра в 15:00 позвонить Ивану"
          disabled={loading}
          className="neu-button px-4 py-3 text-sm text-[#333] min-h-[80px] resize-none outline-none placeholder:text-[#999] disabled:opacity-50"
        />
        {result && (
          <p className={`text-sm ${result.ok ? "text-green-600" : "text-red-600"}`}>{result.message}</p>
        )}
        <div className="flex gap-2">
          <button
            onClick={() => {
              setMode("menu");
              setResult(null);
              setTaskInput("");
            }}
            className="flex-1 neu-button py-2.5 text-sm"
          >
            Отмена
          </button>
          <button
            onClick={handleAddSubmit}
            disabled={loading || !taskInput.trim()}
            className="flex-1 neu-button py-2.5 text-sm text-[var(--gold-primary)] font-semibold disabled:opacity-50"
          >
            {loading ? "..." : "Добавить"}
          </button>
        </div>
      </div>
    );
  }

  if (mode === "list") {
    return (
      <div className="glass-card glow-border p-4 flex flex-col gap-4 animate-fade-in">
        <p className="text-sm font-semibold text-[#333]">{texts.crm_list_header}</p>
        {loadingList ? (
          <p className="text-sm text-[#666]">Загрузка...</p>
        ) : reminders.length === 0 ? (
          <p className="text-sm text-[#666]">{texts.crm_no_reminders}</p>
        ) : (
          <ul className="space-y-2 text-sm text-[#333]">
            {reminders.map((r, i) => (
              <li key={r.id} className="glass rounded-xl px-3 py-2">
                {i + 1}. {formatRunAt(r.run_at)} — {r.task_text}
              </li>
            ))}
          </ul>
        )}
        <button
          onClick={() => setMode("menu")}
          className="w-full neu-button py-2.5 text-sm text-[var(--gold-primary)] font-semibold"
        >
          ← Назад
        </button>
      </div>
    );
  }

  // mode === "menu"
  return (
    <div className="glass-card glow-border p-5 animate-fade-in">
      <h2 className="text-base font-bold text-[#333] mb-1">
        {texts.crm_title.split("\n")[0]}
      </h2>
      <p className="text-sm text-[#666] mb-4">
        {texts.crm_title.split("\n\n")[1] || "Выбери действие:"}
      </p>
      <div className="flex flex-col gap-3">
        <button
          onClick={() => setMode("add")}
          className="w-full neu-button py-3 text-left px-4 flex items-center gap-3"
        >
          <span className="text-lg">➕</span>
          <span className="text-sm font-medium text-[#333]">{texts.crm_add_reminder}</span>
        </button>
        <button
          onClick={async () => {
            setMode("list");
            await fetchList();
          }}
          className="w-full neu-button py-3 text-left px-4 flex items-center gap-3"
        >
          <span className="text-lg">📋</span>
          <span className="text-sm font-medium text-[#333]">{texts.crm_list_reminders}</span>
        </button>
        <button
          onClick={onBack}
          className="w-full neu-button py-3 text-left px-4 flex items-center gap-3 text-[var(--gold-primary)] font-semibold"
        >
          <span className="text-lg">🏠</span>
          <span className="text-sm">В меню</span>
        </button>
      </div>
    </div>
  );
}
