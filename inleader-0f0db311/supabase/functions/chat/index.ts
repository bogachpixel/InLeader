import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-supabase-client-platform, x-supabase-client-platform-version, x-supabase-client-runtime, x-supabase-client-runtime-version",
};

const systemPrompts: Record<string, string> = {
  copywriter: `Ты — профессиональный копирайтер для InLeader. Пиши цепляющие, эмоциональные посты для социальных сетей. Используй эмодзи, короткие абзацы, призывы к действию. Пиши на русском языке.`,
  
  objections: `Ты — эксперт по работе с возражениями в сетевом маркетинге InLeader. Давай чёткие, убедительные аргументы для отработки возражений клиентов. Используй факты, примеры, эмпатию. Отвечай структурированно. Пиши на русском языке.`,
  
  calculator: `Ты — калькулятор и финансовый консультант InLeader. Помогай рассчитывать стоимость круизов, бонусные баллы (ББ), конвертации. Давай точные расчёты и объяснения. Пиши на русском языке.`,
  
  marketing: `Ты — эксперт по маркетинг-плану InLeader. Объясняй структуру вознаграждений, ранги, бонусы, условия безоплатного членства. Давай чёткую информацию. Пиши на русском языке.`,
  
  trainer: `Ты — AI-тренажер продаж InLeader. Ты играешь роль потенциального клиента с определённым профилем. Задавай вопросы, выражай сомнения, реагируй на аргументы пользователя реалистично. Помогай тренировать навыки продаж. Пиши на русском языке.`,
  
  mentor: `Ты — AI-ментор и бизнес-коуч для партнёров InLeader. Давай глубокий анализ, стратегии, практические советы. Без воды — только выжимка опыта. Пиши на русском языке.`,
  
  newbie: `Ты — наставник для новичков InLeader. Помогай составить персональный план развития, объясняй первые шаги, мотивируй. Пиши на русском языке.`,
  
  language: `Ты — многоязычный ассистент InLeader. Отвечай на выбранном языке пользователя. Помогай с переводами и локализацией контента.`,
  
  tracker: `Ты — трекер действий для партнёров InLeader. Помогай планировать задачи, отслеживать прогресс, ставить цели. Пиши на русском языке.`,
  
  crm: `Ты — CRM-ассистент InLeader. Помогай управлять контактами, напоминаниями, встречами. Пиши на русском языке.`,
  
  analytics: `Ты — аналитик встреч InLeader. Помогай анализировать результаты встреч, давай рекомендации по улучшению. Пиши на русском языке.`,
  
  tariffs: `Ты — эксперт по тарифам InLeader. Объясняй все доступные тарифные планы, их преимущества и условия. Пиши на русском языке.`,
  
  registration: `Ты — помощник по регистрации в InLeader. Проведи пользователя через процесс регистрации шаг за шагом. Пиши на русском языке.`,
  
  referral: `Ты — эксперт по реферальной программе InLeader. Объясняй как работает реферальная система, бонусы за приглашения. Пиши на русском языке.`,
};

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { messages, section, buttonContext } = await req.json();
    const LOVABLE_API_KEY = Deno.env.get("LOVABLE_API_KEY");
    if (!LOVABLE_API_KEY) throw new Error("LOVABLE_API_KEY is not configured");

    const sysPrompt = systemPrompts[section] || "Ты — полезный ассистент InLeader. Пиши на русском языке.";
    const contextNote = buttonContext ? `\n\nПользователь выбрал: "${buttonContext}". Отвечай в контексте этого выбора.` : "";

    const response = await fetch("https://ai.gateway.lovable.dev/v1/chat/completions", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${LOVABLE_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "google/gemini-3-flash-preview",
        messages: [
          { role: "system", content: sysPrompt + contextNote },
          ...messages,
        ],
        stream: true,
      }),
    });

    if (!response.ok) {
      if (response.status === 429) {
        return new Response(JSON.stringify({ error: "Слишком много запросов, попробуйте позже." }), {
          status: 429,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }
      if (response.status === 402) {
        return new Response(JSON.stringify({ error: "Необходимо пополнить баланс." }), {
          status: 402,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }
      const t = await response.text();
      console.error("AI gateway error:", response.status, t);
      return new Response(JSON.stringify({ error: "Ошибка AI сервиса" }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    return new Response(response.body, {
      headers: { ...corsHeaders, "Content-Type": "text/event-stream" },
    });
  } catch (e) {
    console.error("chat error:", e);
    return new Response(JSON.stringify({ error: e instanceof Error ? e.message : "Unknown error" }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
