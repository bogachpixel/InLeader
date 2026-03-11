export type LangCode = "ru" | "en" | "az" | "kk" | "it" | "es" | "de" | "zh" | "ko";

type SectionId =
  | "copywriter"
  | "objections"
  | "calculator"
  | "marketing"
  | "trainer"
  | "mentor"
  | "newbie"
  | "language"
  | "tracker"
  | "crm"
  | "analytics"
  | "tariffs"
  | "registration"
  | "referral";

interface SectionTexts {
  title: string;
  description?: string;
  buttons: string[];
}

interface CommonTexts {
  btn_wallet: string;
  btn_back: string;
  btn_back_menu: string;
  loading: string;
  walletTitle: string;
  tariff1: string;
  tariff2: string;
  tariff3: string;
}

interface UiTexts {
  menuTitle: string;
  common: CommonTexts;
  mainMenu: Record<SectionId, string>;
  sections: Record<SectionId, SectionTexts>;
}

const commonRu: CommonTexts = {
  btn_wallet: "Кошелёк",
  btn_back: "← Назад",
  btn_back_menu: "В меню",
  loading: "Загрузка...",
  walletTitle: "Тарифы",
  tariff1: "Тариф 1",
  tariff2: "Тариф 2",
  tariff3: "Тариф 3",
};

const ru: UiTexts = {
  menuTitle: "📋 Выбери раздел:",
  common: commonRu,
  mainMenu: {
    copywriter: "Умный копирайтер",
    objections: "База возражений",
    calculator: "Калькулятор",
    marketing: "Маркетинг-план",
    trainer: "AI-Тренажер продаж",
    mentor: "AI-Ментор",
    newbie: "Запуск новичка InCruises",
    language: "Сменить язык",
    tracker: "Трекер действий",
    crm: "CRM и Напоминания",
    analytics: "Аналитик встреч",
    tariffs: "Тарифы",
    registration: "Регистрация",
    referral: "Рефералка",
  },
  sections: {
    copywriter: {
      title: "Умный копирайтер",
      description: "Выбери тему — и я напишу цепляющий пост для круизного клуба:",
      buttons: [
        "Моя история прихода",
        "Безоплатное членство",
        "Топ-5 причин в круиз",
        "Заработок в клубе",
        "Круизы с детьми",
        "Мифы о круизах",
        "Итоги и мотивация",
        "Обзор лайнера",
        "Свой запрос (текстом)",
      ],
    },
    objections: {
      title: "База возражений",
      description: "Выбери возражение клиента — и я подготовлю аргументы для его отработки:",
      buttons: [
        "Нет денег",
        "Нет времени",
        "Это пирамида",
        "Семья против",
        "Не умею приглашать",
        "Боюсь качки",
        "Сложно с визами",
        "Не знаю языка",
        "Написать свой вариант",
      ],
    },
    calculator: {
      title: "Калькулятор",
      description: "Выбери тип расчёта:",
      buttons: [
        "Калькулятор Туриста",
        "Расчёт круиза ББ",
        "Конвертация ББ (Без доплат)",
        "Безоплатное членство",
      ],
    },
    marketing: {
      title: "Маркетинг-план",
      description: "Выбери нужный раздел:",
      buttons: ["Маркетинг", "Вознаграждения", "Безоплатное членство", "Задать вопрос по доходам (ИИ)"],
    },
    trainer: {
      title: "AI-Тренажер продаж",
      description: "Выбери профиль клиента для тренировки:",
      buttons: [
        "Студент (Хочет всё и сразу, боится мнения друзей)",
        "Пенсионер (Хочет путешествовать, боится обмана)",
        "Офисный сотрудник (Мечтает об увольнении, боится риска)",
        "Блогер (Нужен контент, не хочет «впаривать»)",
        "Предприниматель (Ищет систему, не верит в сетевой)",
        "Скептичный партнер (Просит факты и легальность)",
      ],
    },
    mentor: {
      title: "AI-Ментор",
      description:
        "Здесь нет воды — только глубокий анализ, выжимка опыта и четкие стратегии. Какую сферу будем прокачивать?",
      buttons: [
        "Майндсет и Мышление",
        "Искусство Продаж",
        "Стратегический Коучинг",
        "Лидерство и Менеджмент",
        "Психология Влияния",
        "MLM и Масштабирование",
      ],
    },
    newbie: {
      title: "Запуск новичка InCruises",
      description: "Добро пожаловать в команду InCruises! Выбери свою текущую цель:",
      buttons: ["Турист (Клубные привилегии +)", "Партнер (Бизнес и доход)", "ИИ-Навигатор: Мой план успеха"],
    },
    language: {
      title: "Выбери язык",
      description: undefined,
      buttons: [
        "Русский",
        "Azərbaycan",
        "English",
        "Қазақша",
        "Italiano",
        "Español",
        "Deutsch",
        "中文",
        "한국어",
      ],
    },
    tracker: {
      title: "Трекер действий",
      description: "Планируй действия и отслеживай прогресс:",
      buttons: ["Создать план на неделю", "Мои текущие задачи", "Анализ продуктивности"],
    },
    crm: {
      title: "CRM и Напоминания",
      description: "Управляй контактами и встречами:",
      buttons: ["Добавить контакт", "Настроить напоминание", "Список контактов"],
    },
    analytics: {
      title: "Аналитик встреч",
      description: "Анализируй эффективность встреч:",
      buttons: ["Статистика встреч", "Рекомендации по улучшению", "Разбор последней встречи"],
    },
    tariffs: {
      title: "Тарифы",
      description: "Узнай о тарифных планах InCruises:",
      buttons: ["Сравнить тарифы", "Рассчитать выгоду", "Вопрос по тарифам"],
    },
    registration: {
      title: "Регистрация",
      description: "Помощь с регистрацией в InCruises:",
      buttons: ["Начать регистрацию", "Вопросы по регистрации"],
    },
    referral: {
      title: "Рефералка",
      description: "Реферальная программа InCruises:",
      buttons: ["Как работает рефералка", "Мои реферальные бонусы", "Стратегия приглашений"],
    },
  },
};

