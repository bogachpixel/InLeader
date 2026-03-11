import { useState, useEffect } from "react";
import MenuButton from "@/components/MenuButton";
import SectionHeader from "@/components/SectionHeader";
import BackButton from "@/components/BackButton";
import AiChat from "@/components/AiChat";
import CalcChat from "@/components/CalcChat";
import TrackerView from "@/components/TrackerView";
import CrmView from "@/components/CrmView";
import NewbieNavigatorView from "@/components/NewbieNavigatorView";
import RegistrationView from "@/components/RegistrationView";
import FloatingBackground from "@/components/FloatingBackground";
import WalletModal from "@/components/WalletModal";
import { sections, mainMenuButtons } from "@/data/botData";
import { getTelegramId } from "@/hooks/useTelegram";
import { Wallet } from "lucide-react";
import { UI_TEXTS, DEFAULT_LANG } from "@/i18n/uiTexts";

interface ChatContext {
  sectionId: string;
  buttonLabel: string;
  personaKey?: string;
  calcType?: "tourist" | "cruise" | "conversion" | "free";
  marketingKey?: "ranks" | "rewards" | "free_membership" | "ask_ai";
  mentorKey?: "mindset" | "sales" | "coaching" | "management" | "psychology" | "mlm";
  newbieKey?: "tourist" | "partner" | "navigator";
  registrationKey?: "start" | "questions";
}

const validSectionIds = new Set(sections.map((s) => s.id));

function getInitialSection(): string | null {
  if (typeof window === "undefined") return null;
  const params = new URLSearchParams(window.location.search);
  const s = params.get("section");
  return s && validSectionIds.has(s) ? s : null;
}

const SAVED_TEXT_BY_LANG: Record<string, string> = {
  ru: "Язык сохранён",
  en: "Language saved",
  az: "Dil yadda saxlanıldı",
  kk: "Тіл сақталды",
  it: "Lingua salvata",
  es: "Idioma guardado",
  de: "Sprache gespeichert",
  zh: "语言已保存",
  ko: "언어가 저장되었습니다",
};

const LANG_BUTTONS = [
  { emoji: "🇷🇺", label: "Русский", langCode: "ru" },
  { emoji: "🇦🇿", label: "Azərbaycan", langCode: "az" },
  { emoji: "🇬🇧", label: "English", langCode: "en" },
  { emoji: "🇰🇿", label: "Қазақша", langCode: "kk" },
  { emoji: "🇮🇹", label: "Italiano", langCode: "it" },
  { emoji: "🇪🇸", label: "Español", langCode: "es" },
  { emoji: "🇩🇪", label: "Deutsch", langCode: "de" },
  { emoji: "🇨🇳", label: "中文", langCode: "zh" },
  { emoji: "🇰🇷", label: "한국어", langCode: "ko" },
];

const WELCOME_KEY = "inleader_welcome_seen";

function shouldShowWelcome(): boolean {
  if (typeof window === "undefined") return false;
  const userId = getTelegramId();
  return !localStorage.getItem(`${WELCOME_KEY}_${userId}`);
}

function dismissWelcome(): void {
  const userId = getTelegramId();
  localStorage.setItem(`${WELCOME_KEY}_${userId}`, "1");
}

