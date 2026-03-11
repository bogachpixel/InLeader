interface SubSectionButton {
  emoji: string;
  label: string;
  // Для секции выбора языка: код языка, как в боте (ru, az, en, kk, it, es, de, zh, ko)
  langCode?: string;
  // Для AI-тренажера: ключ персоны (student, pensioner, office, blogger, entrepreneur, skeptic)
  personaKey?: string;
  // Для калькулятора: тип расчёта (tourist, cruise, conversion, free)
  calcType?: "tourist" | "cruise" | "conversion" | "free";
  // Для маркетинг-плана: ranks, rewards, free_membership, ask_ai
  marketingKey?: "ranks" | "rewards" | "free_membership" | "ask_ai";
  // Для AI-Ментора: mindset, sales, coaching, management, psychology, mlm
  mentorKey?: "mindset" | "sales" | "coaching" | "management" | "psychology" | "mlm";
  // Для Запуск новичка: tourist, partner, navigator
  newbieKey?: "tourist" | "partner" | "navigator";
  // Для Регистрации: start = инструкция, questions = чат с вопросами
  registrationKey?: "start" | "questions";
}

interface SubSection {
  id: string;
  emoji: string;
  title: string;
  description?: string;
  buttons: SubSectionButton[];
}

const sections: SubSection[] = [
  {
    id: "copywriter",
    emoji: "✍️",
    title: "Умный копирайтер",
    description: "Выбери тему — и я напишу цепляющий пост для круизного клуба:",
    buttons: [
      { emoji: "🏆", label: "Моя история прихода" },
      { emoji: "🎁", label: "Безоплатное членство" },
      { emoji: "🚢", label: "Топ-5 причин в круиз" },
      { emoji: "💰", label: "Заработок в клубе" },
      { emoji: "👨‍👩‍👧‍👦", label: "Круизы с детьми" },
      { emoji: "🧩", label: "Мифы о круизах" },
      { emoji: "🏅", label: "Итоги и мотивация" },
      { emoji: "🚢", label: "Обзор лайнера" },
      { emoji: "✍️", label: "Свой запрос (текстом)" },
    ],
  },
  {
    id: "objections",
    emoji: "🛡",
    title: "База возражений",
    description: "Выбери возражение клиента — и я подготовлю аргументы для его отработки:",
    buttons: [
      { emoji: "💸", label: "Нет денег" },
      { emoji: "⏳", label: "Нет времени" },
      { emoji: "⚠️", label: "Это пирамида" },
      { emoji: "👨‍👩‍👧", label: "Семья против" },
      { emoji: "🙈", label: "Не умею приглашать" },
      { emoji: "💪", label: "Боюсь качки" },
      { emoji: "📝", label: "Сложно с визами" },
      { emoji: "🇬🇧", label: "Не знаю языка" },
      { emoji: "✏️", label: "Написать свой вариант" },
    ],
  },
  {
    id: "calculator",
    emoji: "🧮",
    title: "Калькулятор",
    description: "Выбери тип расчёта:",
    buttons: [
      { emoji: "🧳", label: "Калькулятор Туриста", calcType: "tourist" as const },
      { emoji: "🏖", label: "Расчёт круиза ББ", calcType: "cruise" as const },
      { emoji: "🔄", label: "Конвертация ББ (Без доплат)", calcType: "conversion" as const },
      { emoji: "🎁", label: "Безоплатное членство", calcType: "free" as const },
    ],
  },
  {
    id: "marketing",
    emoji: "📊",
    title: "Маркетинг-план",
    description: "Выбери нужный раздел:",
    buttons: [
      { emoji: "📊", label: "Маркетинг", marketingKey: "ranks" as const },
      { emoji: "💲", label: "Вознаграждения", marketingKey: "rewards" as const },
      { emoji: "🎁", label: "Безоплатное членство", marketingKey: "free_membership" as const },
      { emoji: "🤖", label: "Задать вопрос по доходам (ИИ)", marketingKey: "ask_ai" as const },
    ],
  },
  {
    id: "trainer",
    emoji: "🎯",
    title: "AI-Тренажер продаж",
    description: "Выбери профиль клиента для тренировки:",
    buttons: [
      { emoji: "🎓", label: "Студент (Хочет всё и сразу, боится мнения друзей)", personaKey: "student" },
      { emoji: "👵", label: "Пенсионер (Хочет путешествовать, боится обмана)", personaKey: "pensioner" },
      { emoji: "👔", label: "Офисный сотрудник (Мечтает об увольнении, боится риска)", personaKey: "office" },
      { emoji: "📸", label: "Блогер (Нужен контент, не хочет «впаривать»)", personaKey: "blogger" },
      { emoji: "🏠", label: "Предприниматель (Ищет систему, не верит в сетевой)", personaKey: "entrepreneur" },
      { emoji: "🤨", label: "Скептичный партнер (Просит факты и легальность)", personaKey: "skeptic" },
    ],
  },
  {
    id: "mentor",
    emoji: "🧠",
    title: "AI-Ментор",
    description: "Здесь нет воды — только глубокий анализ, выжимка опыта и четкие стратегии. Какую сферу будем прокачивать?",
    buttons: [
      { emoji: "🧠", label: "Майндсет и Мышление", mentorKey: "mindset" as const },
      { emoji: "💰", label: "Искусство Продаж", mentorKey: "sales" as const },
      { emoji: "🎯", label: "Стратегический Коучинг", mentorKey: "coaching" as const },
      { emoji: "👥", label: "Лидерство и Менеджмент", mentorKey: "management" as const },
      { emoji: "🧘‍♂️", label: "Психология Влияния", mentorKey: "psychology" as const },
      { emoji: "🌐", label: "MLM и Масштабирование", mentorKey: "mlm" as const },
    ],
  },
  {
    id: "newbie",
    emoji: "🚀",
    title: "Запуск новичка",
    description: "Добро пожаловать! Выбери свою текущую цель:",
    buttons: [
      { emoji: "🏖️", label: "Турист (Клубные привилегии +)", newbieKey: "tourist" as const },
      { emoji: "💼", label: "Партнер (Бизнес и доход)", newbieKey: "partner" as const },
      { emoji: "🚀", label: "ИИ-Навигатор: Мой план успеха", newbieKey: "navigator" as const },
    ],
  },
  {
    id: "language",
    emoji: "🌐",
    title: "Выбери язык",
    description: undefined,
    buttons: [
      { emoji: "🇷🇺", label: "Русский", langCode: "ru" },
      { emoji: "🇦🇿", label: "Azərbaycan", langCode: "az" },
      { emoji: "🇬🇧", label: "English", langCode: "en" },
      { emoji: "🇰🇿", label: "Қазақша", langCode: "kk" },
      { emoji: "🇮🇹", label: "Italiano", langCode: "it" },
      { emoji: "🇪🇸", label: "Español", langCode: "es" },
      { emoji: "🇩🇪", label: "Deutsch", langCode: "de" },
      { emoji: "🇨🇳", label: "中文", langCode: "zh" },
      { emoji: "🇰🇷", label: "한국어", langCode: "ko" },
    ],
  },
  // Sections that previously had no sub-pages
  {
    id: "tracker",
    emoji: "📋",
    title: "Трекер действий",
    description: "Планируй действия и отслеживай прогресс:",
    buttons: [
      { emoji: "📝", label: "Создать план на неделю" },
      { emoji: "✅", label: "Мои текущие задачи" },
      { emoji: "📊", label: "Анализ продуктивности" },
    ],
  },
  {
    id: "crm",
    emoji: "📅",
    title: "CRM и Напоминания (Follow-up)",
    description: "Выбери действие:",
    buttons: [
      { emoji: "➕", label: "Добавить напоминание" },
      { emoji: "📋", label: "Мои напоминания" },
    ],
  },
  {
    id: "analytics",
    emoji: "🧠",
    title: "Аналитик встреч",
    description: "Опиши встречу — получи разбор и совет для дожима:",
    buttons: [
      { emoji: "📊", label: "Статистика встреч" },
      { emoji: "💡", label: "Рекомендации по улучшению" },
      { emoji: "📝", label: "Разбор последней встречи" },
    ],
  },
  {
    id: "registration",
    emoji: "📝",
    title: "Регистрация",
    description: "Помощь с регистрацией в InCruises:",
    buttons: [
      { emoji: "🚀", label: "Начать регистрацию", registrationKey: "start" as const },
      { emoji: "❓", label: "Вопросы по регистрации", registrationKey: "questions" as const },
    ],
  },
];

const mainMenuButtons = [
  { emoji: "✍️", label: "Умный копирайтер", sectionId: "copywriter" },
  { emoji: "🛡", label: "База возражений", sectionId: "objections" },
  { emoji: "🧮", label: "Калькулятор", sectionId: "calculator" },
  { emoji: "📊", label: "Маркетинг-план", sectionId: "marketing" },
  { emoji: "📋", label: "Трекер действий", sectionId: "tracker" },
  { emoji: "🎯", label: "AI-Тренажер продаж", sectionId: "trainer" },
  { emoji: "📅", label: "CRM и Напоминания", sectionId: "crm" },
  { emoji: "📈", label: "Аналитик встреч", sectionId: "analytics" },
  { emoji: "🧠", label: "AI-Ментор", sectionId: "mentor" },
  { emoji: "🚀", label: "Запуск новичка", sectionId: "newbie" },
  { emoji: "📝", label: "Регистрация", sectionId: "registration" },
  { emoji: "🌐", label: "Сменить язык", sectionId: "language" },
];

export { sections, mainMenuButtons };
export type { SubSection };