const commonEn: CommonTexts = {
  btn_wallet: "Wallet",
  btn_back: "← Back",
  btn_back_menu: "To menu",
  loading: "Loading...",
  walletTitle: "Tariffs",
  tariff1: "Tariff 1",
  tariff2: "Tariff 2",
  tariff3: "Tariff 3",
};

const en: UiTexts = {
  menuTitle: "📋 Choose a section:",
  common: commonEn,
  mainMenu: {
    copywriter: "Smart Copywriter",
    objections: "Objection Database",
    calculator: "Calculator",
    marketing: "Marketing Plan",
    trainer: "AI Sales Trainer",
    mentor: "AI Mentor",
    newbie: "Newcomer Launch",
    language: "Change language",
    tracker: "Action Tracker",
    crm: "CRM & Reminders",
    analytics: "Meeting Analytics",
    tariffs: "Tariffs",
    registration: "Registration",
    referral: "Referral Program",
  },
  sections: {
    copywriter: {
      title: "Smart Copywriter",
      description: "Pick a topic — I’ll write a catchy post for the cruise club:",
      buttons: [
        "My story",
        "Free membership",
        "Top 5 reasons for a cruise",
        "Earnings in the club",
        "Cruises with kids",
        "Cruise myths",
        "Results & motivation",
        "Ship overview",
        "Custom request (text)",
      ],
    },
    objections: {
      title: "Objection Database",
      description: "Choose a client objection — I’ll prepare arguments to handle it:",
      buttons: [
        "No money",
        "No time",
        "It's a pyramid",
        "Family is against",
        "Can’t invite people",
        "Afraid of seasickness",
        "Visa is complicated",
        "Don’t know the language",
        "Write your own objection",
      ],
    },
    calculator: {
      title: "Calculator",
      description: "Choose a calculation type:",
      buttons: ["Tourist Calculator", "BB Cruise Calculation", "BB Conversion (No extra pay)", "Free membership"],
    },
    marketing: {
      title: "Marketing Plan",
      description: "Choose a section:",
      buttons: ["Marketing", "Rewards", "Free membership", "Ask income question (AI)"],
    },
    trainer: {
      title: "AI Sales Trainer",
      description: "Choose a client profile for practice:",
      buttons: [
        "Student (wants everything now, fears opinions)",
        "Retiree (wants travel, fears scams)",
        "Office worker (dreams of quitting, fears risk)",
        "Blogger (needs content, hates ‘selling’)",
        "Entrepreneur (wants systems, distrusts MLM)",
        "Skeptical partner (wants facts and legality)",
      ],
    },
    mentor: {
      title: "AI Mentor",
      description:
        "No fluff — only deep analysis, distilled experience, and clear strategies. Which area do we grow now?",
      buttons: [
        "Mindset & Thinking",
        "Sales Mastery",
        "Strategic Coaching",
        "Leadership & Management",
        "Psychology of Influence",
        "MLM & Scaling",
      ],
    },
    newbie: {
      title: "Newcomer Launch",
      description: "Welcome to the InCruises team! Choose your current goal:",
      buttons: ["Tourist (Club privileges +)", "Partner (Business & income)", "AI Navigator: My success plan"],
    },
    language: {
      title: "Choose language",
      description: undefined,
      buttons: ["Русский", "Azərbaycan", "English", "Қазақша", "Italiano", "Español", "Deutsch", "中文", "한국어"],
    },
    tracker: {
      title: "Action Tracker",
      description: "Plan your actions and track your progress:",
      buttons: ["Create weekly plan", "My current tasks", "Productivity analysis"],
    },
    crm: {
      title: "CRM & Reminders",
      description: "Manage contacts and follow-ups:",
      buttons: ["Add contact", "Set reminder", "Contacts list"],
    },
    analytics: {
      title: "Meeting Analytics",
      description: "Analyze your meeting effectiveness:",
      buttons: ["Meeting stats", "Improvement tips", "Last meeting review"],
    },
    tariffs: {
      title: "Tariffs",
      description: "Learn about InCruises tariff plans:",
      buttons: ["Compare tariffs", "Calculate benefits", "Tariff question"],
    },
    registration: {
      title: "Registration",
      description: "Help with InCruises registration:",
      buttons: ["Start registration", "Registration questions"],
    },
    referral: {
      title: "Referral Program",
      description: "InCruises referral program:",
      buttons: ["How referrals work", "My referral bonuses", "Invitation strategy"],
    },
  },
};

const commonAz: CommonTexts = {
  btn_wallet: "Pul qabı",
  btn_back: "← Geri",
  btn_back_menu: "Menyuya",
  loading: "Yüklənir...",
  walletTitle: "Tariflər",
  tariff1: "Tarif 1",
  tariff2: "Tarif 2",
  tariff3: "Tarif 3",
};

