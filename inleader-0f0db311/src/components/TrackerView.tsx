import { useState, useEffect } from "react";
import { useTelegram } from "@/hooks/useTelegram";

interface TrackerViewProps {
  onBack: () => void;
}

const TASK_IDS = [1, 2, 3, 4];
const API = "/api/inleader/tracker";

export default function TrackerView({ onBack }: TrackerViewProps) {
  const { userId } = useTelegram();
  const [data, setData] = useState<{
    streak: number;
    last_tracker_date: string | null;
    daily_progress: string;
    today: string;
  } | null>(null);
  const [texts, setTexts] = useState<Record<string, string>>({});
  const [timezone, setTimezone] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [reportMode, setReportMode] = useState<{ taskId: number; label: string } | null>(null);
  const [reportInput, setReportInput] = useState("");
  const [reportLoading, setReportLoading] = useState(false);
  const [reportError, setReportError] = useState<string | null>(null);

  const fetchData = async () => {
    if (!userId) return;
    try {
      const [dataResp, textsResp, tzResp] = await Promise.all([
        fetch(`${API}/data?user_id=${userId}`),
        fetch(`${API}/texts?user_id=${userId}`),
        fetch(`${API}/timezone?user_id=${userId}`),
      ]);
      if (dataResp.ok) setData(await dataResp.json());
      if (textsResp.ok) setTexts(await textsResp.json());
      if (tzResp.ok) {
        const tz = await tzResp.json();
        setTimezone(tz.timezone);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [userId]);

  const progress = (data?.daily_progress || "0,0,0,0").split(",");
  const doneToday = data?.last_tracker_date === data?.today;

  if (loading || !data) {
    return (
      <div className="glass-card glow-border p-4 flex flex-col items-center justify-center min-h-[300px]">
        <p className="text-[#666]">Загрузка...</p>
      </div>
    );
  }

  if (timezone === null || timezone === undefined) {
    const offsets = [2, 3, 4, 5, 6, 7, 8];
    const tzLabels: Record<number, string> = {
      2: "UTC+2 Европа",
      3: "UTC+3 Москва",
      4: "UTC+4",
      5: "UTC+5",
      6: "UTC+6",
      7: "UTC+7",
      8: "UTC+8",
    };
    return (
      <div className="glass-card glow-border p-4 animate-fade-in">
        <p className="text-sm text-[#333] mb-4">{texts.trk_choose_tz || "🌍 Выбери часовой пояс:"}</p>
        <div className="flex flex-col gap-2">
          {offsets.map((off) => (
            <button
              key={off}
              onClick={async () => {
                await fetch(`${API}/timezone`, {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({ user_id: userId, offset: off }),
                });
                setTimezone(off);
              }}
              className="neu-button py-3 text-left px-4 text-sm"
            >
              {tzLabels[off] || `UTC+${off}`}
            </button>
          ))}
        </div>
      </div>
    );
  }

  if (doneToday) {
    return (
      <div className="glass-card glow-border p-4 animate-fade-in">
        <p className="text-sm text-[#333] whitespace-pre-wrap mb-4">
          {(texts.trk_done_today || "✅ План на сегодня выполнен!\n🔥 Твой стрик: __STREAK__ дней.").replace("__STREAK__", String(data.streak))}
        </p>
        <button onClick={onBack} className="w-full neu-button py-3 text-[var(--gold-primary)] font-bold text-sm">
          В меню
        </button>
      </div>
    );
  }

  if (reportMode) {
    const label = texts[`trk_${["contacts", "followup", "content", "study"][reportMode.taskId - 1]}`] || "";
    return (
      <div className="glass-card glow-border p-4 animate-fade-in">
        <p className="text-sm text-[#333] mb-3">
          📝 Отчёт по заданию: <strong>{label}</strong>
        </p>
        <p className="text-xs text-[#666] mb-3">Напиши кратко, что именно сделано?</p>
        <textarea
          value={reportInput}
          onChange={(e) => setReportInput(e.target.value)}
          placeholder="Например: Позвонил 3 контактам, 2 заинтересовались..."
          className="w-full neu-button px-4 py-3 text-sm min-h-[100px] resize-none"
          disabled={reportLoading}
        />
        {reportError && <p className="text-red-600 text-xs mt-2">{reportError}</p>}
        <div className="flex gap-2 mt-3">
          <button
            onClick={async () => {
              if (reportInput.trim().length < 5) {
                setReportError(texts.trk_report_too_short || "Слишком короткий отчёт.");
                return;
              }
              setReportLoading(true);
              setReportError(null);
              try {
                const r = await fetch(`${API}/task_report`, {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({
                    user_id: userId,
                    task_id: reportMode.taskId,
                    report_text: reportInput.trim(),
                  }),
                });
                const body = await r.json().catch(() => ({}));
                if (!r.ok) throw new Error(body.detail || "Ошибка");
                setReportMode(null);
                setReportInput("");
                fetchData();
              } catch (e) {
                setReportError(e instanceof Error ? e.message : "Ошибка");
              } finally {
                setReportLoading(false);
              }
            }}
            disabled={reportLoading || reportInput.trim().length < 5}
            className="flex-1 neu-button py-2.5 text-[var(--gold-primary)] font-semibold text-sm disabled:opacity-50"
          >
            {reportLoading ? "..." : "Отправить"}
          </button>
          <button
            onClick={() => {
              setReportMode(null);
              setReportInput("");
              setReportError(null);
            }}
            className="neu-button py-2.5 px-4 text-sm"
          >
            Отмена
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="glass-card glow-border p-4 animate-fade-in">
      <p className="text-sm text-[#333] mb-4">
        🔥 Твой спринт: {data.streak} из 7 дней.
      </p>
      <p className="text-sm font-semibold text-[#333] mb-3">
        {texts.trk_title || "🎯 Твой план минимум на сегодня. Отмечай выполненное:"}
      </p>
      <div className="flex flex-col gap-2 mb-4">
        {TASK_IDS.map((id) => {
          const key = ["contacts", "followup", "content", "study"][id - 1];
          const done = progress[id - 1] === "1";
          const label = texts[`trk_${key}`] || key;
          return (
            <button
              key={id}
              onClick={() => {
                if (done) return;
                setReportMode({ taskId: id, label });
              }}
              disabled={done}
              className={`neu-button py-3 px-4 text-left text-sm flex items-center gap-2 ${
                done ? "opacity-70" : "hover:opacity-90"
              }`}
            >
              <span>{done ? "✅" : "❌"}</span>
              <span>{label}</span>
            </button>
          );
        })}
      </div>
      <div className="flex flex-col gap-2">
        <button
          onClick={async () => {
            try {
              const r = await fetch(`${API}/finish`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: userId }),
              });
              const body = await r.json().catch(() => ({}));
              if (!r.ok) throw new Error(body.detail || "Ошибка");
              fetchData();
            } catch (e) {
              alert(e instanceof Error ? e.message : "Выполни все задания!");
            }
          }}
          className="w-full neu-button py-2.5 text-sm flex items-center justify-center gap-2"
        >
          🏁 {texts.trk_finish || "Завершить день"}
        </button>
        <button
          onClick={async () => {
            await fetch(`${API}/reset`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ user_id: userId }),
            });
            fetchData();
          }}
          className="w-full neu-button py-2.5 text-sm flex items-center justify-center gap-2"
        >
          🔄 {texts.trk_restart_sprint || "Начать спринт заново"}
        </button>
        <button onClick={onBack} className="w-full neu-button py-2.5 text-sm text-[var(--gold-primary)] font-semibold">
          В меню
        </button>
      </div>
    </div>
  );
}
