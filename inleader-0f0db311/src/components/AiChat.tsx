import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { Send, Loader2, Sparkles } from "lucide-react";
import { streamChat, Msg } from "@/lib/chatStream";
import { useTelegram } from "@/hooks/useTelegram";

interface AiChatProps {
  section: string;
  sectionTitle: string;
  sectionEmoji: string;
  buttonContext: string;
  buttonPersonaKey?: string;
  buttonMarketingKey?: "ranks" | "rewards" | "free_membership" | "ask_ai";
  buttonMentorKey?: "mindset" | "sales" | "coaching" | "management" | "psychology" | "mlm";
  buttonNewbieKey?: "tourist" | "partner" | "navigator";
  buttonRegistrationKey?: "start" | "questions";
  onBack: () => void;
}

const AiChat = ({ section, sectionTitle, sectionEmoji, buttonContext, buttonPersonaKey, buttonMarketingKey, buttonMentorKey, buttonNewbieKey, buttonRegistrationKey, onBack }: AiChatProps) => {
  const { userId } = useTelegram();
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [autoStarted, setAutoStarted] = useState(false);
  const [askAiPrompt, setAskAiPrompt] = useState<string | null>(null);
  const [analyzerThinking, setAnalyzerThinking] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  const isMarketingAskAi = section === "marketing" && buttonMarketingKey === "ask_ai";
  const isAnalyzer = section === "analytics";
  const isMentor = section === "mentor" && !!buttonMentorKey;
  const isNewbie = section === "newbie" && (buttonNewbieKey === "tourist" || buttonNewbieKey === "partner");
  const isRegistrationQuestions = section === "registration" && buttonRegistrationKey === "questions";

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (isMarketingAskAi && userId) {
      fetch(`/api/inleader/marketing/texts?user_id=${userId}`)
        .then((r) => r.json())
        .then((d) => setAskAiPrompt(d.mkt_ask_prompt || "✏️ Напиши свой вопрос по доходам или рангам."))
        .catch(() => setAskAiPrompt("✏️ Напиши свой вопрос по доходам или рангам."));
    }
  }, [isMarketingAskAi, userId]);

  useEffect(() => {
    if (isNewbie && userId) {
      fetch(`/api/inleader/onboarding/texts?user_id=${userId}`)
        .then((r) => r.json())
        .then((d) => {
          const key = buttonNewbieKey === "tourist" ? "ob_tourist_welcome" : "ob_partner_welcome";
          setAskAiPrompt(d[key] || "Задай любой вопрос:");
        })
        .catch(() => setAskAiPrompt("Задай любой вопрос:"));
    }
  }, [isNewbie, buttonNewbieKey, userId]);

  useEffect(() => {
    if (isMentor && userId) {
      fetch(`/api/inleader/mentor/texts?user_id=${userId}`)
        .then((r) => r.json())
        .then((d) => setAskAiPrompt(d.mentor_ask || "Отличный выбор. Я готов. Опиши свою текущую ситуацию или задай вопрос:"))
        .catch(() => setAskAiPrompt("Отличный выбор. Я готов. Опиши свою текущую ситуацию или задай вопрос:"));
    }
  }, [isMentor, userId]);

  useEffect(() => {
    if (isRegistrationQuestions) {
      setAskAiPrompt("✏️ Задай любой вопрос по регистрации:");
    }
  }, [isRegistrationQuestions]);

  useEffect(() => {
    if (isAnalyzer && userId) {
      fetch(`/api/inleader/analytics/texts?user_id=${userId}`)
        .then((r) => r.json())
        .then((d) => {
          setAskAiPrompt(d.analyzer_ask || "🧠 Опиши, как прошла твоя встреча или созвон с клиентом.");
          setAnalyzerThinking(d.analyzer_thinking || "⏳ InLeader анализирует диалог...");
        })
        .catch(() => {
          setAskAiPrompt("🧠 Опиши, как прошла твоя встреча или созвон с клиентом.");
          setAnalyzerThinking("⏳ Анализирую...");
        });
    }
  }, [isAnalyzer, userId]);

  useEffect(() => {
    if (!autoStarted && !isMarketingAskAi && !isAnalyzer && !isMentor && !isNewbie && !isRegistrationQuestions) {
      setAutoStarted(true);
      startAiResponse([]);
    } else if ((isMarketingAskAi || isMentor || isNewbie || isRegistrationQuestions) && askAiPrompt) {
      setAutoStarted(true);
    } else if (isAnalyzer && askAiPrompt) {
      setAutoStarted(true);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isMarketingAskAi, isAnalyzer, isMentor, isNewbie, isRegistrationQuestions, askAiPrompt]);

  const startAiResponse = async (currentMessages: Msg[], reviewRequest = false) => {
    setIsLoading(true);
    let assistantSoFar = "";

    const upsertAssistant = (chunk: string) => {
      assistantSoFar += chunk;
      setMessages((prev) => {
        const last = prev[prev.length - 1];
        if (last?.role === "assistant") {
          return prev.map((m, i) => (i === prev.length - 1 ? { ...m, content: assistantSoFar } : m));
        }
        return [...prev, { role: "assistant", content: assistantSoFar }];
      });
    };

    try {
      await streamChat({
        messages: currentMessages,
        section,
        buttonContext: section === "trainer" && buttonPersonaKey ? buttonPersonaKey : buttonContext,
        userId: userId!,
        reviewRequest,
        marketingKey: buttonMarketingKey,
        mentorKey: buttonMentorKey,
        newbieKey: buttonNewbieKey,
        onDelta: upsertAssistant,
        onDone: () => setIsLoading(false),
      });
    } catch (e) {
      console.error(e);
      setIsLoading(false);
      const errorMsg = e instanceof Error ? e.message : "Произошла ошибка";
      setMessages((prev) => [...prev, { role: "assistant", content: `⚠️ ${errorMsg}` }]);
    }
  };

  const send = async () => {
    if (!input.trim() || isLoading) return;
    const userMsg: Msg = { role: "user", content: input.trim() };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInput("");
    await startAiResponse(newMessages);
  };

  const requestBreakdown = async () => {
    if (isLoading || messages.length < 2) return;
    await startAiResponse(messages, true);
  };

  const showBreakdownButton = (section === "objections" || section === "trainer") && messages.length >= 2;

  return (
    <div className="glass-card glow-border p-4 flex flex-col h-[80vh] max-h-[700px] animate-fade-in">
      {/* Header — без кнопки назад (она под окном) */}
      <div className="glass-header rounded-2xl px-4 py-3 mb-3 flex items-center gap-3">
        <div className="flex-1 min-w-0">
          <h2 className="text-sm font-display font-bold text-[#333] flex items-center gap-1.5">
            <span className="text-lg w-6 shrink-0">{sectionEmoji}</span> {sectionTitle}
          </h2>
          <p className="text-xs text-[#666] truncate">{buttonContext}</p>
        </div>
        <Sparkles className="w-4 h-4 shrink-0 text-[var(--gold-primary)]/60 animate-pulse" />
      </div>

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto space-y-3 mb-3 pr-1">
        {(isMarketingAskAi || isAnalyzer || isMentor || isNewbie || isRegistrationQuestions) && askAiPrompt && messages.length === 0 && !isLoading && (
          <div className="flex justify-start animate-fade-in">
            <div className="glass rounded-2xl px-4 py-3 text-sm text-[#333] max-w-[85%]">
              {askAiPrompt}
            </div>
          </div>
        )}
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"} animate-fade-in`}
          >
            <div
              className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm ${
                msg.role === "user"
                  ? "glass-header text-[#333]"
                  : "glass text-[#333]"
              }`}
            >
              {msg.role === "assistant" ? (
                <div className="prose prose-sm max-w-none prose-headings:text-[#333] prose-p:text-[#333] prose-li:text-[#333] prose-strong:text-[var(--gold-primary)] prose-a:text-[var(--gold-primary)]">
                  {section === "trainer" && (
                    <p className="text-xs font-semibold text-[var(--gold-primary)] mb-1">🎭 Клиент:</p>
                  )}
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
              ) : (
                msg.content
              )}
            </div>
          </div>
        ))}
        {isLoading && messages.length === 0 && !isMarketingAskAi && !isAnalyzer && !isMentor && !isNewbie && !isRegistrationQuestions && (
          <div className="flex justify-start animate-fade-in">
            <div className="glass rounded-2xl px-5 py-4 text-sm text-[#666] flex items-center gap-3">
              <div className="flex gap-1.5">
                <span className="typing-dot" />
                <span className="typing-dot" />
                <span className="typing-dot" />
              </div>
              <span className="text-xs">AI думает...</span>
            </div>
          </div>
        )}
        {isLoading && messages.length > 0 && messages[messages.length - 1]?.role === "user" && (
          <div className="flex justify-start animate-fade-in">
            <div className="glass rounded-2xl px-5 py-4 text-sm text-[#666] flex items-center gap-3">
              <div className="flex gap-1.5">
                <span className="typing-dot" />
                <span className="typing-dot" />
                <span className="typing-dot" />
              </div>
              <span className="text-xs">{isAnalyzer && analyzerThinking ? analyzerThinking : undefined}</span>
            </div>
          </div>
        )}
      </div>

      {/* Кнопка "Остановить и разбор" для objections и trainer */}
      {showBreakdownButton && (
        <button
          onClick={requestBreakdown}
          disabled={isLoading}
          className="w-full neu-button py-2.5 mb-2 text-sm text-[var(--gold-primary)] font-semibold disabled:opacity-50"
        >
          🛑 Остановить и получить разбор
        </button>
      )}

      {/* Input */}
      <div className="flex gap-2 animate-slide-in-bottom">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && send()}
          placeholder={
            isMarketingAskAi
              ? "Например: Сколько заработаю при 5 подключениях?"
              : isAnalyzer
                ? "Опиши встречу: что сказал ты, что ответил клиент, где диалог забуксовал..."
                : isMentor
                  ? "Опиши свою текущую ситуацию или задай вопрос..."
                    : isNewbie
                    ? "Задай любой вопрос..."
                    : isRegistrationQuestions
                      ? "Например: Что нужно для регистрации?"
                      : "Напишите сообщение..."
          }
          disabled={isLoading}
          className="flex-1 neu-button px-4 py-3.5 text-sm text-[#333] outline-none placeholder:text-[#999] disabled:opacity-50 focus:shadow-[0_0_20px_rgba(212,175,55,0.3)]"
        />
        <button
          onClick={send}
          disabled={isLoading || !input.trim()}
          className="neu-button px-4 py-3.5 text-[var(--gold-primary)] disabled:opacity-30 transition-colors duration-300 shrink-0"
        >
          {isLoading ? <Loader2 className="w-5 h-5 shrink-0 animate-spin" /> : <Send className="w-5 h-5 shrink-0" />}
        </button>
      </div>
    </div>
  );
};

export default AiChat;