const az: UiTexts = {
  menuTitle: "📋 Bölmə seç:",
  common: commonAz,
  mainMenu: {
    copywriter: "Ağıllı Kopirayter",
    objections: "Etirazlar Bazası",
    calculator: "Kalkulyator",
    marketing: "Marketinq Planı",
    trainer: "AI Satış Təlimçisi",
    mentor: "AI Mentor",
    newbie: "Yeni Başlayanların Startı",
    language: "Dili dəyiş",
    tracker: "Fəaliyyət Trakeri",
    crm: "CRM və Xatırlatmalar",
    analytics: "Görüş Analitikası",
    tariffs: "Tariflər",
    registration: "Qeydiyyat",
    referral: "Referal Proqramı",
  },
  sections: {
    copywriter: {
      title: "Ağıllı Kopirayter",
      description: "Mövzu seç — kruiz klubu üçün cəlbedici post yazım:",
      buttons: [
        "Mənim hekayəm",
        "Ödənişsiz üzvlük",
        "Kruizə getmək üçün TOP 5 səbəb",
        "Klubda qazanc",
        "Uşaqlarla kruizlər",
        "Kruizlərlə bağlı miflər",
        "Nəticələr və motivasiya",
        "Layner icmalı",
        "Öz sorğun (mətnlə)",
      ],
    },
    objections: {
      title: "Etirazlar Bazası",
      description: "Müştərinin etirazını seç — onu bağlamağa kömək edən arqumentlər hazırlayım:",
      buttons: [
        "Pulum yoxdur",
        "Vaxtım yoxdur",
        "Bu piramidadır",
        "Ailə razı deyil",
        "Dəvət etməyi bacarmıram",
        "Dəniz xəstəliyindən qorxuram",
        "Vizalar çətindir",
        "Dili bilmirəm",
        "Öz etirazını yaz",
      ],
    },
    calculator: {
      title: "Kalkulyator",
      description: "Hesab növünü seç:",
      buttons: ["Turist Kalkulyatoru", "BB Kruiz Hesabı", "BB Konvertasiya (Əlavə ödənişsiz)", "Ödənişsiz üzvlük"],
    },
    marketing: {
      title: "Marketinq Planı",
      description: "Bölmə seç:",
      buttons: ["Marketinq", "Mükafatlar", "Ödənişsiz üzvlük", "Gəlir barədə sual ver (AI)"],
    },
    trainer: {
      title: "AI Satış Təlimçisi",
      description: "Təlim üçün müştəri profilini seç:",
      buttons: [
        "Tələbə (hər şeyi tez istəyir, fikirlərdən qorxur)",
        "Pensioner (səyahət etmək istəyir, aldanmaqdan qorxur)",
        "Ofis işçisi (işdən çıxmaq arzusundadır, riskdən qorxur)",
        "Bloqçu (kontentə ehtiyacı var, ‘satmağı’ istəmir)",
        "Sahibkar (sistem axtarır, şəbəkəyə inanmır)",
        "Skeptik tərəfdaş (faktlar və qanunilik istəyir)",
      ],
    },
    mentor: {
      title: "AI Mentor",
      description:
        "Burada su yoxdur — yalnız dərin analiz, təcrübənin sıxılmış forması və dəqiq strategiyalar. Hansı sahəni inkişaf etdirək?",
      buttons: [
        "Meyndset və Düşüncə tərzi",
        "Satış sənəti",
        "Strateji Kouçinq",
        "Liderlik və Menecment",
        "Təsir Psixologiyası",
        "MLM və Miqyaslandırma",
      ],
    },
    newbie: {
      title: "InCruises Yeni Başlayan",
      description: "InCruises komandasına xoş gəlmisən! Cari hədəfini seç:",
      buttons: [
        "Turist (Klub üstünlükləri +)",
        "Tərəfdaş (Biznes və gəlir)",
        "AI Naviqator: Mənim uğur planım",
      ],
    },
    language: {
      title: "Dili seç",
      description: undefined,
      buttons: ["Русский", "Azərbaycan", "English", "Қазақша", "Italiano", "Español", "Deutsch", "中文", "한국어"],
    },
    tracker: {
      title: "Fəaliyyət Trakeri",
      description: "Fəaliyyətlərini planlaşdır və nəticələri izlə:",
      buttons: ["Həftəlik plan yarat", "Cari tapşırıqlarım", "Produktivlik analizi"],
    },
    crm: {
      title: "CRM və Xatırlatmalar",
      description: "Kontaktları və görüşləri idarə et:",
      buttons: ["Kontakt əlavə et", "Xatırlatma qur", "Kontakt siyahısı"],
    },
    analytics: {
      title: "Görüş Analitikası",
      description: "Görüşlərin effektivliyini analiz et:",
      buttons: ["Görüş statistikası", "Yaxşılaşdırma tövsiyələri", "Son görüşün təhlili"],
    },
    tariffs: {
      title: "Tariflər",
      description: "InCruises tarif planları haqqında öyrən:",
      buttons: ["Tarifləri müqayisə et", "Faydanı hesabla", "Tariflərlə bağlı sual"],
    },
    registration: {
      title: "Qeydiyyat",
      description: "InCruises-də qeydiyyata kömək:",
      buttons: ["Qeydiyyata başla", "Qeydiyyat sualları"],
    },
    referral: {
      title: "Referal Proqramı",
      description: "InCruises referal proqramı:",
      buttons: ["Necə işləyir", "Referal bonuslarım", "Dəvət strategiyası"],
    },
  },
};

const commonKk: CommonTexts = {
  btn_wallet: "Әмиян",
  btn_back: "← Артқа",
  btn_back_menu: "Менюге",
  loading: "Жүктелуде...",
  walletTitle: "Тарифтер",
  tariff1: "Тариф 1",
  tariff2: "Тариф 2",
  tariff3: "Тариф 3",
};