const Index = () => {
  const [showWelcome, setShowWelcome] = useState(false);
  const [currentSection, setCurrentSection] = useState<string | null>(() => getInitialSection());
  const [chatContext, setChatContext] = useState<ChatContext | null>(null);
  const [inCoins, setInCoins] = useState<number | null>(null);
  const [currentLang, setCurrentLang] = useState<string | null>(null);
  const [showWalletModal, setShowWalletModal] = useState(false);

  useEffect(() => {
    setShowWelcome(shouldShowWelcome());
  }, []);

  useEffect(() => {
    const webApp = (window as unknown as { Telegram?: { WebApp?: { ready?: () => void; expand?: () => void } } }).Telegram?.WebApp;
    if (webApp) {
      webApp.ready?.();
      webApp.expand?.();
    }

    const fetchProfileAndLang = async () => {
      try {
        const userId = getTelegramId();
        const [profileResp, langResp] = await Promise.all([
          fetch(`/api/inleader/profile/${userId}`),
          fetch(`/api/inleader/lang/${userId}`),
        ]);
        if (profileResp.ok) {
          const data = await profileResp.json();
          setInCoins(data.incoins ?? 0);
        }
        if (langResp.ok) {
          const langData = await langResp.json();
          setCurrentLang(langData.lang);
        } else {
          setCurrentLang(DEFAULT_LANG);
        }
      } catch (error) {
        console.error("Ошибка загрузки профиля/языка:", error);
        setCurrentLang(DEFAULT_LANG);
      }
    };

    fetchProfileAndLang();
  }, []);

  const activeSection = sections.find((s) => s.id === currentSection);

  const openChat = (
    sectionId: string,
    buttonLabel: string,
    personaKey?: string,
    calcType?: "tourist" | "cruise" | "conversion" | "free",
    marketingKey?: "ranks" | "rewards" | "free_membership" | "ask_ai",
    mentorKey?: "mindset" | "sales" | "coaching" | "management" | "psychology" | "mlm",
    newbieKey?: "tourist" | "partner" | "navigator",
    registrationKey?: "start" | "questions"
  ) => {
    setChatContext({ sectionId, buttonLabel, personaKey, calcType, marketingKey, mentorKey, newbieKey, registrationKey });
  };

  const closeChat = () => {
    setChatContext(null);
    // Refresh balance after chat
    const fetchProfile = async () => {
      try {
        const userId = getTelegramId();
        const response = await fetch(`/api/inleader/profile/${userId}`);
        if (response.ok) {
          const data = await response.json();
          setInCoins(data.incoins);
        }
      } catch (error) {
        console.error("Ошибка загрузки профиля:", error);
      }
    };
    fetchProfile();
  };

  const handlePayment = async () => {
    console.log("Payment button clicked");
    try {
      const userId = getTelegramId();
      const resp = await fetch(`/api/inleader/generate-payment/${userId}`);
      const data = await resp.json();
      if (data.payment_url) {
        window.location.href = data.payment_url;
      } else {
        alert("Ошибка при создании платежа");
      }
    } catch (e) {
      alert("Ошибка при создании платежа");
    }
  };

  const changeLanguage = async (langCode: string) => {
    try {
      const userId = getTelegramId();
      const resp = await fetch("/api/inleader/lang", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, lang: langCode }),
      });
      if (!resp.ok) {
        console.error("Ошибка смены языка:", await resp.text());
        return;
      }
      setCurrentLang(langCode);
    } catch (e) {
      console.error("Ошибка смены языка:", e);
    }
  };

  if (showWelcome) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center p-4 relative">
        <FloatingBackground />
        <div className="w-full max-w-md relative z-10">
          <div className="glass-card glow-border p-6 animate-fade-in">
            <div className="glass-header rounded-2xl px-5 py-4 mb-4">
              <h2 className="text-xl font-display font-extrabold text-[#333] text-center mb-3">
                👋 Добро пожаловать в InLeader!
              </h2>
              <p className="text-sm text-[#333] leading-relaxed opacity-90">
                InLeader — ваш AI-помощник для партнёров inCruises. Здесь вы найдёте:
              </p>
              <ul className="text-sm text-[#333] mt-3 space-y-1.5 opacity-90 list-disc list-inside">
                <li>Умный копирайтер для постов</li>
                <li>Базу возражений и AI-тренажёр продаж</li>
                <li>Калькулятор туриста и круизов</li>
                <li>Маркетинг-план, трекер и CRM</li>
                <li>AI-ментор и аналитик встреч</li>
              </ul>
              <p className="text-sm text-[#333] mt-4 font-semibold text-[var(--gold-primary)]">
                🎁 Чтобы попробовать — мы дарим вам 10 InCoin!
              </p>
            </div>
            <button
              onClick={() => {
                dismissWelcome();
                setShowWelcome(false);
              }}
              className="w-full neu-button py-3.5 text-[var(--gold-primary)] font-bold text-base"
            >
              Перейти
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (chatContext) {
    const sec = sections.find((s) => s.id === chatContext.sectionId);
    const lang = currentLang ?? DEFAULT_LANG;
    const ui = UI_TEXTS[lang] ?? UI_TEXTS[DEFAULT_LANG];
    return (
      <div className="min-h-screen flex flex-col items-center justify-center p-4 relative">
        <FloatingBackground />
        <div className="w-full max-w-md relative z-10 flex flex-col gap-3">
          {/* Коины над окном чата */}
          <div className="flex justify-end items-center gap-1 p-2 text-[var(--gold-primary)] font-bold text-sm">
            <img src="/InCoin.png" alt="InCoin" className="coin-img w-8 h-8 object-contain shrink-0" />
            <span>{inCoins !== null ? `${inCoins} InCoins` : ui.common.loading}</span>
          </div>
          {chatContext.sectionId === "calculator" && chatContext.calcType ? (
            <CalcChat calcType={chatContext.calcType} onBack={closeChat} />
          ) : chatContext.sectionId === "registration" && chatContext.registrationKey === "start" ? (
            <RegistrationView
              onBack={closeChat}
              onSuccess={() => {
                const uid = getTelegramId();
                fetch(`/api/inleader/profile/${uid}`).then((r) => r.ok && r.json()).then((d) => d && setInCoins(d.incoins));
              }}
            />
          ) : chatContext.sectionId === "newbie" && chatContext.newbieKey === "navigator" ? (
            <NewbieNavigatorView onBack={closeChat} onSuccess={() => { const uid = getTelegramId(); fetch(`/api/inleader/profile/${uid}`).then((r) => r.ok && r.json()).then((d) => d && setInCoins(d.incoins)); }} />
          ) : (
            <AiChat
              section={chatContext.sectionId}
              sectionTitle={sec?.title || ""}
              sectionEmoji={sec?.emoji || ""}
              buttonContext={chatContext.buttonLabel}
              buttonPersonaKey={chatContext.personaKey}
              buttonMarketingKey={chatContext.marketingKey}
              buttonMentorKey={chatContext.mentorKey}
              buttonNewbieKey={chatContext.newbieKey}
              buttonRegistrationKey={chatContext.registrationKey}
              onBack={closeChat}
            />
          )}
          {/* Кнопка Назад под окном */}
          <button
            onClick={closeChat}
            className="w-full neu-button py-3 text-[var(--gold-primary)] font-bold text-sm"
          >
            {ui.common.btn_back}
          </button>
        </div>
      </div>
    );
  }

  const isZeroBalance = inCoins !== null && inCoins <= 0;
  const lang = currentLang ?? DEFAULT_LANG;
  const ui = UI_TEXTS[lang] ?? UI_TEXTS[DEFAULT_LANG];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 relative">
      <FloatingBackground />

      <div className="w-full max-w-md relative z-10">
        {/* Верхняя строка: Кошелёк/Назад слева, InCoin справа */}
        <div className="flex justify-between items-center mb-2 animate-fade-in min-h-[40px]">
          {currentSection ? (
            <button
              onClick={() => setCurrentSection(null)}
              className="p-2 -ml-2 text-[var(--gold-primary)] font-bold text-sm hover:opacity-80 transition-opacity"
            >
              {ui.common.btn_back}
            </button>
          ) : (
            <button
              onClick={() => setShowWalletModal(true)}
              className="flex items-center gap-2 p-2 -ml-2 text-[var(--gold-primary)] font-bold text-sm hover:opacity-80 transition-opacity"
            >
              <Wallet className="w-5 h-5 shrink-0" />
              {ui.common.btn_wallet}
            </button>
          )}
          <div className="flex items-center gap-1 p-2 text-[var(--gold-primary)] font-bold text-sm">
            <img src="/InCoin.png" alt="InCoin" className="coin-img w-12 h-12 object-contain shrink-0" />
            <span>
              {inCoins !== null ? `${inCoins} InCoins` : ui.common.loading}
            </span>
          </div>
        </div>

        {/* Выбор языка сверху с логотипом */}
        <div className="flex items-center gap-2 mb-3 animate-fade-in flex-wrap relative z-10">
          <span className="text-xl">🌐</span>
          {LANG_BUTTONS.map((btn) => (
            <button
              key={btn.langCode}
              type="button"
              onClick={() => btn.langCode && changeLanguage(btn.langCode)}
              className={`px-2 py-1 text-xs font-semibold rounded-lg transition-opacity hover:opacity-80 cursor-pointer select-none touch-manipulation ${
                btn.langCode === currentLang
                  ? "text-[var(--gold-primary)] bg-[var(--gold-primary)]/10"
                  : "text-[#666]"
              }`}
            >
              {btn.emoji}
            </button>
          ))}
        </div>

        {/* Hero video banner */}
        <div className="relative rounded-3xl overflow-hidden mb-5 animate-fade-in shadow-2xl">
          <video
            src="/hero-video.mp4"
            autoPlay
            loop
            muted
            playsInline
            className="w-full h-36 object-cover"
          />
        </div>

        {!currentSection ? (
          <div className="glass-card glow-border p-5 animate-fade-in">
            <div className="glass-header rounded-2xl px-5 py-4 mb-5 text-center animate-pulse-glow">
              <h2 className="text-lg font-display font-extrabold text-[#333]">
                {ui.menuTitle}
              </h2>
            </div>
            <div className="grid grid-cols-2 gap-3 stagger-children">
              {mainMenuButtons.map((btn, i) => (
                <MenuButton
                  key={btn.label}
                  emoji={btn.emoji}
                  label={ui.mainMenu[btn.sectionId as keyof typeof ui.mainMenu] ?? btn.label}
                  index={i}
                  disabled={isZeroBalance}
                  showLowBalance={isZeroBalance}
                  onClick={() => {
                    if (!btn.sectionId || isZeroBalance) return;
                    if (btn.sectionId === "analytics") {
                      openChat("analytics", "Аналитик встреч");
                    } else {
                      setCurrentSection(btn.sectionId);
                    }
                  }}
                />
              ))}
            </div>
          </div>
        ) : currentSection === "tracker" ? (
          <div className="flex flex-col gap-3">
            <TrackerView
              onBack={() => {
                setCurrentSection(null);
                const uid = getTelegramId();
                fetch(`/api/inleader/profile/${uid}`).then((r) => r.ok && r.json()).then((d) => d && setInCoins(d.incoins)).catch(() => {});
              }}
            />
          </div>
        ) : currentSection === "crm" ? (
          <div className="flex flex-col gap-3">
            <CrmView
              onBack={() => {
                setCurrentSection(null);
                const uid = getTelegramId();
                fetch(`/api/inleader/profile/${uid}`).then((r) => r.ok && r.json()).then((d) => d && setInCoins(d.incoins)).catch(() => {});
              }}
              onReminderAdded={() => {
                const uid = getTelegramId();
                fetch(`/api/inleader/profile/${uid}`).then((r) => r.ok && r.json()).then((d) => d && setInCoins(d.incoins)).catch(() => {});
              }}
            />
          </div>
        ) : (
          <div className="glass-card glow-border p-5 animate-fade-in">
            <SectionHeader
              emoji={activeSection?.emoji || ""}
              title={currentSection && ui.sections[currentSection as keyof typeof ui.sections]?.title
                ? ui.sections[currentSection as keyof typeof ui.sections].title
                : activeSection?.title || ""}
              description={currentSection && ui.sections[currentSection as keyof typeof ui.sections]?.description
                ? ui.sections[currentSection as keyof typeof ui.sections].description
                : activeSection?.description}
            />
            <div className="flex flex-col gap-3 stagger-children">
              {activeSection?.buttons.map((btn: any, i) => {
                const secTexts =
                  currentSection && ui.sections[currentSection as keyof typeof ui.sections]
                    ? ui.sections[currentSection as keyof typeof ui.sections]
                    : undefined;
                const translatedLabel = secTexts?.buttons?.[i];
                // Секция смены языка: меняем язык через API, ИИ не вызывается
                if (currentSection === "language") {
                  return (
                    <MenuButton
                      key={btn.label}
                      emoji={btn.emoji}
                      label={translatedLabel ?? btn.label}
                      index={i}
                      disabled={false}
                      showLowBalance={false}
                      note={btn.langCode && btn.langCode === currentLang ? SAVED_TEXT_BY_LANG[btn.langCode] ?? SAVED_TEXT_BY_LANG["en"] : undefined}
                      onClick={() => {
                        if (btn.langCode) changeLanguage(btn.langCode);
                      }}
                    />
                  );
                }

                return (
                  <MenuButton
                    key={btn.label}
                    emoji={btn.emoji}
                    label={translatedLabel ?? btn.label}
                    index={i}
                    disabled={isZeroBalance}
                    showLowBalance={false}
                    onClick={() => {
                      if (!isZeroBalance) openChat(currentSection!, btn.label, btn.personaKey, btn.calcType, btn.marketingKey, btn.mentorKey, btn.newbieKey, btn.registrationKey);
                    }}
                  />
                );
              })}
              <BackButton label={ui.common.btn_back_menu} onClick={() => setCurrentSection(null)} />
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="glass mt-5 px-4 py-3 text-center animate-fade-in-up">
          <p className="text-xs text-[#666] font-semibold">
            ✨ Powered by AI • InLeader Partner Assistant
          </p>
        </div>
      </div>

      <WalletModal
        isOpen={showWalletModal}
        onClose={() => setShowWalletModal(false)}
        walletTitle={ui.common.btn_wallet}
        inCoins={inCoins}
        onPayment={handlePayment}
      />
    </div>
  );
};

export default Index;
