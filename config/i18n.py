"""
All UI strings for every supported language.

Usage:  TEXTS[lang_code][key]
"""

LANGUAGES: dict[str, str] = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "kk": "🇰🇿 Қазақша",
    "it": "🇮🇹 Italiano",
    "es": "🇪🇸 Español",
    "de": "🇩🇪 Deutsch",
    "zh": "🇨🇳 中文",
    "ko": "🇰🇷 한국어",
}

TEXTS: dict[str, dict[str, str]] = {
    # ── Russian ──────────────────────────────────────────────
    "ru": {
        "choose_lang": "🌍 Выбери язык:",
        "start_greeting": "Привет, {name}! 👋\n\nЯ *InLeader* 🚢 — твой помощник для партнёров inCruises.",
        "start_guide": (
            "📖 *Краткий гайд по боту:*\n\n"
            "• ✍️ *Копирайтер* — посты под твою аудиторию\n"
            "• 🛡 *Возражения* — аргументы для клиентов\n"
            "• 🧮 *Калькулятор* — доходы и расчёт круизов\n"
            "• 📊 *Маркетинг-план* — ранги, бонусы, вопросы ИИ\n"
            "• 🎯 *Трекер* — план на день + InCoins\n"
            "• 🎭 *AI-Тренажер* — практика продаж с клиентом\n"
            "• 🧠 *Аналитик встреч* — разбор созвонов и follow-up\n"
            "• 🧠 *AI-Ментор* — коучинг от виртуальных экспертов\n"
            "• 🏆 *Рейтинг* — топ активных партнёров\n\n"
            "Нажимай кнопки меню — и вперёд! 🚀"
        ),
        "lang_stub": "✅ Язык сохранён! (Остальные языки — скоро)",
        "welcome": (
            "Привет! Я *InLeader* 🚢\n\n"
            "Помогу подготовить посты и отработать возражения.\n"
            "Нажми кнопку ниже, чтобы начать:"
        ),
        "menu_placeholder": "Выбери действие",
        "btn_back_menu": "🏠 В меню",
        "btn_menu": "📋 Меню",
        "menu_reply_hint": "⬇️ Кнопка «Меню» — всегда под рукой",
        "menu_choose": "📋 Выбери раздел:",
        "btn_copywriter": "✍️ Умный копирайтер",
        "btn_objections": "🛡 База возражений",
        "btn_change_lang": "🌍 Сменить язык",
        "btn_sales_trainer": "🎭 AI-Тренажер продаж",
        # copywriter
        "copywriter_title": (
            "✍️ *Умный копирайтер*\n\n"
            "Выбери тему — и я напишу цепляющий пост для круизного клуба:"
        ),
        "copy_story": "📖 Моя история прихода",
        "copy_free": "🎁 Безоплатное членство",
        "copy_top5": "🌍 Топ-5 причин в круиз",
        "copy_money": "💰 Заработок в клубе",
        "copy_kids": "👨‍👩‍👧‍👦 Круизы с детьми",
        "copy_myths": "🛳 Мифы о круизах",
        "copy_motivation": "🏆 Итоги и мотивация",
        "copy_liner": "🚢 Обзор лайнера",
        "copy_custom": "✍️ Свой запрос (текстом)",
        "copy_ask_custom": "О чём хочешь написать? Напиши мне тему, идею или целевую аудиторию, и я сгенерирую мощный пост:",
        "copy_custom_prompt": "Партнёр хочет пост на тему: {topic}. Напиши цепляющий пост для круизного клуба inCruises. Коротко, с эмодзи. Ответ на русском.",
        "aud_moms": "Мамы в декрете",
        "aud_entrepreneurs": "Предприниматели",
        "aud_students": "Студенты/Молодежь",
        "generating_post": "⏳ InLeader генерирует пост...",
        "post_prompt": "Напиши короткий, цепляющий пост-приглашение в круизный клуб для аудитории: {audience}. Ответ дай на русском языке.",
        "error_post": "❌ Не удалось сгенерировать пост.",
        # objections
        "objections_title": (
            "🛡 *База возражений*\n\n"
            "Выбери возражение клиента — и я подготовлю аргументы для его отработки:"
        ),
        "obj_money": "💸 Нет денег",
        "obj_time": "⏳ Нет времени",
        "obj_pyramid": "🔺 Это пирамида",
        "obj_family": "👫 Семья против",
        "obj_invite": "🗣 Не умею приглашать",
        "obj_seasick": "🌊 Боюсь качки",
        "obj_visa": "🛂 Сложно с визами",
        "obj_language": "🇬🇧 Не знаю языка",
        "obj_custom": "✍️ Написать свой вариант",
        "obj_ask_custom": "Напиши текстом возражение, которое тебе озвучил клиент, и я помогу его грамотно закрыть:",
        "objection_custom_prompt": "Отработай это возражение клиента inCruises максимально убедительно, без агрессии, опираясь на факты. Возражение: {objection}",
        "obj_no_money": "У меня нет денег",
        "obj_no_time": "Нет времени этим заниматься",
        "generating_objection": "⏳ InLeader подбирает аргументы...",
        "objection_prompt": (
            "Клиент круизного клуба inCruises озвучил возражение: «{objection}». "
            "Дай 2-3 коротких, вежливых и весомых аргумента, чтобы партнер мог легко "
            "отработать это возражение в переписке. Используй форматирование и списки. "
            "Ответ дай на русском языке."
        ),
        "error_objection": "❌ Не удалось подготовить ответ.",
        # account (бывший media)
        "btn_media": "👤 Работа в аккаунте",
        "btn_account": "👤 Работа в аккаунте",
        "account_title": "👤 *Работа в аккаунте*\n\nВыбери раздел:",
        "account_2fa": "🔐 Настроить 2FA",
        "account_2fa_intro": (
            "🔐 *Двухфакторная аутентификация (2FA)*\n\n"
            "Следуй пошаговой инструкции. После выполнения каждого шага нажимай кнопку подтверждения — "
            "только тогда откроется следующий шаг.\n\nГотов начать?"
        ),
        "account_2fa_no_file": (
            "📁 Файл с инструкцией 2FA пока не найден.\n\n"
            "Поместите файл *2FA.pdf* или *2FA.txt* в папку `documents/` или `documents/2FA/`. "
            "Изображения для шагов — `documents/2FA/step1.png`, `step2.png` и т.д."
        ),
        "account_2fa_congrats": (
            "🎉 *Поздравляем!*\n\n"
            "Ты успешно настроил двухфакторную аутентификацию. Твой аккаунт теперь надёжно защищён! 🔒\n\n"
            "Рекомендуем сохранить резервные коды в надёжном месте. Удачной работы! 🚀"
        ),
        "account_policy": "📋 Политика",
        "account_policy_no_file": "📁 Файл «Политика» не найден. Добавьте политика.pdf или политика.txt в documents/.",
        "account_policy_thinking": "⏳ InLeader готовит ответ...",
        "account_policy_ask": "Задай любой вопрос о политике — я отвечу, проверю твоё понимание и помогу разобраться.",
        "account_policy_intro_prompt": "Ты эксперт по политике inCruises. Ты изучил файл «Политика» полностью. Поприветствуй партнёра кратко. Скажи, что готов отвечать на вопросы, задавать уточняющие вопросы и проводить мини-тесты на понимание. Ответь 2–3 предложениями.",
        "account_policy_user_prompt": "Партнёр написал: «{question}»\n\nОтветь на основе политики. Если уместно — задай уточняющий вопрос или проверь, понял ли он. Будь лаконичен. Используй ТОЛЬКО данные из контекста.",
        "account_policy_system": "Ты — обучающий помощник по политике inCruises. Отвечай на вопросы, задавай контрвопросы для проверки понимания, обучай партнёров. НЕ выдумывай — используй ТОЛЬКО факты из контекста.",
        "account_btn_back_account": "◀ Назад в аккаунт",
        # marketing
        "btn_marketing": "📊 Маркетинг-план",
        "mkt_title": "📊 *Маркетинг-план*\n\nВыбери нужный раздел:",
        "mkt_ranks": "📊 Маркетинг",
        "mkt_rewards": "💰 Вознаграждения",
        "mkt_free_membership": "🎁 Безоплатное членство",
        "mkt_ask_ai": "🤖 Задать вопрос по доходам (ИИ)",
        "mkt_ranks_text": (
            "🏆 Ранги в inCruises:\n\n"
            "1. Member → Partner → Senior → Director → President\n"
            "2. Каждый ранг открывает дополнительный лидерский бонус (от 5% до 25%).\n"
            "3. Ранг зависит от объёма команды и личных продаж.\n\n"
            "💰 Партнёрство: $95, пролонгация каждые 6 месяцев.\n"
            "💎 Первый вход на Classic: $295 (тариф Classic + партнёрство, разово).\n\n"
            "Чем выше ранг — тем больше бонусов с оборота всей структуры!"
        ),
        "mkt_free_text": (
            "🎁 Безоплатное членство:\n\n"
            "Твой ежемесячный взнос $100 покрывается, если выполнено ОДНО из условий:\n\n"
            "• 5 человек ежемесячно активны (каждый платит $100/мес по своим счетам)\n"
            "• 1 активация на тарифе Премиум\n"
            "• 3 подключения на тариф Classic\n\n"
            "Фактически, ты путешествуешь и зарабатываешь — не платя за членство!"
        ),
        "mkt_ranks_ai_prompt": "Расскажи структурированно о рангах и бонусах inCruises. Включи: ранги (MD, SMD, RD, ND, ID, ED, BOD и выше), таблицу Командного Лидерского бонуса, 5 источников дохода, 5 вознаграждений, даты выплат. Используй ТОЛЬКО данные из контекста. Ответ на русском, кратко и с цифрами.",
        "mkt_free_ai_prompt": "Расскажи подробно о безоплатном членстве inCruises. Включи: 3 способа квалификации (5 активных, 1 PREMIUM, 3 Classic), что получаешь (200 BP, взнос не списывается), важные правила (партнёры с бесплатным не считаются, момент выставления счёта, возвраты), отдельно для STARTER и PREMIUM. Используй ТОЛЬКО данные из контекста. Ответ на русском, структурированно.",
        "mkt_rewards_ai_prompt": "На основе полного текста из файла «Вознаграждения» расскажи о программе доходов и вознаграждений inCruises: 5 источников дохода, 5 вознаграждений, ранги и КЛБ, даты выплат, важные правила. Структурируй ответ, используй ТОЛЬКО данные из контекста. Ответ на русском, с цифрами.",
        "mkt_ask_prompt": "✏️ Напиши свой вопрос по доходам или рангам.\n\nНапример: «Сколько я заработаю, если подключу 5 человек?»",
        "mkt_thinking": "⏳ InLeader считает...",
        "mkt_ai_prompt": "Партнер inCruises задает вопрос по маркетинг-плану: {question}. Ответь кратко, точно и с цифрами. Если для точного расчёта не хватает вводных данных, вежливо уточни их. Опирайся на официальный маркетинг-план клуба. Ответ дай на русском языке.",
        # tracker
        "btn_tracker": "🎯 Трекер действий",
        "trk_title": "🎯 Твой план минимум на сегодня. Отмечай выполненное:",
        "trk_contacts": "5 новых контактов",
        "trk_followup": "10 касаний/follow-up",
        "trk_content": "2 сторис / 1 пост",
        "trk_study": "30 мин обучения",
        "trk_finish": "🏁 Завершить день",
        "trk_all_done": "🚀 Ты супер-лидер! Все задачи выполнены! Так держать!",
        "trk_all_done_coins": "🎉 Поздравляю! Ты выполнил план на день и заработал +10 InCoins 🪙! Так держать!",
        "trk_coins_already": "🚀 План выполнен! Очки за сегодня уже начислены, возвращайся завтра 😉",
        "trk_partial": "💪 Отличное начало! Выполнено {done} из {total}. Завтра добьём остальное!",
        "trk_streak_hint": "🔥 Твой стрик: {streak} дней подряд. Закрой трекер сегодня, чтобы не потерять прогресс!",
        "trk_do_all_first": "Сначала выполни все действия!",
        "trk_all_done_already": "Ты уже выполнил все задачи на сегодня! 🎉",
        "trk_ask_report": "Молодец! Но просто нажать кнопки мало. Напиши краткий отчет: кому сегодня звонил/писал? Какие были возражения или успехи?",
        # calculator
        "btn_calc": "🧮 Калькулятор",
        "calc_title": "🧮 *Калькулятор*\n\nВыбери тип расчёта:",
        "calc_tourist_btn": "🏖 Калькулятор Туриста",
        "calc_cruise_btn": "🚢 Расчёт круиза ББ",
        "calc_conversion_btn": "🔄 Конвертация ББ (Без доплат)",
        "calc_conversion_ask": (
            "Напиши стоимость круиза и сумму налогов/сборов (если знаешь).\n\n"
            'Например: "Каюта 3500 и сборы 350" или просто "3500" '
            "(тогда сборы я посчитаю примерно как 10%)."
        ),
        "calc_conversion_parse_error": "❌ Не удалось извлечь цифры. Напиши, например: «3500» или «каюта 3500, сборы 350».",
        "calc_conversion_receipt": (
            "🧾 Расчет круиза с КОНВЕРТАЦИЕЙ (БЕЗ ДОПЛАТ):\n\n"
            "💰 Базовая стоимость: ${price}\n"
            "➖ Доступные баллы (50%): {standard_points} ББ\n"
            "🔄 Конвертация 2 к 1: {converted_points} ББ\n"
            "⚓️ Примерная стоимость: {subtotal} ББ\n"
            "📑 Налоги и сборы: ${fees}\n"
            "=======================\n"
            "🔥 Итого к списанию: {final_total} ББ (Ноль доплат с карты!)"
        ),
        "calc_bad_number": "⚠️ Введи целое положительное число.",
        "calc_tourist_ask": "🏖 Сколько месяцев ты планируешь копить баллы?\n\nВзнос: $100/мес → 200 Reward Points/мес.",
        "calc_tourist_header": "🏖 Таблица накопления баллов:",
        "calc_tourist_row": "  Месяц {month}: вложено {paid}, баллов {points}",
        "calc_tourist_total": "📊 Итого: вложено {total_paid}, накоплено {total_points} RP",
        "calc_tourist_tip": "💡 Баллы применяются как скидка при бронировании круиза!",
        "calc_cruise_ask_price": (
            "🚢 Введи заявленную цену круиза на inCruises (в USD).\n\n"
            "Например: 5845"
        ),
        "calc_cruise_ask_rp": (
            "Отлично! Теперь введи количество твоих накопленных Бонусных Баллов (ББ).\n\n"
            "Например: 1200"
        ),
        "calc_cruise_header": "🚢 Расчёт стоимости круиза:",
        "calc_cruise_listed": "📋 Заявленная цена inCruises:   ${price}",
        "calc_cruise_insider": "🏷 INsider Pricing (−17%):        ${price}   (экономия ${save})",
        "calc_cruise_rp_avail": "💎 Твои ББ:  {rp} баллов = ${value} ценности",
        "calc_cruise_rp_usable": "✅ Применимо к круизу (макс. 50%): {rp} ББ = ${value}",
        "calc_cruise_rp_not_enough": "⚠️ Твоих ББ ({rp}) не хватает на 50%. Применяем все {rp} ББ.",
        "calc_cruise_cash": "💵 Итого к оплате наличными:      ${cash}",
        "calc_cruise_savings": "🎉 Итоговая экономия:              ${save} (от заявленной цены)",
        "calc_cruise_partner_tip": (
            "💡 Если ты партнёр с Безоплатным Членством — твои взносы покрыты бонусами,\n"
            "   и реальные расходы из кармана ещё ниже!\n"
            "🏆 Партнёры с рангом могут закрыть до 100% баллами, заработанными бесплатно."
        ),
        "calc_cruise_booking_tip": "📅 Бонусные баллы применяются при бронировании за 90+ дней до круиза.",
        "calc_image_caption": "🖼 Сохрани или отправь в сторис!",
        "calc_free_member": "🎁 Безоплатное членство",
        "calc_free_member_text": "Условия безоплатного членства:\n\n1. 5 активных членов клуба\n2. ИЛИ 1 активация на тарифе Премиум\n3. ИЛИ 3 активации на тарифе Classic\n\nПри выполнении одного из условий вы получаете 200 ББ ежемесячно без оплаты взноса!",
        # simulator
        "sim_title": "🎭 *AI-Тренажер продаж*\n\nВыбери профиль клиента для тренировки:",
        "sim_persona_biz": "💼 Бизнесмен (Скептик, нет времени)",
        "sim_persona_mom": "👶 Мамочка в декрете (Хочет отдыхать, переживает за бюджет)",
        "sim_persona_tourist": "🏖 Заядлый турист (Любит Турцию, не понимает зачем круизы)",
        "sim_start_status": "⏳ Клиент подключается к чату...",
        "sim_stop_btn": "🛑 Завершить и получить разбор",
        "sim_analyzing": "⏳ InLeader анализирует диалог...",
        "sim_review_prompt": (
            "Проанализируй этот диалог продажи клуба inCruises.\n"
            "Укажи сильные стороны партнёра и его ошибки.\n"
            "Дай конкретные советы по улучшению.\n"
            "Поставь оценку от 1 до 10.\n"
            "Ответ дай на русском языке.\n\nДиалог:\n{dialogue}"
        ),
        "sim_no_messages": "⚠️ Диалог пуст — напиши хотя бы одно сообщение клиенту.",
        "sim_ended": "✅ Тренировка завершена! Вот разбор:",
        # crm
        "btn_crm": "📅 CRM и Напоминания",
        "crm_title": "📅 CRM и Напоминания (Follow-up)\n\nВыбери действие:",
        "crm_add_reminder": "➕ Добавить напоминание",
        "crm_list_reminders": "📋 Мои напоминания",
        "crm_ask_task": (
            "✏️ Напиши, о чём и когда тебе напомнить?\n\n"
            "Например:\n"
            "• «Завтра в 14:00 написать Анне про безоплатку»\n"
            "• «Через 2 часа позвонить Ивану»\n"
            "• «В пятницу в 10:00 скинуть Кате видео про круизы»"
        ),
        "crm_thinking": "⏳ Анализирую задачу...",
        "crm_confirmed": "✅ Отлично! Я напомню тебе:\n\n📌 {task}\n🕐 {dt}",
        "crm_parse_error": "❌ Не смог распознать дату/время. Попробуй написать точнее, например: «Завтра в 15:00 позвонить Ивану».",
        "crm_past_date": "❌ Указанное время уже прошло. Укажи будущую дату.",
        "crm_no_reminders": "📭 У тебя пока нет активных напоминаний.",
        "crm_list_header": "📋 Твои активные напоминания:\n",
        # onboarding
        "btn_onboarding": "🚀 Запуск новичка InCruises",
        "ob_ask_goal": (
            "👋 Добро пожаловать в команду!\n\n"
            "Чтобы я мог давать тебе максимально полезные советы, давай познакомимся. "
            "Напиши в одном-двух предложениях: ты пришёл сюда больше ради того, "
            "чтобы выгодно путешествовать, или хочешь построить мощный бизнес "
            "и выйти на пассивный доход?"
        ),
        "ob_thinking": "⏳ InLeader готовит твой персональный план...",
        # analyzer
        "btn_analyzer": "🧠 Аналитик встреч",
        "btn_mentor": "🧠 AI-Ментор",
        "analyzer_ask": (
            "🧠 Опиши, как прошла твоя встреча или созвон с клиентом.\n\n"
            "Что сказал ты? Что ответил клиент? На каком моменте диалог забуксовал?\n"
            "Чем подробнее опишешь, тем точнее будет разбор!"
        ),
        "analyzer_thinking": "⏳ InLeader анализирует диалог...",
        # leaderboard
        "btn_leaderboard": "🏆 Рейтинг команды",
        "lb_header": "📊 Топ-10 самых активных партнёров:\n",
        "lb_empty": "🏆 Рейтинг пока пуст. Выполни трекер действий первым и стань лидером! 🚀",
        # documents
        "btn_documents": "📄 Документы",
        "btn_images": "🎨 AI Картинки",
        "doc_title": "📄 *Документы*\n\nВыберите раздел:",
        "doc_cruise_protection": "🛡 Защита круиза",
        "doc_thinking": "⏳ InLeader подготавливает ответ...",
        "doc_cruise_protection_prompt": "На основе файла «Защита круиза» расскажи о защите круиза: условия, что входит, как работает. Используй ТОЛЬКО данные из контекста. Ответ на русском.",
    },
    # ── English ──────────────────────────────────────────────
    "en": {
        "choose_lang": "🌍 Choose your language:",
        "welcome": (
            "Hi! I'm *InLeader* 🚢\n\n"
            "I'll help you craft posts and handle objections.\n"
            "Tap a button below to get started:"
        ),
        "menu_placeholder": "Choose an action",
        "btn_menu": "📋 Menu",
        "menu_reply_hint": "⬇️ Menu button — always at hand",
        "btn_back_menu": "🏠 Back to menu",
        "btn_copywriter": "✍️ Smart Copywriter",
        "btn_objections": "🛡 Objection Database",
        "btn_change_lang": "🌍 Change language",
        "btn_sales_trainer": "🎭 AI Sales Trainer",
        "copywriter_title": (
            "✍️ *Smart Copywriter*\n\n"
            "Pick your target audience — I'll write a catchy invitation post for the cruise club:"
        ),
        "aud_moms": "Moms on maternity leave",
        "aud_entrepreneurs": "Entrepreneurs",
        "aud_students": "Students / Young people",
        "generating_post": "⏳ InLeader is generating a post...",
        "post_prompt": "Write a short, catchy invitation post for a cruise club aimed at: {audience}. Reply in English.",
        "error_post": "❌ Failed to generate the post.",
        "objections_title": (
            "🛡 *Objection Database*\n\n"
            "Choose a client objection — I'll prepare counter-arguments:"
        ),
        "obj_pyramid": "It's a pyramid scheme",
        "obj_no_money": "I don't have money",
        "obj_seasick": "I get seasick",
        "obj_no_time": "I have no time for this",
        "generating_objection": "⏳ InLeader is preparing arguments...",
        "objection_prompt": (
            "A cruise club inCruises client raised an objection: \"{objection}\". "
            "Give 2-3 short, polite and persuasive counter-arguments a partner can easily "
            "copy-paste in a chat. Use formatting and bullet points. Reply in English."
        ),
        "error_objection": "❌ Failed to prepare the response.",
        # media
        "btn_media": "👤 Account",
        "btn_account": "👤 Account",
        "account_title": "👤 *Account*\n\nChoose a section:",
        "account_2fa": "🔐 Set up 2FA",
        "account_2fa_intro": "🔐 *Two-Factor Authentication (2FA)*\n\nFollow the step-by-step guide. After completing each step, press the confirmation button to proceed.",
        "account_2fa_no_file": "📁 2FA instruction file not found. Place 2FA.pdf or 2FA.txt in documents/ or documents/2FA/.",
        "account_2fa_congrats": "🎉 *Congratulations!* You have successfully set up 2FA. Your account is now secure! 🔒",
        "account_policy": "📋 Policy",
        "account_policy_no_file": "📁 Policy file not found. Add policy.pdf or policy.txt to documents/.",
        "account_policy_thinking": "⏳ InLeader is preparing...",
        "account_policy_ask": "Ask any question about the policy — I'll answer, check your understanding, and help you.",
        "account_policy_intro_prompt": "You're an inCruises policy expert. You've studied the Policy file. Greet the partner briefly. Say you're ready to answer questions, ask follow-ups, and run quick quizzes. Reply in 2–3 sentences.",
        "account_policy_user_prompt": "Partner wrote: «{question}»\n\nAnswer based on the policy. If appropriate, ask a follow-up or check understanding. Be concise. Use ONLY context data.",
        "account_policy_system": "You're a policy educator for inCruises. Answer questions, ask check questions, train partners. DO NOT invent — use ONLY facts from context.",
        "account_btn_back_account": "◀ Back to account",
        # marketing
        "btn_marketing": "📊 Marketing Plan",
        "mkt_title": "📊 *Marketing Plan*\n\nChoose a section:",
        "mkt_ranks": "📊 Marketing",
        "mkt_rewards": "💰 Rewards",
        "mkt_free_membership": "🎁 Free Membership",
        "mkt_ask_ai": "🤖 Ask about income (AI)",
        "mkt_ranks_text": "🏆 inCruises Ranks:\n\n1. Member → Partner → Senior → Director → President\n2. Each rank unlocks an additional leadership bonus (5% to 25%).\n3. Rank depends on team volume and personal sales.\n\nHigher rank = bigger bonuses from your entire structure!",
        "mkt_free_text": "🎁 Free Membership:\n\nWhen you invite 1 active partner on Premium, your monthly fee is covered by team bonuses.\n\nYou travel and earn — without paying for membership!",
        "mkt_ask_prompt": "✏️ Type your question about income or ranks.\n\nExample: \"How much will I earn if I recruit 5 people?\"",
        "mkt_thinking": "⏳ InLeader is calculating...",
        "mkt_ai_prompt": "An inCruises partner asks about the marketing plan: {question}. Reply concisely, accurately, with numbers. If you need more data for an exact calculation, politely ask for it. Base your answer on the official club marketing plan. Reply in English.",
        # tracker
        "btn_tracker": "🎯 Action Tracker",
        "trk_title": "🎯 Your minimum plan for today. Check off completed tasks:",
        "trk_contacts": "5 new contacts",
        "trk_followup": "10 touches / follow-ups",
        "trk_content": "2 stories / 1 post",
        "trk_study": "30 min of learning",
        "trk_finish": "🏁 Finish the day",
        "trk_all_done": "🚀 You're a super leader! All tasks done! Keep it up!",
        "trk_all_done_coins": "🎉 Congrats! You completed today's plan and earned +10 InCoins 🪙! Keep going!",
        "trk_coins_already": "🚀 Plan done! Points for today are already awarded, come back tomorrow 😉",
        "trk_partial": "💪 Great start! Completed {done} out of {total}. Let's crush the rest tomorrow!",
        # calculator
        "btn_calc": "🧮 Calculator",
        "calc_title": "🧮 *Calculator*\n\nChoose a calculation type:",
        "calc_tourist_btn": "🏖 Tourist Calculator",
        "calc_cruise_btn": "🚢 Cruise BB Calculator",
        "calc_bad_number": "⚠️ Please enter a positive whole number.",
        "calc_tourist_ask": "🏖 How many months do you plan to save points?\n\nContribution: $100/mo → 200 Reward Points/mo.",
        "calc_tourist_header": "🏖 Points accumulation table:",
        "calc_tourist_row": "  Month {month}: invested {paid}, points {points}",
        "calc_tourist_total": "📊 Total: invested {total_paid}, accumulated {total_points} RP",
        "calc_tourist_tip": "💡 Points are applied as a discount when booking a cruise!",
        "calc_cruise_ask_price": (
            "🚢 Enter the inCruises listed cruise price (in USD).\n\n"
            "Example: 5845"
        ),
        "calc_cruise_ask_rp": (
            "Great! Now enter your total accumulated Bonus Points (BB).\n\n"
            "Example: 1200"
        ),
        "calc_cruise_header": "🚢 Cruise price breakdown:",
        "calc_cruise_listed": "📋 inCruises listed price:        ${price}",
        "calc_cruise_insider": "🏷 INsider Pricing (−17%):        ${price}   (save ${save})",
        "calc_cruise_rp_avail": "💎 Your BB:  {rp} points = ${value} value",
        "calc_cruise_rp_usable": "✅ Applicable to cruise (max 50%): {rp} BB = ${value}",
        "calc_cruise_rp_not_enough": "⚠️ Your BB ({rp}) don't cover 50%. Using all {rp} BB.",
        "calc_cruise_cash": "💵 Cash you pay:                  ${cash}",
        "calc_cruise_savings": "🎉 Total savings:                 ${save} (vs listed price)",
        "calc_cruise_partner_tip": (
            "💡 If you are a partner with Free Membership — your fees are covered by bonuses,\n"
            "   so your real out-of-pocket cost is even lower!\n"
            "🏆 Partners with rank can cover up to 100% using points earned for free."
        ),
        "calc_cruise_booking_tip": "📅 Bonus Points apply when booking 90+ days before the cruise.",
        "calc_image_caption": "🖼 Save it or share to your stories!",
        # simulator
        "sim_title": "🎭 *AI Sales Trainer*\n\nChoose a client persona to practice with:",
        "sim_persona_biz": "💼 Businessman (Skeptic, no time)",
        "sim_persona_mom": "👶 Mom on maternity leave (Wants rest, worried about budget)",
        "sim_persona_tourist": "🏖 Avid tourist (Loves Turkey, doesn't get why cruises)",
        "sim_start_status": "⏳ Client is joining the chat...",
        "sim_stop_btn": "🛑 Finish & get review",
        "sim_analyzing": "⏳ InLeader is analyzing the conversation...",
        "sim_review_prompt": (
            "Analyze this inCruises sales conversation.\n"
            "Point out the partner's strengths and mistakes.\n"
            "Give specific improvement tips.\n"
            "Rate from 1 to 10.\n"
            "Reply in English.\n\nDialogue:\n{dialogue}"
        ),
        "sim_no_messages": "⚠️ The dialogue is empty — write at least one message to the client.",
        "sim_ended": "✅ Training complete! Here's your review:",
        # crm
        "btn_crm": "📅 CRM & Reminders",
        "crm_title": "📅 CRM & Reminders (Follow-up)\n\nChoose an action:",
        "crm_add_reminder": "➕ Add reminder",
        "crm_list_reminders": "📋 My reminders",
        "crm_ask_task": (
            "✏️ What and when should I remind you about?\n\n"
            "For example:\n"
            "• 'Tomorrow at 2pm message Anna about free membership'\n"
            "• 'In 2 hours call Ivan'\n"
            "• 'Friday at 10am send Kate the cruise video'"
        ),
        "crm_thinking": "⏳ Analyzing your task...",
        "crm_confirmed": "✅ Got it! I'll remind you:\n\n📌 {task}\n🕐 {dt}",
        "crm_parse_error": "❌ Couldn't recognize the date/time. Try writing more precisely, e.g. 'Tomorrow at 3pm call Ivan'.",
        "crm_past_date": "❌ That time has already passed. Please specify a future date.",
        "crm_no_reminders": "📭 You don't have any active reminders yet.",
        "crm_list_header": "📋 Your active reminders:\n",
        # onboarding
        "btn_onboarding": "🚀 Newcomer Launch",
        "ob_welcome": (
            "👋 Welcome to the team!\n\n"
            "To get started quickly and avoid mistakes, complete this short quest.\n"
            "Ready?"
        ),
        # analyzer
        "btn_analyzer": "🧠 Meeting Analyzer",
        "analyzer_ask": (
            "🧠 Describe how your meeting or call with a client went.\n\n"
            "What did you say? What did the client reply? Where did the conversation stall?\n"
            "The more detail you provide, the more accurate the analysis!"
        ),
        "analyzer_thinking": "⏳ InLeader is analyzing the dialogue...",
        # leaderboard
        "btn_leaderboard": "🏆 Team Leaderboard",
        "lb_header": "📊 Top 10 most active partners:\n",
        "lb_empty": "🏆 The leaderboard is empty. Complete the action tracker first and become a leader! 🚀",
        # documents
        "btn_documents": "📄 Documents",
        "btn_images": "🎨 AI Images",
        "doc_title": "📄 *Documents*\n\nChoose a section:",
        "doc_cruise_protection": "🛡 Cruise Protection",
        "doc_thinking": "⏳ InLeader is preparing...",
        "doc_cruise_protection_prompt": "Based on the «Cruise Protection» file, explain cruise protection: conditions, what's included, how it works. Use ONLY data from context. Reply in English.",
    },
    # ── Kazakh ───────────────────────────────────────────────
    "kk": {
        "choose_lang": "🌍 Тілді таңдаңыз / Choose language:",
        "welcome": (
            "Сәлем! Мен *InLeader* 🚢\n\n"
            "Посттар дайындауға және қарсылықтарды өңдеуге көмектесемін.\n"
            "Бастау үшін төмендегі батырманы басыңыз:"
        ),
        "menu_placeholder": "Әрекетті таңдаңыз",
        "btn_copywriter": "✍️ Ақылды копирайтер",
        "btn_objections": "🛡 Қарсылықтар базасы",
        "btn_change_lang": "🌍 Тілді ауыстыру",
        "btn_sales_trainer": "🎭 AI-Сату тренажері",
        "copywriter_title": (
            "✍️ *Ақылды копирайтер*\n\n"
            "Мақсатты аудиторияны таңдаңыз — круиз клубына тартымды пост жазамын:"
        ),
        "aud_moms": "Декреттегі аналар",
        "aud_entrepreneurs": "Кәсіпкерлер",
        "aud_students": "Студенттер / Жастар",
        "generating_post": "⏳ InLeader пост жасап жатыр...",
        "post_prompt": "Круиз клубына қысқа, тартымды шақыру-пост жаз. Аудитория: {audience}. Қазақ тілінде жауап бер.",
        "error_post": "❌ Пост жасалмады.",
        "objections_title": (
            "🛡 *Қарсылықтар базасы*\n\n"
            "Клиент қарсылығын таңдаңыз — мен дәлелдер дайындаймын:"
        ),
        "obj_pyramid": "Бұл пирамида",
        "obj_no_money": "Менде ақша жоқ",
        "obj_seasick": "Мені теңізде жүрек айнытады",
        "obj_no_time": "Маған бұған уақыт жоқ",
        "generating_objection": "⏳ InLeader дәлелдер іздеп жатыр...",
        "objection_prompt": (
            "inCruises круиз клубының клиенті мынадай қарсылық білдірді: «{обjection}». "
            "Серіктес жазысуда осы қарсылықты оңай жеңе алатындай 2-3 қысқа, сыпайы және "
            "салмақты дәлел бер. Форматтау мен тізімдерді қолдан. Қазақ тілінде жауап бер."
        ),
        "error_objection": "❌ Жауап дайындалмады.",
        # media
        "btn_media": "🗂 Медиа және сілтемелер",
        "media_title": "📂 *Команда материалдары*\n\nТөмендегі бөлімді таңдаңыз:",
        "media_site": "🌐 Біздің сайт",
        "media_visuals": "🖼 Промо-материалдар",
        "media_pdf": "📝 PDF-Презентациялар",
        "media_video": "🎥 Zoom / Видео сілтемелері",
        "media_visuals_text": "🎨 Мұнда сторис үшін фирмалық баннерлер болады. Жақында!",
        "media_pdf_text": "📄 Мұнда компания мен маркетинг-жоспар туралы PDF-презентациялар пайда болады. Жақында!",
        "media_video_text": "🎬 Мұнда Zoom-жазбалар, оқу видеолары мен вебинарлар сілтемелері болады. Жақында!",
        # marketing
        "btn_marketing": "📊 Маркетинг-жоспар",
        "mkt_title": "📊 *Маркетинг-жоспар*\n\nБөлімді таңдаңыз:",
        "mkt_ranks": "📊 Маркетинг",
        "mkt_free_membership": "🎁 Тегін мүшелік",
        "mkt_ask_ai": "🤖 Табыс туралы сұрақ (ЖИ)",
        "mkt_ranks_text": "🏆 inCruises дәрежелері:\n\n1. Member → Partner → Senior → Director → President\n2. Әр дәреже қосымша лидерлік бонус ашады (5%-дан 25%-ға дейін).\n3. Дәреже команда көлемі мен жеке сатылымдарға байланысты.\n\nДәреже жоғары болған сайын — бонустар да көп!",
        "mkt_free_text": "🎁 Тегін мүшелік:\n\n1 белсенді Премиум серіктес шақырғанда, ай сайынғы жарна команда бонустарымен өтеледі.\n\nСен саяхаттайсың және табыс табасың — мүшелікке ақша төлемейсің!",
        "mkt_ask_prompt": "✏️ Табыс немесе дәрежелер туралы сұрағыңды жаз.\n\nМысалы: «5 адам қоссам қанша табыс табамын?»",
        "mkt_thinking": "⏳ InLeader есептеп жатыр...",
        "mkt_ai_prompt": "inCruises серіктесі маркетинг-жоспар бойынша сұрақ қойды: {question}. Қысқа, нақты, сандармен жауап бер. Егер нақты есептеу үшін деректер жетіспесе, сыпайы түрде сұра. Қазақ тілінде жауап бер.",
        # tracker
        "btn_tracker": "🎯 Әрекет трекері",
        "trk_title": "🎯 Бүгінгі минимум жоспарың. Орындалғанды белгіле:",
        "trk_contacts": "5 жаңа байланыс",
        "trk_followup": "10 жанасу/follow-up",
        "trk_content": "2 сторис / 1 пост",
        "trk_study": "30 мин оқу",
        "trk_finish": "🏁 Күнді аяқтау",
        "trk_all_done": "🚀 Сен супер лидерсің! Барлық тапсырмалар орындалды!",
        "trk_all_done_coins": "🎉 Құттықтаймыз! Бүгінгі жоспар орындалды, +10 InCoins 🪙 алдың! Жалғастыр!",
        "trk_coins_already": "🚀 Жоспар орындалды! Бүгінгі ұпайлар бұрын берілген, ертең қайт 😉",
        "trk_partial": "💪 Тамаша бастама! {done}/{total} орындалды. Ертең қалғанын аяқтаймыз!",
        # calculator
        "btn_calc": "🧮 Калькулятор",
        "calc_title": "🧮 *Калькулятор*\n\nЕсептеу түрін таңда:",
        "calc_tourist_btn": "🏖 Турист калькуляторы",
        "calc_cruise_btn": "🚢 Круиз ББ есебі",
        "calc_bad_number": "⚠️ Оң бүтін сан енгіз.",
        "calc_tourist_ask": "🏖 Неше ай балл жинағың келеді?\n\nЖарна: $100/ай → 200 Reward Points/ай.",
        "calc_tourist_header": "🏖 Балл жинау кестесі:",
        "calc_tourist_row": "  {month}-ай: салынды {paid}, баллдар {points}",
        "calc_tourist_total": "📊 Барлығы: салынды {total_paid}, жиналды {total_points} RP",
        "calc_tourist_tip": "💡 Баллдар круиз брондау кезінде жеңілдік ретінде қолданылады!",
        "calc_cruise_ask_price": "🚢 inCruises-тегі круиз бағасын долларда енгіз.\n\nМысалы: 5845",
        "calc_cruise_ask_rp": "Жарайды! Жиналған Бонустық Баллдарды (ББ) енгіз.\n\nМысалы: 1200",
        "calc_cruise_header": "🚢 Круиз бағасының есебі:",
        "calc_cruise_listed": "📋 inCruises тізімдік бағасы:    ${price}",
        "calc_cruise_insider": "🏷 INsider Pricing (−17%):        ${price}   (үнемдеу ${save})",
        "calc_cruise_rp_avail": "💎 Сенің ББ-ің:  {rp} балл = ${value} құны",
        "calc_cruise_rp_usable": "✅ Круизге қолданылады (макс. 50%): {rp} ББ = ${value}",
        "calc_cruise_rp_not_enough": "⚠️ ББ-ің ({rp}) 50%-ке жетпейді. Барлық {rp} ББ қолданамыз.",
        "calc_cruise_cash": "💵 Қолма-қол төлем:               ${cash}",
        "calc_cruise_savings": "🎉 Жалпы үнемдеу:                 ${save}",
        "calc_cruise_partner_tip": (
            "💡 Тегін мүшелік бар серіктес болсаң — жарналарың бонустармен өтеледі!\n"
            "🏆 Дәрежесі бар серіктестер тегін жинаған баллдармен 100%-ке дейін жаба алады."
        ),
        "calc_cruise_booking_tip": "📅 Бонустық баллдар круизге 90+ күн бұрын брондағанда қолданылады.",
        "calc_image_caption": "🖼 Сақтап ал немесе сторисқа жібер!",
        # simulator
        "sim_title": "🎭 *AI-Сату тренажері*\n\nЖаттығу үшін клиент профилін таңда:",
        "sim_persona_biz": "💼 Бизнесмен (Скептик, уақыты жоқ)",
        "sim_persona_mom": "👶 Декреттегі ана (Демалғысы келеді, бюджетке алаңдайды)",
        "sim_persona_tourist": "🏖 Турист (Түркияны жақсы көреді, круизді түсінбейді)",
        "sim_start_status": "⏳ Клиент чатқа қосылып жатыр...",
        "sim_stop_btn": "🛑 Аяқтау және талдау алу",
        "sim_analyzing": "⏳ InLeader диалогты талдап жатыр...",
        "sim_review_prompt": (
            "Бұл inCruises сату диалогын талда.\n"
            "Серіктестің күшті жақтары мен қателерін көрсет.\n"
            "Нақты кеңестер бер.\n"
            "1-ден 10-ға дейін баға қой.\n"
            "Қазақ тілінде жауап бер.\n\nДиалог:\n{dialogue}"
        ),
        "sim_no_messages": "⚠️ Диалог бос — клиентке кем дегенде бір хабарлама жаз.",
        "sim_ended": "✅ Жаттығу аяқталды! Міне талдау:",
        # crm
        "btn_crm": "📅 CRM және Еске салулар",
        "crm_title": "📅 CRM және Еске салулар (Follow-up)\n\nӘрекетті таңда:",
        "crm_add_reminder": "➕ Еске салу қосу",
        "crm_list_reminders": "📋 Менің еске салуларым",
        "crm_ask_task": (
            "✏️ Не туралы и қашан еске салуым керек?\n\n"
            "Мысалы:\n"
            "• «Ертең 14:00-де Аннаға безоплатка туралы жазу»\n"
            "• «2 сағаттан кейін Иванға қоңырау шалу»"
        ),
        "crm_thinking": "⏳ Тапсырманы талдап жатырмын...",
        "crm_confirmed": "✅ Жарайды! Мен саған еске саламын:\n\n📌 {task}\n🕐 {dt}",
        "crm_parse_error": "❌ Уақытты тану мүмкін болмады. Нақтырақ жаз.",
        "crm_past_date": "❌ Көрсетілген уақыт өтіп кетті. Болашақ күнді көрсет.",
        "crm_no_reminders": "📭 Белсенді еске салулар жоқ.",
        "crm_list_header": "📋 Белсенді еске салулар:\n",
        # onboarding
        "btn_onboarding": "🚀 Жаңадан бастау",
        # analyzer
        "btn_analyzer": "🧠 Кездесу талдаушы",
        "analyzer_ask": (
            "🧠 Клиентпен кездесуің қалай өткенін сипатта.\n\n"
            "Сен не айттың? Клиент не жауап берді? Қай жерде диалог тұрып қалды?\n"
            "Неғұрлым толық жазсаң, соғұрлым талдау дәлірек болады!"
        ),
        "analyzer_thinking": "⏳ InLeader диалогты талдап жатыр...",
        # leaderboard
        "btn_leaderboard": "🏆 Команда рейтингі",
        "lb_header": "📊 Ең белсенді 10 серіктес:\n",
        "lb_empty": "🏆 Рейтинг әзірге бос. Бірінші болып трекерді орында және лидер бол! 🚀",
        # documents
        "btn_documents": "📄 Құжаттар",
        "doc_title": "📄 *Құжаттар*\n\nБөлімді таңдаңыз:",
        "doc_cruise_protection": "🛡 Круиз қорғауы",
        "doc_thinking": "⏳ InLeader жауап дайындауда...",
        "doc_cruise_protection_prompt": "«Круиз қорғауы» файлына негіздеп круиз қорғауы туралы айт: шарттар, не кіреді, қалай жұмыс істейді. Тек контексттегі деректерді қолдан. Жауап қазақша.",
    },
}