const kk: UiTexts = {
  menuTitle: "📋 Бөлімді таңда:",
  common: commonKk,
  mainMenu: {
    copywriter: "Ақылды копирайтер",
    objections: "Қарсылықтар базасы",
    calculator: "Калькулятор",
    marketing: "Маркетинг жоспары",
    trainer: "AI-Сату тренажері",
    mentor: "AI-Ментор",
    newbie: "InCruises жаңадан бастаушы",
    language: "Тілді ауыстыру",
    tracker: "Әрекеттер трекері",
    crm: "CRM және Еске салғыштар",
    analytics: "Кездесу аналитикасы",
    tariffs: "Тарифтер",
    registration: "Тіркелу",
    referral: "Реферал бағдарламасы",
  },
  sections: {
    copywriter: {
      title: "Ақылды копирайтер",
      description: "Тақырыпты таңда — мен круиз клубына тартымды пост жазамын:",
      buttons: [
        "Менің келу тарихым",
        "Тегін мүшелік",
        "Круизге барудың ТОП-5 себебі",
        "Клубтағы табыс",
        "Балалармен круиздер",
        "Круиздер туралы мифтер",
        "Қорытынды және мотивация",
        "Лайнерге шолу",
        "Өз сұранысың (мәтінмен)",
      ],
    },
    objections: {
      title: "Қарсылықтар базасы",
      description: "Клиент қарсылығын таңда — оны жабуға көмектесетін аргументтер дайындаймын:",
      buttons: [
        "Ақшам жоқ",
        "Уақытым жоқ",
        "Бұл пирамида",
        "Отбасы қарсы",
        "Шақыруды білмеймін",
        "Теңіз сырқатынан қорқамын",
        "Виза қиын",
        "Тілді білмеймін",
        "Өз қарсылығыңды жаз",
      ],
    },
    calculator: {
      title: "Калькулятор",
      description: "Есеп түрін таңда:",
      buttons: ["Турист калькуляторы", "BB круиз есебі", "BB конвертациясы (Қосымша төлемсіз)", "Тегін мүшелік"],
    },
    marketing: {
      title: "Маркетинг жоспары",
      description: "Қажетті бөлімді таңда:",
      buttons: ["Маркетинг", "Сыйақылар", "Тегін мүшелік", "Табыс туралы сұрақ (AI)"],
    },
    trainer: {
      title: "AI-Сату тренажері",
      description: "Тренировка үшін клиент профилін таңда:",
      buttons: [
        "Студент (бәрін қазір қалайды, пікірлерден қорқады)",
        "Зейнеткер (саяхаттағысы келеді, алданудан қорқады)",
        "Офис қызметкері (жұмыстан кеткісі келеді, тәуекелден қорқады)",
        "Блогер (контент керек, «сатқысы» келмейді)",
        "Кәсіпкер (жүйе іздейді, желілікке сенбейді)",
        "Скептик серіктес (факт пен заңдылықты талап етеді)",
      ],
    },
    mentor: {
      title: "AI-Ментор",
      description:
        "Мұнда артық сөз жоқ — тек терең талдау, тәжірибенің сығындысы және нақты стратегиялар. Қай саланы дамытамыз?",
      buttons: [
        "Майнсет және Ойлау",
        "Сату өнері",
        "Стратегиялық коучинг",
        "Лидерлік және Менеджмент",
        "Әсер психологиясы",
        "MLM және Масштабтау",
      ],
    },
    newbie: {
      title: "InCruises жаңадан бастаушы",
      description: "InCruises командасына қош келдің! Қазіргі мақсатыңды таңда:",
      buttons: [
        "Турист (Клубтық артықшылықтар +)",
        "Серіктес (Бизнес және табыс)",
        "AI-Навигатор: Менің табыс жоспарым",
      ],
    },
    language: {
      title: "Тілді таңда",
      description: undefined,
      buttons: ["Русский", "Azərbaycan", "English", "Қазақша", "Italiano", "Español", "Deutsch", "中文", "한국어"],
    },
    tracker: {
      title: "Әрекеттер трекері",
      description: "Әрекеттеріңді жоспарлап, прогресті бақыла:",
      buttons: ["Апталық жоспар құру", "Ағымдағы тапсырмаларым", "Өнімділік талдауы"],
    },
    crm: {
      title: "CRM және Еске салғыштар",
      description: "Контакттар мен кездесулерді басқар:",
      buttons: ["Контакт қосу", "Еске салғыш орнату", "Контакт тізімі"],
    },
    analytics: {
      title: "Кездесу аналитикасы",
      description: "Кездесулер тиімділігін талда:",
      buttons: ["Кездесу статистикасы", "Жақсарту бойынша кеңестер", "Соңғы кездесуді талдау"],
    },
    tariffs: {
      title: "Тарифтер",
      description: "InCruises тариф жоспарлары туралы біл:",
      buttons: ["Тарифтерді салыстыру", "Пайданы есептеу", "Тарифтер бойынша сұрақ"],
    },
    registration: {
      title: "Тіркелу",
      description: "InCruises-ке тіркелуге көмек:",
      buttons: ["Тіркелуді бастау", "Тіркелу сұрақтары"],
    },
    referral: {
      title: "Реферал бағдарламасы",
      description: "InCruises реферал бағдарламасы:",
      buttons: ["Қалай жұмыс істейді", "Менің реферал бонусым", "Шақыру стратегиясы"],
    },
  },
};

const commonIt: CommonTexts = {
  btn_wallet: "Portafoglio",
  btn_back: "← Indietro",
  btn_back_menu: "Al menu",
  loading: "Caricamento...",
  walletTitle: "Tariffe",
  tariff1: "Tariffa 1",
  tariff2: "Tariffa 2",
  tariff3: "Tariffa 3",
};

const it: UiTexts = {
  menuTitle: "📋 Scegli una sezione:",
  common: commonIt,
  mainMenu: {
    copywriter: "Copywriter Intelligente",
    objections: "Banca Obiezioni",
    calculator: "Calcolatore",
    marketing: "Piano Marketing",
    trainer: "Trainer Vendite AI",
    mentor: "Mentor AI",
    newbie: "Avvio Nuovo Partner",
    language: "Cambia lingua",
    tracker: "Tracker Azioni",
    crm: "CRM e Promemoria",
    analytics: "Analisi Incontri",
    tariffs: "Tariffe",
    registration: "Registrazione",
    referral: "Programma Referral",
  },
  sections: {
    copywriter: {
      title: "Copywriter Intelligente",
      description: "Scegli un tema — e scriverò un post accattivante per il club crociere:",
      buttons: [
        "La mia storia",
        "Iscrizione gratuita",
        "Top 5 motivi per una crociera",
        "Guadagni nel club",
        "Crociere con bambini",
        "Miti sulle crociere",
        "Risultati e motivazione",
        "Panoramica della nave",
        "Richiesta personalizzata (testo)",
      ],
    },
    objections: {
      title: "Banca Obiezioni",
      description: "Scegli l’obiezione del cliente — preparerò argomenti per gestirla:",
      buttons: [
        "Non ho soldi",
        "Non ho tempo",
        "È una piramide",
        "La famiglia è contraria",
        "Non so invitare",
        "Ho paura del mal di mare",
        "Il visto è complicato",
        "Non conosco la lingua",
        "Scrivi la tua obiezione",
      ],
    },
    calculator: {
      title: "Calcolatore",
      description: "Scegli il tipo di calcolo:",
      buttons: [
        "Calcolatore Turista",
        "Calcolo crociera BB",
        "Conversione BB (senza extra)",
        "Iscrizione gratuita",
      ],
    },
    marketing: {
      title: "Piano Marketing",
      description: "Scegli la sezione:",
      buttons: ["Marketing", "Compensi", "Iscrizione gratuita", "Domanda sui guadagni (AI)"],
    },
    trainer: {
      title: "Trainer Vendite AI",
      description: "Scegli il profilo cliente per allenarti:",
      buttons: [
        "Studente (vuole tutto subito, teme il giudizio)",
        "Pensionato (vuole viaggiare, teme le truffe)",
        "Impiegato d’ufficio (sogna di licenziarsi, teme il rischio)",
        "Blogger (ha bisogno di contenuti, non vuole ‘vendere’)",
        "Imprenditore (cerca un sistema, non crede al network)",
        "Partner scettico (chiede fatti e legalità)",
      ],
    },
    mentor: {
      title: "Mentor AI",
      description:
        "Niente acqua — solo analisi profonda, esperienza concentrata e strategie chiare. Quale area alleniamo?",
      buttons: [
        "Mindset e Pensiero",
        "Arte della Vendita",
        "Coaching Strategico",
        "Leadership e Management",
        "Psicologia dell’Influenza",
        "MLM e Scalabilità",
      ],
    },
    newbie: {
      title: "Avvio Nuovo Partner",
      description: "Benvenuto nel team InCruises! Scegli il tuo obiettivo attuale:",
      buttons: [
        "Turista (Vantaggi del club +)",
        "Partner (Business e reddito)",
        "AI Navigator: Il mio piano di successo",
      ],
    },
    language: {
      title: "Scegli la lingua",
      description: undefined,
      buttons: ["Русский", "Azərbaycan", "English", "Қазақша", "Italiano", "Español", "Deutsch", "中文", "한국어"],
    },
    tracker: {
      title: "Tracker Azioni",
      description: "Pianifica le azioni e monitora i progressi:",
      buttons: ["Crea piano settimanale", "Le mie attività attuali", "Analisi produttività"],
    },
    crm: {
      title: "CRM e Promemoria",
      description: "Gestisci contatti e appuntamenti:",
      buttons: ["Aggiungi contatto", "Imposta promemoria", "Elenco contatti"],
    },
    analytics: {
      title: "Analisi Incontri",
      description: "Analizza l’efficacia degli incontri:",
      buttons: ["Statistiche incontri", "Suggerimenti di miglioramento", "Analisi dell’ultimo incontro"],
    },
    tariffs: {
      title: "Tariffe",
      description: "Scopri i piani tariffari InCruises:",
      buttons: ["Confronta tariffe", "Calcola il vantaggio", "Domanda sulle tariffe"],
    },
    registration: {
      title: "Registrazione",
      description: "Aiuto con la registrazione InCruises:",
      buttons: ["Inizia la registrazione", "Domande sulla registrazione"],
    },
    referral: {
      title: "Programma Referral",
      description: "Programma referral InCruises:",
      buttons: ["Come funziona", "I miei bonus referral", "Strategia di invito"],
    },
  },
};

const commonEs: CommonTexts = {
  btn_wallet: "Cartera",
  btn_back: "← Atrás",
  btn_back_menu: "Al menú",
  loading: "Cargando...",
  walletTitle: "Tarifas",
  tariff1: "Tarifa 1",
  tariff2: "Tarifa 2",
  tariff3: "Tarifa 3",
};

const es: UiTexts = {
  menuTitle: "📋 Elige una sección:",
  common: commonEs,
  mainMenu: {
    copywriter: "Copywriter Inteligente",
    objections: "Banco de Objeciones",
    calculator: "Calculadora",
    marketing: "Plan de Marketing",
    trainer: "Entrenador de Ventas AI",
    mentor: "Mentor AI",
    newbie: "Lanzamiento de Nuevo Socio",
    language: "Cambiar idioma",
    tracker: "Tracker de Acciones",
    crm: "CRM y Recordatorios",
    analytics: "Analítica de Reuniones",
    tariffs: "Tarifas",
    registration: "Registro",
    referral: "Programa de Referidos",
  },
  sections: {
    copywriter: {
      title: "Copywriter Inteligente",
      description: "Elige un tema — y escribiré un post atractivo para el club de cruceros:",
      buttons: [
        "Mi historia",
        "Membresía gratuita",
        "Top 5 razones para un crucero",
        "Ganancias en el club",
        "Cruceros con niños",
        "Mitos sobre los cruceros",
        "Resultados y motivación",
        "Resumen del barco",
        "Solicitud personalizada (texto)",
      ],
    },
    objections: {
      title: "Banco de Objeciones",
      description: "Elige la objeción del cliente — prepararé argumentos para manejarla:",
      buttons: [
        "No tengo dinero",
        "No tengo tiempo",
        "Es una pirámide",
        "Mi familia está en contra",
        "No sé invitar",
        "Tengo miedo al mareo",
        "La visa es complicada",
        "No conozco el idioma",
        "Escribe tu propia objeción",
      ],
    },
    calculator: {
      title: "Calculadora",
      description: "Elige el tipo de cálculo:",
      buttons: [
        "Calculadora de Turista",
        "Cálculo de crucero BB",
        "Conversión BB (sin pagos extra)",
        "Membresía gratuita",
      ],
    },
    marketing: {
      title: "Plan de Marketing",
      description: "Elige la sección:",
      buttons: ["Marketing", "Recompensas", "Membresía gratuita", "Pregunta sobre ingresos (AI)"],
    },
    trainer: {
      title: "Entrenador de Ventas AI",
      description: "Elige el perfil de cliente para practicar:",
      buttons: [
        "Estudiante (lo quiere todo ya, teme la opinión de otros)",
        "Jubilado (quiere viajar, teme ser engañado)",
        "Empleado de oficina (sueña con renunciar, teme el riesgo)",
        "Bloguero (necesita contenido, no quiere ‘vender’)",
        "Empresario (busca un sistema, no cree en el multinivel)",
        "Socio escéptico (pide hechos y legalidad)",
      ],
    },
    mentor: {
      title: "Mentor AI",
      description:
        "Sin relleno — solo análisis profundo, experiencia concentrada y estrategias claras. ¿Qué área vamos a potenciar?",
      buttons: [
        "Mindset y Pensamiento",
        "Arte de las Ventas",
        "Coaching Estratégico",
        "Liderazgo y Management",
        "Psicología de la Influencia",
        "MLM y Escalado",
      ],
    },
    newbie: {
      title: "Lanzamiento de Nuevo Socio",
      description: "¡Bienvenido al equipo InCruises! Elige tu objetivo actual:",
      buttons: [
        "Turista (Ventajas del club +)",
        "Socio (Negocio e ingresos)",
        "AI Navigator: Mi plan de éxito",
      ],
    },
    language: {
      title: "Elige idioma",
      description: undefined,
      buttons: ["Русский", "Azərbaycan", "English", "Қазақша", "Italiano", "Español", "Deutsch", "中文", "한국어"],
    },
    tracker: {
      title: "Tracker de Acciones",
      description: "Planifica tus acciones y sigue tu progreso:",
      buttons: ["Crear plan semanal", "Mis tareas actuales", "Análisis de productividad"],
    },
    crm: {
      title: "CRM y Recordatorios",
      description: "Gestiona contactos y reuniones:",
      buttons: ["Añadir contacto", "Configurar recordatorio", "Lista de contactos"],
    },
    analytics: {
      title: "Analítica de Reuniones",
      description: "Analiza la efectividad de tus reuniones:",
      buttons: ["Estadísticas de reuniones", "Consejos de mejora", "Análisis de la última reunión"],
    },
    tariffs: {
      title: "Tarifas",
      description: "Conoce los planes de tarifas de InCruises:",
      buttons: ["Comparar tarifas", "Calcular beneficio", "Pregunta sobre tarifas"],
    },
    registration: {
      title: "Registro",
      description: "Ayuda con el registro en InCruises:",
      buttons: ["Empezar registro", "Preguntas sobre registro"],
    },
    referral: {
      title: "Programa de Referidos",
      description: "Programa de referidos de InCruises:",
      buttons: ["Cómo funciona", "Mis bonos de referido", "Estrategia de invitación"],
    },
  },
};

const commonDe: CommonTexts = {
  btn_wallet: "Geldbörse",
  btn_back: "← Zurück",
  btn_back_menu: "Zum Menü",
  loading: "Laden...",
  walletTitle: "Tarife",
  tariff1: "Tarif 1",
  tariff2: "Tarif 2",
  tariff3: "Tarif 3",
};

const de: UiTexts = {
  menuTitle: "📋 Wähle einen Bereich:",
  common: commonDe,
  mainMenu: {
    copywriter: "Intelligenter Copywriter",
    objections: "Einwand-Datenbank",
    calculator: "Rechner",
    marketing: "Marketingplan",
    trainer: "AI-Verkaufstrainer",
    mentor: "AI-Mentor",
    newbie: "Start für Neue Partner",
    language: "Sprache ändern",
    tracker: "Aktions-Tracker",
    crm: "CRM & Erinnerungen",
    analytics: "Meeting-Analyse",
    tariffs: "Tarife",
    registration: "Registrierung",
    referral: "Partnerprogramm",
  },
  sections: {
    copywriter: {
      title: "Intelligenter Copywriter",
      description: "Wähle ein Thema — ich schreibe einen überzeugenden Post für den Kreuzfahrtclub:",
      buttons: [
        "Meine Geschichte",
        "Kostenlose Mitgliedschaft",
        "Top 5 Gründe für eine Kreuzfahrt",
        "Verdienst im Club",
        "Kreuzfahrten mit Kindern",
        "Mythen über Kreuzfahrten",
        "Ergebnisse & Motivation",
        "Schiffsübersicht",
        "Eigene Anfrage (Text)",
      ],
    },
    objections: {
      title: "Einwand-Datenbank",
      description: "Wähle den Einwand des Kunden — ich bereite Argumente zur Entkräftung vor:",
      buttons: [
        "Ich habe kein Geld",
        "Ich habe keine Zeit",
        "Das ist eine Pyramide",
        "Meine Familie ist dagegen",
        "Ich kann niemanden einladen",
        "Ich habe Angst vor Seekrankheit",
        "Visa ist kompliziert",
        "Ich spreche die Sprache nicht",
        "Eigenen Einwand schreiben",
      ],
    },
    calculator: {
      title: "Rechner",
      description: "Wähle die Art der Berechnung:",
      buttons: [
        "Touristen-Rechner",
        "BB-Kreuzfahrtberechnung",
        "BB-Konvertierung (ohne Aufpreis)",
        "Kostenlose Mitgliedschaft",
      ],
    },
    marketing: {
      title: "Marketingplan",
      description: "Wähle einen Bereich:",
      buttons: ["Marketing", "Vergütungen", "Kostenlose Mitgliedschaft", "Frage zu Einnahmen (AI)"],
    },
    trainer: {
      title: "AI-Verkaufstrainer",
      description: "Wähle ein Kundenprofil für das Training:",
      buttons: [
        "Student (will alles sofort, fürchtet Meinungen)",
        "Rentner (möchte reisen, fürchtet Betrug)",
        "Angestellter (träumt vom Kündigen, fürchtet Risiko)",
        "Blogger (braucht Content, will nicht „verkaufen“)",
        "Unternehmer (sucht ein System, glaubt nicht an MLM)",
        "Skeptischer Partner (fordert Fakten und Legalität)",
      ],
    },
    mentor: {
      title: "AI-Mentor",
      description:
        "Kein Blabla — nur tiefe Analyse, verdichtete Erfahrung und klare Strategien. Welchen Bereich entwickeln wir?",
      buttons: [
        "Mindset & Denken",
        "Verkaufs­kunst",
        "Strategisches Coaching",
        "Führung & Management",
        "Psychologie des Einflusses",
        "MLM & Skalierung",
      ],
    },
    newbie: {
      title: "Start für Neue Partner",
      description: "Willkommen im InCruises-Team! Wähle dein aktuelles Ziel:",
      buttons: [
        "Tourist (Clubvorteile +)",
        "Partner (Business & Einkommen)",
        "AI-Navigator: Mein Erfolgsplan",
      ],
    },
    language: {
      title: "Sprache wählen",
      description: undefined,
      buttons: ["Русский", "Azərbaycan", "English", "Қазақша", "Italiano", "Español", "Deutsch", "中文", "한국어"],
    },
    tracker: {
      title: "Aktions-Tracker",
      description: "Plane deine Aktionen und verfolge deinen Fortschritt:",
      buttons: ["Wochenplan erstellen", "Meine aktuellen Aufgaben", "Produktivitätsanalyse"],
    },
    crm: {
      title: "CRM & Erinnerungen",
      description: "Verwalte Kontakte und Termine:",
      buttons: ["Kontakt hinzufügen", "Erinnerung setzen", "Kontaktliste"],
    },
    analytics: {
      title: "Meeting-Analyse",
      description: "Analysiere die Effektivität deiner Meetings:",
      buttons: ["Meeting-Statistiken", "Verbesserungs­tipps", "Analyse des letzten Meetings"],
    },
    tariffs: {
      title: "Tarife",
      description: "Erfahre mehr über die InCruises-Tarifpläne:",
      buttons: ["Tarife vergleichen", "Vorteil berechnen", "Frage zu Tarifen"],
    },
    registration: {
      title: "Registrierung",
      description: "Hilfe bei der InCruises-Registrierung:",
      buttons: ["Registrierung starten", "Fragen zur Registrierung"],
    },
    referral: {
      title: "Partnerprogramm",
      description: "InCruises-Partnerprogramm:",
      buttons: ["Wie es funktioniert", "Meine Bonuszahlungen", "Einladungsstrategie"],
    },
  },
};

const commonZh: CommonTexts = {
  btn_wallet: "钱包",
  btn_back: "← 返回",
  btn_back_menu: "返回菜单",
  loading: "加载中...",
  walletTitle: "套餐资费",
  tariff1: "套餐 1",
  tariff2: "套餐 2",
  tariff3: "套餐 3",
};

const zh: UiTexts = {
  menuTitle: "📋 请选择模块：",
  common: commonZh,
  mainMenu: {
    copywriter: "智能文案助手",
    objections: "异议处理库",
    calculator: "计算器",
    marketing: "营销计划",
    trainer: "AI 销售训练器",
    mentor: "AI 导师",
    newbie: "新伙伴启动",
    language: "切换语言",
    tracker: "行动追踪器",
    crm: "CRM 与提醒",
    analytics: "会谈分析",
    tariffs: "套餐与资费",
    registration: "注册",
    referral: "推荐计划",
  },
  sections: {
    copywriter: {
      title: "智能文案助手",
      description: "选择主题——我会为邮轮俱乐部写出吸引人的文案：",
      buttons: [
        "我的故事",
        "免费会员资格",
        "选择邮轮的 5 大理由",
        "俱乐部收益",
        "携儿童出游",
        "邮轮相关迷思",
        "成果与激励",
        "邮轮介绍",
        "自定义请求（文字）",
      ],
    },
    objections: {
      title: "异议处理库",
      description: "选择客户的异议——我会提供有力话术帮助你应对：",
      buttons: [
        "没有钱",
        "没有时间",
        "这是金字塔骗局",
        "家人反对",
        "不会邀约",
        "怕晕船",
        "签证太复杂",
        "不会外语",
        "写下你自己的异议",
      ],
    },
    calculator: {
      title: "计算器",
      description: "选择需要的计算类型：",
      buttons: [
        "游客计算器",
        "BB 邮轮费用计算",
        "BB 转换（无额外支付）",
        "免费会员资格",
      ],
    },
    marketing: {
      title: "营销计划",
      description: "选择需要的部分：",
      buttons: ["营销", "奖励", "免费会员", "收入问题（AI）"],
    },
    trainer: {
      title: "AI 销售训练器",
      description: "选择要练习的客户画像：",
      buttons: [
        "学生（想要一切马上得到，怕他人眼光）",
        "退休者（想旅行，又怕被骗）",
        "上班族（想辞职，又怕风险）",
        "博主（需要内容，不想“推销”）",
        "企业家（寻找系统，不信直销）",
        "怀疑型伙伴（需要事实与合法性）",
      ],
    },
    mentor: {
      title: "AI 导师",
      description: "没有废话——只有深度分析、经验精华与清晰策略。我们先提升哪一块？",
      buttons: [
        "心态与思维",
        "销售艺术",
        "战略教练",
        "领导力与管理",
        "影响力心理学",
        "直销与规模化",
      ],
    },
    newbie: {
      title: "新伙伴启动",
      description: "欢迎加入 InCruises 团队！请选择你当前的目标：",
      buttons: ["游客（俱乐部权益 +）", "伙伴（事业与收入）", "AI 向导：我的成功计划"],
    },
    language: {
      title: "选择语言",
      description: undefined,
      buttons: ["Русский", "Azərbaycan", "English", "Қазақша", "Italiano", "Español", "Deutsch", "中文", "한국어"],
    },
    tracker: {
      title: "行动追踪器",
      description: "规划行动并跟踪你的进展：",
      buttons: ["制定一周计划", "当前任务", "效率分析"],
    },
    crm: {
      title: "CRM 与提醒",
      description: "管理联系人与跟进提醒：",
      buttons: ["新增联系人", "设置提醒", "联系人列表"],
    },
    analytics: {
      title: "会谈分析",
      description: "分析你的会谈效果：",
      buttons: ["会谈统计", "优化建议", "最近一次会谈复盘"],
    },
    tariffs: {
      title: "套餐与资费",
      description: "了解 InCruises 的套餐与资费计划：",
      buttons: ["对比套餐", "计算收益", "资费相关问题"],
    },
    registration: {
      title: "注册",
      description: "帮助你完成 InCruises 注册：",
      buttons: ["开始注册", "注册常见问题"],
    },
    referral: {
      title: "推荐计划",
      description: "InCruises 推荐与分成计划：",
      buttons: ["如何运作", "我的推荐奖金", "邀请策略"],
    },
  },
};

const commonKo: CommonTexts = {
  btn_wallet: "지갑",
  btn_back: "← 뒤로",
  btn_back_menu: "메뉴로",
  loading: "로딩 중...",
  walletTitle: "요금제",
  tariff1: "요금제 1",
  tariff2: "요금제 2",
  tariff3: "요금제 3",
};

const ko: UiTexts = {
  menuTitle: "📋 메뉴를 선택하세요:",
  common: commonKo,
  mainMenu: {
    copywriter: "스마트 카피라이터",
    objections: "반대 처리 데이터베이스",
    calculator: "계산기",
    marketing: "마케팅 플랜",
    trainer: "AI 세일즈 트레이너",
    mentor: "AI 멘토",
    newbie: "신규 파트너 스타트",
    language: "언어 변경",
    tracker: "액션 트래커",
    crm: "CRM 및 알림",
    analytics: "미팅 분석",
    tariffs: "요금제",
    registration: "가입",
    referral: "추천 프로그램",
  },
  sections: {
    copywriter: {
      title: "스마트 카피라이터",
      description: "주제를 선택하세요 — 크루즈 클럽을 위한 매력적인 글을 작성해 드립니다:",
      buttons: [
        "나의 스토리",
        "무료 멤버십",
        "크루즈를 가야 하는 5가지 이유",
        "클럽 수익",
        "아이들과 함께하는 크루즈",
        "크루즈에 대한 오해",
        "결과 및 동기부여",
        "선박 소개",
        "직접 요청 (텍스트)",
      ],
    },
    objections: {
      title: "반대 처리 데이터베이스",
      description: "고객의 반대를 선택하세요 — 대응할 수 있는 설득 논리를 준비해 드립니다:",
      buttons: [
        "돈이 없다",
        "시간이 없다",
        "피라미드 같다",
        "가족이 반대한다",
        "초대하는 법을 모른다",
        "멀미가 걱정된다",
        "비자가 복잡하다",
        "언어를 모른다",
        "나만의 반대를 작성",
      ],
    },
    calculator: {
      title: "계산기",
      description: "계산 유형을 선택하세요:",
      buttons: [
        "투어리스트 계산기",
        "BB 크루즈 계산",
        "BB 전환 (추가 비용 없음)",
        "무료 멤버십",
      ],
    },
    marketing: {
      title: "마케팅 플랜",
      description: "원하는 섹션을 선택하세요:",
      buttons: ["마케팅", "보너스", "무료 멤버십", "수익 질문 (AI)"],
    },
    trainer: {
      title: "AI 세일즈 트레이너",
      description: "연습할 고객 프로필을 선택하세요:",
      buttons: [
        "학생 (모든 것을 빨리 원함, 주변 시선을 두려워함)",
        "은퇴자 (여행은 원하지만 사기를 두려워함)",
        "직장인 (퇴사를 꿈꾸지만 리스크를 두려워함)",
        "블로거 (콘텐츠는 필요하지만 ‘영업’은 싫어함)",
        "사업가 (시스템을 찾고 있으며, 네트워크 마케팅을 믿지 않음)",
        "회의적인 파트너 (팩트와 합법성을 요구함)",
      ],
    },
    mentor: {
      title: "AI 멘토",
      description:
        "쓸데없는 말 없이 — 깊은 분석과 경험, 그리고 명확한 전략만 제공합니다. 어느 영역부터 성장시킬까요?",
      buttons: [
        "마인드셋 & 사고방식",
        "세일즈 스킬",
        "전략 코칭",
        "리더십 & 매니지먼트",
        "영향력 심리학",
        "MLM & 스케일링",
      ],
    },
    newbie: {
      title: "신규 파트너 스타트",
      description: "InCruises 팀에 오신 것을 환영합니다! 현재 목표를 선택하세요:",
      buttons: [
        "투어리스트 (클럽 혜택 +)",
        "파트너 (비즈니스 & 수익)",
        "AI 내비게이터: 나의 성공 플랜",
      ],
    },
    language: {
      title: "언어 선택",
      description: undefined,
      buttons: ["Русский", "Azərbaycan", "English", "Қазақша", "Italiano", "Español", "Deutsch", "中文", "한국어"],
    },
    tracker: {
      title: "액션 트래커",
      description: "실행 계획을 세우고 진행 상황을 확인하세요:",
      buttons: ["주간 계획 만들기", "현재 작업", "생산성 분석"],
    },
    crm: {
      title: "CRM 및 알림",
      description: "연락처와 리마인더를 관리하세요:",
      buttons: ["연락처 추가", "알림 설정", "연락처 목록"],
    },
    analytics: {
      title: "미팅 분석",
      description: "미팅의 효율성을 분석하세요:",
      buttons: ["미팅 통계", "개선 제안", "마지막 미팅 리뷰"],
    },
    tariffs: {
      title: "요금제",
      description: "InCruises 요금제에 대해 알아보세요:",
      buttons: ["요금제 비교", "이익 계산", "요금제 문의"],
    },
    registration: {
      title: "가입",
      description: "InCruises 가입을 도와드립니다:",
      buttons: ["가입 시작", "가입 관련 질문"],
    },
    referral: {
      title: "추천 프로그램",
      description: "InCruises 추천 및 보너스 프로그램:",
      buttons: ["어떻게 작동하나요", "나의 보너스", "초대 전략"],
    },
  },
};

export const UI_TEXTS: Record<LangCode, UiTexts> = {
  ru,
  en,
  az,
  kk,
  it,
  es,
  de,
  zh,
  ko,
};

export const DEFAULT_LANG: LangCode = "ru";

