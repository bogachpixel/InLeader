"""
All UI strings for every supported language.

Usage:  TEXTS[lang_code][key]
"""

LANGUAGES: dict[str, str] = {
    "ru": "🇷🇺 Русский",
    "az": "🇦🇿 Azərbaycan",
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
        "lang_stub": "✅ Язык сохранён!",
        "welcome": (
            "Привет! Я *InLeader* 🚢\n\n"
            "Помогу подготовить посты и отработать возражения.\n"
            "Нажми кнопку ниже, чтобы начать:"
        ),
        "menu_placeholder": "Выбери действие",
        "btn_back_menu": "🏠 В меню",
        "btn_back": "🔙 Назад",
        "btn_menu": "📋 Меню",
        "btn_balance": "💰 Мой баланс",
        "btn_topup": "💰 Пополнить",
        "btn_tariffs": "💎 Тарифы",
        "btn_registration": "📝 Регистрация",
        "btn_referral": "🔗 Рефералка",
        "btn_continue": "🚀 Продолжить",
        "btn_pay": "💳 Оплатить",
        "btn_pay_amount": "💳 Оплатить {amount}₽",
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
        "account_2fa_step_done": "✅ Выполнил, к следующему шагу",
        "account_2fa_finish": "✅ Готово! Завершить",
        "account_2fa_start": "🚀 Начать настройку 2FA",
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
        "trk_restart_sprint": "🔄 Начать спринт заново",
        "trk_done_today": "✅ План на сегодня выполнен!\n🔥 Твой стрик: {streak} дней. Возвращайся завтра, чтобы продолжить спринт!",
        "trk_choose_tz": "🌍 Чтобы я напоминал тебе о трекере ровно в 20:00, выбери свой часовой пояс:",
        "tz_2": "UTC+2 Европа",
        "tz_3": "UTC+3 Москва",
        "tz_4": "UTC+4 Екатеринбург",
        "tz_5": "UTC+5 Астана/Ташкент",
        "tz_6": "UTC+6 Алматы/Бишкек",
        "tz_7": "UTC+7 Новосибирск/Бангкок",
        "tz_8": "UTC+8 Иркутск/Сингапур",
        "trk_task_done_already": "✅ Это задание уже выполнено сегодня!",
        "trk_report_prompt": "📝 Отчет по заданию: *{label}*\n\nНапиши кратко, что именно сделано?",
        "trk_report_too_short": "❌ Слишком короткий отчет. Распиши подробнее!",
        "trk_task_accepted": "✅ Задание принято!",
        "trk_sprint_reset": "🔄 Спринт сброшен!",
        "trk_reminder": "⏰ Капитан! Время 20:00, а твой Журнал пуст! Зайди в Трекер, иначе твой стрик сгорит!",
        "crm_reminder_header": "🔔 *Напоминание (Follow-up):*",
        "paywall_text": (
            "⚠️ <b>Доступ ограничен</b>\n\n"
            "Твой тестовый период или текущий баланс InCoins подошли к концу. "
            "Инструменты бота ждут тебя, но для их запуска необходимо подзарядить кошелек.\n\n"
            "💎 <b>Пополни баланс и продолжай творить вместе с ИИ!</b>\n\n"
            "<i>Для пополнения баланса и активации всех функций обратись к своему наставнику или администратору.</i>"
        ),
        "coin_deducted": "⚡️ Успешно! Списана 1 монета. Остаток: {coins} 🪙",
        "payment_success": "✅ <b>Пополнение прошло успешно!</b>\n\nНа ваш баланс зачислено <b>{coins} InCoins</b> 🪙\nСумма оплаты: {amount:.2f} ₽",
        "payment_success_cryptopay": "💎 Поздравляем! Оплата через CryptoPay прошла успешно. Баланс пополнен.",
        "blocked_msg": "🚫 Ваш доступ к боту заблокирован администратором.",
        "welcome_back": "С возвращением, {name}! 👋\n\nНа твоём балансе осталось <b>{coins} InCoins</b> 🪙",
        "wallet_text": "💳 <b>Ваш кошелёк:</b>\n\nДоступно: <b>{coins} InCoins</b> 🪙\n\n<i>💡 1 генерация ИИ = 1 InCoin.</i>",
        "test_mode_text": (
            "⚙️ <b>Внимание: Тестовый режим</b>\n\n"
            "Вы получили доступ к InLeader в режиме закрытого бета-тестирования. "
            "Вам начислено <b>5 InCoins</b> 🪙 для бесплатного тестирования ИИ-функций.\n\n"
            "📉 <b>Стоимость:</b> 1 генерация = 1 InCoin.\n"
            "Когда монеты закончатся, доступ к ИИ будет приостановлен до пополнения баланса.\n\n"
            "Используйте монеты с умом, чтобы оценить мощь наших инструментов! 🚢"
        ),
        "name_friend": "друг",
        "balance_screen": "💳 <b>Ваш кошелёк</b>\n\nДоступно: <b>{coins} InCoins</b> 🪙\n\n<i>1 генерация ИИ = 1 InCoin</i>\n\nВыберите сумму пополнения:",
        "balance_topup_text": "💳 <b>Пополнение на {amount} ₽</b>\n\n1 ₽ = 1 InCoin\nПосле оплаты вы получите <b>{amount} InCoins</b>.\n\nНажмите кнопку ниже для перехода к оплате:",
        "balance_payment_error": "❌ Ошибка настройки платежей. Обратитесь к администратору.",
        "tariff_desc": "Выберите подходящий пакет InCoins для доступа к AI-инструментам InLeader. InCoins позволяют генерировать контент, отрабатывать возражения и проводить аудит профилей.",
        "tariff_title": "💎 <b>Тарифы InCoins</b>\n\n{desc}\n\nВыберите пакет:",
        "tariff_trial": "Проба",
        "tariff_standard": "Стандарт",
        "tariff_leader": "Лидер",
        "tariff_pay_text": "💎 <b>{label}</b> — {coins} InCoins\n\nСумма к оплате: <b>{amount} ₽</b>\n\nНажмите кнопку ниже для перехода к оплате:",
        "admin_free": "👑 Администратор пользуется ботом бесплатно.",
        "tariff_error": "❌ Ошибка выбора тарифа.",
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
        "sim_persona_student": "🎓 Студент (Хочет всё и сразу, боится мнения друзей)",
        "sim_persona_pensioner": "👵 Пенсионер (Хочет путешествовать, боится обмана)",
        "sim_persona_office": "👔 Офисный сотрудник (Мечтает об увольнении, боится риска)",
        "sim_persona_blogger": "📸 Блогер (Нужен контент, не хочет «впаривать»)",
        "sim_persona_entrepreneur": "🏠 Предприниматель (Ищет систему, не верит в сетевой)",
        "sim_persona_skeptic": "🤨 Скептичный партнер (Просит факты и легальность)",
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
        "ob_tourist": "🏖️ Турист (Клубные привилегии +)",
        "ob_partner": "💼 Партнер (Бизнес и доход)",
        "ob_navigator": "🚀 ИИ-Навигатор: Мой план успеха",
        "ob_welcome": "👋 Добро пожаловать в команду InCruises!\n\nЧтобы я подготовил для тебя персональный план развития, выбери свою текущую цель:",
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
        "mentor_title": "🧠 <b>Твой личный Совет Директоров на связи!</b>\n\nЗдесь нет воды — только глубокий анализ, выжимка опыта и четкие стратегии. В любой непонятной ситуации обращайся к своим AI-наставникам.\n\nКакую сферу будем прокачивать сейчас? Выбери эксперта:",
        "mentor_mindset": "🧠 Майндсет и Мышление",
        "mentor_sales": "💰 Искусство Продаж",
        "mentor_coaching": "🎯 Стратегический Коучинг",
        "mentor_management": "👥 Лидерство и Менеджмент",
        "mentor_psychology": "🧘‍♂️ Психология Влияния",
        "mentor_mlm": "🌐 MLM и Масштабирование",
        "mentor_ask": "Отличный выбор. Я готов. Опиши свою текущую ситуацию или задай вопрос:",
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
    # ── Azerbaijani ───────────────────────────────────────────────
    "az": {
        "choose_lang": "🌍 Dil seçin:",
        "start_greeting": "Salam, {name}! 👋\n\nMən *InLeader* 🚢 — inCruises tərəfdaşları üçün köməkçinizəm.",
        "start_guide": (
            "📖 *Bot haqqında qısa bələdçi:*\n\n"
            "• ✍️ *Kopyrayter* — auditoriyanız üçün postlar\n"
            "• 🛡 *Etirazlar* — müştərilər üçün arqumentlər\n"
            "• 🧮 *Kalkulyator* — gəlir və kruiz hesablamaları\n"
            "• 📊 *Marketinq planı* — dərəcələr, bonuslar, AI suallar\n"
            "• 🎯 *Trekker* — günlük plan + InCoins\n"
            "• 🎭 *AI-Treyner* — müştəri ilə satış praktikası\n"
            "• 🧠 *Görüş analitiki* — zəng və follow-up təhlili\n"
            "• 🧠 *AI-Mentor* — virtual mütəxəssislərdən koçinq\n"
            "• 🏆 *Reytinq* — ən aktiv tərəfdaşlar\n\n"
            "Menyu düymələrinə bas — və irəlilə! 🚀"
        ),
        "lang_stub": "✅ Dil saxlanıldı!",
        "welcome": (
            "Salam! Mən *InLeader* 🚢\n\n"
            "Postlar hazırlamağa və etirazları işləməyə kömək edəcəyəm.\n"
            "Başlamaq üçün aşağıdakı düyməyə bas:"
        ),
        "menu_placeholder": "Əməliyyat seçin",
        "btn_back_menu": "🏠 Menyaya",
        "btn_back": "🔙 Geri",
        "btn_menu": "📋 Menyu",
        "btn_balance": "💰 Balansım",
        "btn_topup": "💰 Yüklə",
        "btn_tariffs": "💎 Tariflər",
        "btn_registration": "📝 Qeydiyyat",
        "btn_referral": "🔗 Referal",
        "btn_continue": "🚀 Davam et",
        "btn_pay": "💳 Ödə",
        "btn_pay_amount": "💳 {amount}₽ ödə",
        "menu_reply_hint": "⬇️ «Menyu» düyməsi — həmişə əlində",
        "menu_choose": "📋 Bölmə seçin:",
        "btn_copywriter": "✍️ Ağıllı kopyrayter",
        "btn_objections": "🛡 Etirazlar bazası",
        "btn_change_lang": "🌍 Dil dəyiş",
        "btn_sales_trainer": "🎭 AI-Satış treyneri",
        "copywriter_title": (
            "✍️ *Ağıllı kopyrayter*\n\n"
            "Mövzu seç — kruiz klubu üçün cəlbedici post yazacağam:"
        ),
        "copy_story": "📖 Mənim gəliş tarixçəm",
        "copy_free": "🎁 Pulsuz üzvlük",
        "copy_top5": "🌍 Kruizda top-5 səbəb",
        "copy_money": "💰 Klubda qazanç",
        "copy_kids": "👨‍👩‍👧‍👦 Uşaqlarla kruizlər",
        "copy_myths": "🛳 Kruizlar haqqında mifler",
        "copy_motivation": "🏆 Nəticələr və motivasiya",
        "copy_liner": "🚢 Layner baxışı",
        "copy_custom": "✍️ Öz sorğun (mətn)",
        "copy_ask_custom": "Haqqında nə yazmaq istəyirsən? Mövzu, ideya və ya hədəf auditoriya yaz — güclü post hazırlayacağam:",
        "copy_custom_prompt": "Tərəfdaş mövzu üzrə post istəyir: {topic}. inCruises kruiz klubu üçün cəlbedici post yaz. Qısa, emoji ilə. Cavab azərbaycanca.",
        "aud_moms": "Doğuş məzuniyyətində olan analar",
        "aud_entrepreneurs": "Sahibkarlar",
        "aud_students": "Tələbələr/Gənclər",
        "generating_post": "⏳ InLeader post hazırlayır...",
        "post_prompt": "Kruiz klubu üçün auditoriyaya qısa, cəlbedici dəvət postu yaz: {audience}. Cavab azərbaycanca ver.",
        "error_post": "❌ Post hazırlanmadı.",
        "objections_title": (
            "🛡 *Etirazlar bazası*\n\n"
            "Müştərinin etirazını seç — işləmə üçün arqumentlər hazırlayacağam:"
        ),
        "obj_money": "💸 Pulum yoxdur",
        "obj_time": "⏳ Vaxtım yoxdur",
        "obj_pyramid": "🔺 Bu piramidadır",
        "obj_family": "👫 Ailə qarşıdır",
        "obj_invite": "🗣 Dəvət etməyi bilmirəm",
        "obj_seasick": "🌊 Dəniz xəstəliyindən qorxuram",
        "obj_visa": "🛂 Viza məsələsi çətindir",
        "obj_language": "🇬🇧 Dil bilmirəm",
        "obj_custom": "✍️ Öz variant yaz",
        "obj_ask_custom": "Müştərinin etirazını mətnlə yaz — düzgün bağlamağa kömək edəcəyəm:",
        "objection_custom_prompt": "Bu inCruises müştəri etirazını maksimum inandırıcı, aqressiyasız, faktlara əsaslanaraq işlə. Etiraz: {objection}",
        "obj_no_money": "Pulum yoxdur",
        "obj_no_time": "Buna vaxtım yoxdur",
        "generating_objection": "⏳ InLeader arqumentlər hazırlayır...",
        "objection_prompt": (
            "inCruises kruiz klubu müştərisi etiraz bildirdi: «{objection}». "
            "Tərəfdaşın yazışmada asanlıqla işləyə bilməsi üçün 2-3 qısa, nəzakətli və ağır arqument ver. "
            "Formatlaşdırma və siyahılar istifadə et. Cavab azərbaycanca ver."
        ),
        "error_objection": "❌ Cavab hazırlanmadı.",
        "btn_media": "👤 Hesabda iş",
        "btn_account": "👤 Hesabda iş",
        "account_title": "👤 *Hesabda iş*\n\nBölmə seçin:",
        "account_2fa": "🔐 2FA quraşdır",
        "account_2fa_intro": (
            "🔐 *İki faktorlu autentifikasiya (2FA)*\n\n"
            "Addım-addım təlimatı izlə. Hər addımı yerinə yetirdikdən sonra təsdiq düyməsinə bas — "
            "yalnız o zaman növbəti addım açılacaq.\n\nBaşlamağa hazırsan?"
        ),
        "account_2fa_no_file": (
            "📁 2FA təlimat faylı tapılmadı.\n\n"
            "*2FA.pdf* və ya *2FA.txt* faylını `documents/` və ya `documents/2FA/` qovluğuna qoyun. "
            "Addım şəkilləri: `documents/2FA/step1.png`, `step2.png` və s."
        ),
        "account_2fa_congrats": (
            "🎉 *Təbriklər!*\n\n"
            "2FA-nı uğurla quraşdırdın. Hesabın indi etibarlı qorunur! 🔒\n\n"
            "Ehtiyat kodları təhlükəsiz yerdə saxla. Uğurlu işlər! 🚀"
        ),
        "account_policy": "📋 Siyasət",
        "account_policy_no_file": "📁 «Siyasət» faylı tapılmadı. documents/ qovluğuna siyasət.pdf və ya siyasət.txt əlavə edin.",
        "account_policy_thinking": "⏳ InLeader cavab hazırlayır...",
        "account_policy_ask": "Siyasət haqqında istənilən sual ver — cavab verəcəyəm, başa düşməni yoxlayacağam və kömək edəcəyəm.",
        "account_policy_intro_prompt": "Sən inCruises siyasəti üzrə ekspertsən. «Siyasət» faylını tam öyrəndin. Tərəfdaşı qısa salamla. Suallara cavab verməyə, aydınlaşdırıcı suallar verməyə və başa düşmə yoxlaması keçirməyə hazır olduğunu söylə. 2–3 cümlə ilə cavab ver.",
        "account_policy_user_prompt": "Tərəfdaş yazdı: «{question}»\n\nSiyasətə əsasən cavab ver. Lazım gələrsə — aydınlaşdırıcı sual ver və ya başa düşüb-düşməməsini yoxla. Qısa ol. YALNIZ kontekstdən məlumat istifadə et.",
        "account_policy_system": "Sən inCruises siyasəti üzrə təlimçi köməkçisən. Suallara cavab ver, başa düşmə yoxlaması üçün nəzarət sualları ver, tərəfdaşları təlim et. UYDURMA — YALNIZ kontekstdəki faktlardan istifadə et.",
        "account_btn_back_account": "◀ Hesaba qayıt",
        "account_2fa_step_done": "✅ Etdim, növbəti addıma",
        "account_2fa_finish": "✅ Hazırdır! Bitir",
        "account_2fa_start": "🚀 2FA quraşdırmaya başla",
        "btn_marketing": "📊 Marketinq planı",
        "mkt_title": "📊 *Marketinq planı*\n\nLazım olan bölməni seçin:",
        "mkt_ranks": "📊 Marketinq",
        "mkt_rewards": "💰 Mükafatlar",
        "mkt_free_membership": "🎁 Pulsuz üzvlük",
        "mkt_ask_ai": "🤖 Gəlir haqqında sual (AI)",
        "mkt_ranks_text": (
            "🏆 inCruises dərəcələri:\n\n"
            "1. Member → Partner → Senior → Director → President\n"
            "2. Hər dərəcə əlavə liderlik bonusu açır (5%-dən 25%-ə qədər).\n"
            "3. Dərəcə komanda həcminə və şəxsi satışlara bağlıdır.\n\n"
            "💰 Tərəfdaşlıq: $95, hər 6 ayda uzadılır.\n"
            "💎 Classic-ə ilk giriş: $295 (Classic tarifi + tərəfdaşlıq, bir dəfə).\n\n"
            "Dərəcə nə qədər yüksəkdirsə — bütün strukturun dövriyyəsindən bonuslar bir o qədər çox!"
        ),
        "mkt_free_text": (
            "🎁 Pulsuz üzvlük:\n\n"
            "Aylıq töhvən $100 ödənilir, əgər ŞƏRTLƏRDƏN BİRİ yerinə yetirilərsə:\n\n"
            "• 5 nəfər aylıq aktivdir (hər biri öz hesabına $100/ay ödəyir)\n"
            "• 1 Premium tarifində aktivasiya\n"
            "• 3 Classic tarifində qoşulma\n\n"
            "Əslində sən səyahət edirsən və qazanırsan — üzvlük üçün ödəmirsen!"
        ),
        "mkt_ranks_ai_prompt": "inCruises dərəcələri və bonusları haqqında strukturlaşdırılmış danış. Daxil et: dərəcələr (MD, SMD, RD, ND, ID, ED, BOD və yuxarı), Komanda Liderlik bonusu cədvəli, 5 gəlir mənbəyi, 5 mükafat, ödəniş tarixləri. YALNIZ kontekstdən məlumat istifadə et. Cavab azərbaycanca, qısa və rəqəmlərlə.",
        "mkt_free_ai_prompt": "inCruises pulsuz üzvlüyü haqqında ətraflı danış. Daxil et: 3 ixtisas yolu (5 aktiv, 1 PREMIUM, 3 Classic), nə əldə edirsən (200 BP, töhvə silinmir), vacib qaydalar. YALNIZ kontekstdən məlumat istifadə et. Cavab azərbaycanca, strukturlaşdırılmış.",
        "mkt_rewards_ai_prompt": "«Mükafatlar» faylından tam mətnə əsaslanaraq inCruises gəlir və mükafat proqramı haqqında danış: 5 gəlir mənbəyi, 5 mükafat, dərəcələr və KLB, ödəniş tarixləri. Cavabı strukturlaşdır, YALNIZ kontekstdən məlumat istifadə et. Cavab azərbaycanca, rəqəmlərlə.",
        "mkt_ask_prompt": "✏️ Gəlir və ya dərəcələr haqqında sualını yaz.\n\nMəsələn: «5 nəfər qoşsam nə qədər qazanaram?»",
        "mkt_thinking": "⏳ InLeader hesablayır...",
        "mkt_ai_prompt": "inCruises tərəfdaşı marketinq planı haqqında sual verir: {question}. Qısa, dəqiq, rəqəmlərlə cavab ver. Dəqiq hesab üçün məlumat çatışmazsa — nəzakətlə soruş. Rəsmi klub marketinq planına əsaslan. Cavab azərbaycanca ver.",
        "btn_tracker": "🎯 Əməliyyat trekkeri",
        "trk_title": "🎯 Bu gün üçün minimum plan. Ediləni qeyd et:",
        "trk_contacts": "5 yeni əlaqə",
        "trk_followup": "10 toxunma/follow-up",
        "trk_content": "2 stori / 1 post",
        "trk_study": "30 dəq təlim",
        "trk_finish": "🏁 Günü bitir",
        "trk_all_done": "🚀 Sən super-lidersən! Bütün tapşırıqlar tamamlandı! Belə davam et!",
        "trk_all_done_coins": "🎉 Təbriklər! Bu günkü planı tamamladın və +10 InCoins 🪙 qazandın! Davam et!",
        "trk_coins_already": "🚀 Plan tamamlandı! Bu gün üçün ballar artıq verildi, sabah qayıt 😉",
        "trk_partial": "💪 Əla başlanğıc! {done}/{total} tamamlandı. Sabah qalanı bitirəcəyik!",
        "trk_streak_hint": "🔥 Strik: {streak} gün ardıcıl. Proqressi itirməmək üçün bugün trekkeri bağla!",
        "trk_do_all_first": "Əvvəlcə bütün əməliyyatları yerinə yetir!",
        "trk_all_done_already": "Bu gün üçün bütün tapşırıqları artıq tamamladın! 🎉",
        "trk_ask_report": "Əla! Amma sadəcə düyməyə basmaq kifayət deyil. Qısa hesabat yaz: bu gün kimə zəng etdin/yazdın? Hansı etirazlar və ya uğurlar oldu?",
        "trk_restart_sprint": "🔄 Sprinti yenidən başlat",
        "trk_done_today": "✅ Bu gün üçün plan tamamlandı!\n🔥 Strik: {streak} gün. Sabah davam et!",
        "trk_choose_tz": "🌍 Sənə 20:00-da trekker xatırlatması göndərim üçün vaxt zonasını seç:",
        "tz_2": "UTC+2 Avropa",
        "tz_3": "UTC+3 Moskva",
        "tz_4": "UTC+4 Yekaterinburq",
        "tz_5": "UTC+5 Astana/Taşkənd",
        "tz_6": "UTC+6 Almatı/Bişkek",
        "tz_7": "UTC+7 Novosibirsk/Banqkok",
        "tz_8": "UTC+8 İrkutsk/Sinqapur",
        "trk_task_done_already": "✅ Bu tapşırıq bu gün artıq tamamlandı!",
        "trk_report_prompt": "📝 Tapşırıq haqqında hesabat: *{label}*\n\nQısa yaz: nə etdin?",
        "trk_report_too_short": "❌ Hesabat çox qısadır. Ətraflı yaz!",
        "trk_task_accepted": "✅ Tapşırıq qəbul edildi!",
        "trk_sprint_reset": "🔄 Sprint sıfırlandı!",
        "trk_reminder": "⏰ Kapitan! Saat 20:00, jurnalın boşdur! Trekkerə gəl, strik sönəcək!",
        "crm_reminder_header": "🔔 *Xatırlatma (Follow-up):*",
        "paywall_text": (
            "⚠️ <b>Giriş məhdudlaşdırılıb</b>\n\n"
            "Test dövrün və ya InCoins balansın bitdi. "
            "Bot alətləri səni gözləyir, amma onları işə salmaq üçün balansı doldurmalısan.\n\n"
            "💎 <b>Balansı doldur və AI ilə yaratmaya davam et!</b>\n\n"
            "<i>Balans doldurmaq üçün məsləhətçinə və ya administrata müraciət et.</i>"
        ),
        "coin_deducted": "⚡️ Uğurla! 1 sikkə silindi. Qalıq: {coins} 🪙",
        "payment_success": "✅ <b>Ödəniş uğurla tamamlandı!</b>\n\nBalansına <b>{coins} InCoins</b> 🪙 əlavə edildi.\nÖdəniş məbləği: {amount:.2f} ₽",
        "payment_success_cryptopay": "💎 Təbriklər! CryptoPay ilə ödəniş uğurla tamamlandı. Balans dolduruldu.",
        "blocked_msg": "🚫 Bota girişin administrator tərəfindən bloklanıb.",
        "welcome_back": "Qayıtdığın üçün salam, {name}! 👋\n\nBalansında <b>{coins} InCoins</b> 🪙 qaldı.",
        "wallet_text": "💳 <b>Balansınız:</b>\n\nMövcud: <b>{coins} InCoins</b> 🪙\n\n<i>💡 1 İİ yaradılması = 1 InCoin.</i>",
        "test_mode_text": (
            "⚙️ <b>Diqqət: Test rejimi</b>\n\n"
            "InLeader-ə qapalı beta rejimində giriş əldə etdiniz. "
            "İİ funksiyalarını pulsuz test etmək üçün <b>5 InCoins</b> 🪙 verildi.\n\n"
            "📉 <b>Qiymət:</b> 1 yaradılma = 1 InCoin.\n"
            "Sikkələr bitəndə balans doldurulana qədər İİ-ə giriş dayandırılacaq.\n\n"
            "Alətlərimizin gücünü qiymətləndirmək üçün sikkələri ağıllı istifadə edin! 🚢"
        ),
        "name_friend": "dost",
        "balance_screen": "💳 <b>Balansınız</b>\n\nMövcud: <b>{coins} InCoins</b> 🪙\n\n<i>1 İİ yaradılması = 1 InCoin</i>\n\nToplama məbləğini seçin:",
        "balance_topup_text": "💳 <b>{amount} ₽ yükləmə</b>\n\n1 ₽ = 1 InCoin\nÖdənişdən sonra <b>{amount} InCoins</b> alacaqsınız.\n\nÖdənişə keçmək üçün düyməyə basın:",
        "balance_payment_error": "❌ Ödənişlərin quraşdırılmasında xəta. Administrata müraciət edin.",
        "tariff_desc": "InLeader AI alətlərinə giriş üçün InCoins paketi seçin. InCoins kontent yaratmağa, etirazları işləməyə və profil auditinə imkan verir.",
        "tariff_title": "💎 <b>InCoins tarifləri</b>\n\n{desc}\n\nPaket seçin:",
        "tariff_trial": "Proba",
        "tariff_standard": "Standart",
        "tariff_leader": "Lider",
        "tariff_pay_text": "💎 <b>{label}</b> — {coins} InCoins\n\nÖdəniş məbləği: <b>{amount} ₽</b>\n\nÖdənişə keçmək üçün düyməyə basın:",
        "admin_free": "👑 Administrator botdan pulsuz istifadə edir.",
        "tariff_error": "❌ Tarif seçimində xəta.",
        "btn_calc": "🧮 Kalkulyator",
        "calc_title": "🧮 *Kalkulyator*\n\nHesablama növü seç:",
        "calc_tourist_btn": "🏖 Turist kalkulyatoru",
        "calc_cruise_btn": "🚢 Kruiz BB hesabı",
        "calc_conversion_btn": "🔄 BB konvertasiyası (Əlavə ödənişsiz)",
        "calc_conversion_ask": (
            "Kruizun qiymətini və vergi/rüsum məbləğini yaz (bildiksə).\n\n"
            'Məsələn: "Kamu 3500 və rüsum 350" və ya sadəcə "3500" '
            "(onda rüsumu təxminən 10% hesablayacağam)."
        ),
        "calc_conversion_parse_error": "❌ Rəqəmlər çıxarılmadı. Məsələn yaz: «3500» və ya «kamu 3500, rüsum 350».",
        "calc_conversion_receipt": (
            "🧾 KONVERTASİYALI kruiz hesabı (ƏLAVƏ ÖDƏNİŞSİZ):\n\n"
            "💰 Əsas qiymət: ${price}\n"
            "➖ Mövcud ballar (50%): {standard_points} BB\n"
            "🔄 Konvertasiya 2-ə 1: {converted_points} BB\n"
            "⚓️ Təxmini qiymət: {subtotal} BB\n"
            "📑 Vergilər və rüsumlar: ${fees}\n"
            "=======================\n"
            "🔥 Ümumi silinəcək: {final_total} BB (Kartdan sıfır əlavə!)"
        ),
        "calc_bad_number": "⚠️ Müsbət tam ədəd daxil et.",
        "calc_tourist_ask": "🏖 Neçə ay ballar toplamağı planlaşdırırsan?\n\nTöhvə: $100/ay → 200 Reward Points/ay.",
        "calc_tourist_header": "🏖 Ballar toplama cədvəli:",
        "calc_tourist_row": "  Ay {month}: yatırılıb {paid}, ballar {points}",
        "calc_tourist_total": "📊 Ümumi: yatırılıb {total_paid}, toplandı {total_points} RP",
        "calc_tourist_tip": "💡 Ballar kruiz bronlaşdırarkən endirim kimi tətbiq olunur!",
        "calc_cruise_ask_price": (
            "🚢 inCruises-də kruiz qiymətini (USD) daxil et.\n\n"
            "Məsələn: 5845"
        ),
        "calc_cruise_ask_rp": (
            "Əla! İndi yığdığın Bonus Ballarını (BB) daxil et.\n\n"
            "Məsələn: 1200"
        ),
        "calc_cruise_header": "🚢 Kruiz qiyməti hesabı:",
        "calc_cruise_listed": "📋 inCruises siyahı qiyməti:   ${price}",
        "calc_cruise_insider": "🏷 INsider Pricing (−17%):        ${price}   (qənaət ${save})",
        "calc_cruise_rp_avail": "💎 Sənin BB:  {rp} bal = ${value} dəyər",
        "calc_cruise_rp_usable": "✅ Kruizə tətbiq (maks. 50%): {rp} BB = ${value}",
        "calc_cruise_rp_not_enough": "⚠️ BB-n ({rp}) 50%-ə çatmır. Bütün {rp} BB tətbiq edirik.",
        "calc_cruise_cash": "💵 Nağd ödəniş:      ${cash}",
        "calc_cruise_savings": "🎉 Ümumi qənaət:              ${save} (siyahı qiymətdən)",
        "calc_cruise_partner_tip": (
            "💡 Pulsuz üzvlüklü tərəfdaşsansa — töhvələrin bonuslarla ödənilir,\n"
            "   real xərclər daha azdır!\n"
            "🏆 Dərəcəli tərəfdaşlar pulsuz qazandıqları ballarla 100%-ə qədər ödəyə bilər."
        ),
        "calc_cruise_booking_tip": "📅 Bonus ballar kruizə 90+ gün qalmış bronlaşdıranda tətbiq olunur.",
        "calc_image_caption": "🖼 Saxla və ya storiyə göndər!",
        "calc_free_member": "🎁 Pulsuz üzvlük",
        "calc_free_member_text": "Pulsuz üzvlük şərtləri:\n\n1. 5 aktiv klub üzvü\n2. VƏ YA 1 Premium tarifində aktivasiya\n3. VƏ YA 3 Classic tarifində qoşulma\n\nŞərtlərdən biri yerinə yetiriləndə hər ay 200 BB pulsuz alırsan!",
        "sim_title": "🎭 *AI-Satış treyneri*\n\nMəşq üçün müştəri profilini seç:",
        "sim_persona_biz": "💼 Sahibkar (Şübhəli, vaxtı yoxdur)",
        "sim_persona_mom": "👶 Doğuş məzuniyyətində ana (İstirahət istəyir, büdcədən narahat)",
        "sim_persona_tourist": "🏖 Turist (Türkiyəni sevir, kruizləri başa düşmür)",
        "sim_start_status": "⏳ Müştəri chata qoşulur...",
        "sim_stop_btn": "🛑 Bitir və təhlil al",
        "sim_analyzing": "⏳ InLeader dialoqu təhlil edir...",
        "sim_review_prompt": (
            "Bu inCruises satış dialoqunu təhlil et.\n"
            "Tərəfdaşın güclü tərəflərini və səhvlərini göstər.\n"
            "Konkret təkmilləşdirmə məsləhətləri ver.\n"
            "1-dən 10-a qiymət ver.\n"
            "Cavab azərbaycanca ver.\n\nDialoq:\n{dialogue}"
        ),
        "sim_no_messages": "⚠️ Dialoq boşdur — müştəriyə ən azı bir mesaj yaz.",
        "sim_ended": "✅ Məşq tamamlandı! Budur təhlil:",
        "sim_persona_student": "🎓 Tələbə (Hər şeyi dərhal istəyir, dostların rəyindən qorxur)",
        "sim_persona_pensioner": "👵 Pensiyaçı (Səyahət etmək istəyir, aldanmaqdan qorxur)",
        "sim_persona_office": "👔 Ofis işçisi (İstəfa arzulayır, riskdən qorxur)",
        "sim_persona_blogger": "📸 Bloqqer (Kontent lazımdır, «satmaq» istəmir)",
        "sim_persona_entrepreneur": "🏠 Sahibkar (Sistem axtarır, şəbəkəyə inanmır)",
        "sim_persona_skeptic": "🤨 Şübhəli tərəfdaş (Faktlar və qanuniliük tələb edir)",
        "btn_crm": "📅 CRM və Xatırlatmalar",
        "crm_title": "📅 CRM və Xatırlatmalar (Follow-up)\n\nƏməliyyat seç:",
        "crm_add_reminder": "➕ Xatırlatma əlavə et",
        "crm_list_reminders": "📋 Xatırlatmalarım",
        "crm_ask_task": (
            "✏️ Nə haqqında və nə vaxt xatırlatım?\n\n"
            "Məsələn:\n"
            "• «Sabah 14:00-də Annaya pulsuz haqqında yaz»\n"
            "• «2 saatdan sonra İvana zəng et»\n"
            "• «Cümə 10:00-da Katyaya kruiz videosu göndər»"
        ),
        "crm_thinking": "⏳ Tapşırığı təhlil edirəm...",
        "crm_confirmed": "✅ Yaxşı! Sənə xatırladacağam:\n\n📌 {task}\n🕐 {dt}",
        "crm_parse_error": "❌ Tarix/vaxt tanınmadı. Daha dəqiq yaz, məsələn: «Sabah 15:00-də İvana zəng et».",
        "crm_past_date": "❌ Göstərilən vaxt keçib. Gələcək tarix göstər.",
        "crm_no_reminders": "📭 Aktiv xatırlatmalar yoxdur.",
        "crm_list_header": "📋 Aktiv xatırlatmalar:\n",
        "btn_onboarding": "🚀 InCruises yenicə başlayan",
        "ob_tourist": "🏖️ Turist (Klub imtiyazları +)",
        "ob_partner": "💼 Tərəfdaş (Biznes və gəlir)",
        "ob_navigator": "🚀 AI-Navigator: Uğur planım",
        "ob_welcome": "👋 InCruises komandasına xoş gəldin!\n\nSənə şəxsi inkişaf planı hazırlamağım üçün hazırkı məqsədini seç:",
        "ob_ask_goal": (
            "👋 Komandaya xoş gəldin!\n\n"
            "Mənə maksimum faydalı məsləhətlər vermək üçün tanış olaq. "
            "Bir-iki cümlədə yaz: sən daha çox səyahət üçün gəlirsən, "
            "yoxsa güclü biznes qurmaq və passiv gəlir əldə etmək istəyirsən?"
        ),
        "ob_thinking": "⏳ InLeader şəxsi planını hazırlayır...",
        "btn_analyzer": "🧠 Görüş analitiki",
        "btn_mentor": "🧠 AI-Mentor",
        "mentor_title": "🧠 <b>Şəxsi Direktorlar Şuran səndə cavab verir!</b>\n\nBurada boş sözlər yoxdur — yalnız dərin təhlil və strategiyalar. Hansı sahəni inkişaf etdirək? Mütəxəssis seç:",
        "mentor_mindset": "🧠 Mindsət və Düşüncə",
        "mentor_sales": "💰 Satış Sənəti",
        "mentor_coaching": "🎯 Strateji Kouçinq",
        "mentor_management": "👥 Liderlik və Menecment",
        "mentor_psychology": "🧘‍♂️ Təsir Psixologiyası",
        "mentor_mlm": "🌐 MLM və Miqyaslaşdırma",
        "mentor_ask": "Əla seçim. Hazıram. Cari vəziyyətini və ya sualını təsvir et:",
        "analyzer_ask": (
            "🧠 Müştərilə görüş və ya zəngin necə keçdiyini təsvir et.\n\n"
            "Sən nə dedin? Müştəri nə cavab verdi? Dialoq harada tıxandı?\n"
            "Nə qədər ətraflı yazsan, təhlil bir o qədər dəqiq olacaq!"
        ),
        "analyzer_thinking": "⏳ InLeader dialoqu təhlil edir...",
        "btn_leaderboard": "🏆 Komanda reytinqi",
        "lb_header": "📊 Ən aktiv 10 tərəfdaş:\n",
        "lb_empty": "🏆 Reyting hələ boşdur. Əvvəlcə trekkeri tamamla və lider ol! 🚀",
        "btn_documents": "📄 Sənədlər",
        "btn_images": "🎨 AI Şəkillər",
        "doc_title": "📄 *Sənədlər*\n\nBölmə seçin:",
        "doc_cruise_protection": "🛡 Kruiz müdafiəsi",
        "doc_thinking": "⏳ InLeader cavab hazırlayır...",
        "doc_cruise_protection_prompt": "«Kruiz müdafiəsi» faylına əsasən kruiz müdafiəsi haqqında danış: şərtlər, nə daxildir, necə işləyir. YALNIZ kontekstdən məlumat istifadə et. Cavab azərbaycanca.",
    },
    # ── English ──────────────────────────────────────────────
    "en": {
        "choose_lang": "🌍 Choose your language:",
        "lang_stub": "✅ Language saved!",
        "welcome": (
            "Hi! I'm *InLeader* 🚢\n\n"
            "I'll help you craft posts and handle objections.\n"
            "Tap a button below to get started:"
        ),
        "menu_placeholder": "Choose an action",
        "btn_menu": "📋 Menu",
        "menu_reply_hint": "⬇️ Menu button — always at hand",
        "btn_back_menu": "🏠 Back to menu",
        "btn_back": "🔙 Back",
        "btn_balance": "💰 My balance",
        "btn_topup": "💰 Top up",
        "btn_tariffs": "💎 Tariffs",
        "btn_registration": "📝 Registration",
        "btn_referral": "🔗 Referral",
        "btn_continue": "🚀 Continue",
        "btn_pay": "💳 Pay",
        "btn_pay_amount": "💳 Pay {amount}₽",
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
        "account_2fa_step_done": "✅ Done, next step",
        "account_2fa_finish": "✅ Done! Finish",
        "account_2fa_start": "🚀 Start 2FA setup",
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
        "trk_restart_sprint": "🔄 Restart sprint",
        "trk_done_today": "✅ Today's plan done!\n🔥 Your streak: {streak} days. Come back tomorrow to continue!",
        "trk_choose_tz": "🌍 To remind you about the tracker at 8 PM, choose your timezone:",
        "tz_2": "UTC+2 Europe",
        "tz_3": "UTC+3 Moscow",
        "tz_4": "UTC+4 Yekaterinburg",
        "tz_5": "UTC+5 Astana/Tashkent",
        "tz_6": "UTC+6 Almaty/Bishkek",
        "tz_7": "UTC+7 Novosibirsk/Bangkok",
        "tz_8": "UTC+8 Irkutsk/Singapore",
        "trk_task_done_already": "✅ This task is already done today!",
        "trk_report_prompt": "📝 Task report: *{label}*\n\nBriefly describe what you did:",
        "trk_report_too_short": "❌ Report too short. Please elaborate!",
        "trk_task_accepted": "✅ Task accepted!",
        "trk_sprint_reset": "🔄 Sprint reset!",
        "trk_reminder": "⏰ Captain! It's 8 PM and your Journal is empty! Open the Tracker or your streak will burn!",
        "crm_reminder_header": "🔔 *Reminder (Follow-up):*",
        "paywall_text": (
            "⚠️ <b>Access restricted</b>\n\n"
            "Your trial or InCoins balance has run out. "
            "The bot tools are waiting, but you need to top up your balance to use them.\n\n"
            "💎 <b>Top up your balance and keep creating with AI!</b>\n\n"
            "<i>Contact your mentor or admin to top up.</i>"
        ),
        "coin_deducted": "⚡️ Success! 1 coin deducted. Balance: {coins} 🪙",
        "payment_success": "✅ <b>Payment successful!</b>\n\n<b>{coins} InCoins</b> 🪙 added to your balance.\nAmount paid: {amount:.2f} ₽",
        "payment_success_cryptopay": "💎 Congratulations! CryptoPay payment completed successfully. Balance topped up.",
        "blocked_msg": "🚫 Your access to the bot has been blocked by the administrator.",
        "welcome_back": "Welcome back, {name}! 👋\n\nYou have <b>{coins} InCoins</b> 🪙 left on your balance.",
        "wallet_text": "💳 <b>Your wallet:</b>\n\nAvailable: <b>{coins} InCoins</b> 🪙\n\n<i>💡 1 AI generation = 1 InCoin.</i>",
        "test_mode_text": (
            "⚙️ <b>Attention: Test mode</b>\n\n"
            "You have access to InLeader in closed beta. "
            "You received <b>5 InCoins</b> 🪙 for free AI testing.\n\n"
            "📉 <b>Cost:</b> 1 generation = 1 InCoin.\n"
            "When coins run out, AI access will be paused until you top up.\n\n"
            "Use your coins wisely to experience our tools! 🚢"
        ),
        "name_friend": "friend",
        "balance_screen": "💳 <b>Your wallet</b>\n\nAvailable: <b>{coins} InCoins</b> 🪙\n\n<i>1 AI generation = 1 InCoin</i>\n\nChoose top-up amount:",
        "balance_topup_text": "💳 <b>Top up {amount} ₽</b>\n\n1 ₽ = 1 InCoin\nAfter payment you'll receive <b>{amount} InCoins</b>.\n\nTap the button below to pay:",
        "balance_payment_error": "❌ Payment configuration error. Contact the administrator.",
        "tariff_desc": "Choose an InCoins package for access to InLeader AI tools. InCoins enable content generation, objection handling, and profile audits.",
        "tariff_title": "💎 <b>InCoins Tariffs</b>\n\n{desc}\n\nChoose a package:",
        "tariff_trial": "Trial",
        "tariff_standard": "Standard",
        "tariff_leader": "Leader",
        "tariff_pay_text": "💎 <b>{label}</b> — {coins} InCoins\n\nAmount to pay: <b>{amount} ₽</b>\n\nTap the button below to proceed to payment:",
        "admin_free": "👑 Administrator uses the bot for free.",
        "tariff_error": "❌ Tariff selection error.",
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
        "sim_persona_student": "🎓 Student (Wants everything now, fears friends' opinion)",
        "sim_persona_pensioner": "👵 Retiree (Wants to travel, fears being scammed)",
        "sim_persona_office": "👔 Office worker (Dreams of quitting, fears risk)",
        "sim_persona_blogger": "📸 Blogger (Needs content, doesn't want to 'sell')",
        "sim_persona_entrepreneur": "🏠 Entrepreneur (Seeks system, doesn't believe in MLM)",
        "sim_persona_skeptic": "🤨 Skeptic partner (Asks for facts and legality)",
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
        "ob_tourist": "🏖️ Tourist (Club benefits +)",
        "ob_partner": "💼 Partner (Business & income)",
        "ob_navigator": "🚀 AI Navigator: My success plan",
        "ob_welcome": "👋 Welcome to InCruises!\n\nTo prepare your personal development plan, choose your current goal:",
        # analyzer
        "btn_analyzer": "🧠 Meeting Analyzer",
        "mentor_title": "🧠 <b>Your personal Board of Directors is on call!</b>\n\nNo fluff — only deep analysis and strategies. Choose an expert to work with:",
        "mentor_mindset": "🧠 Mindset & Thinking",
        "mentor_sales": "💰 Art of Sales",
        "mentor_coaching": "🎯 Strategic Coaching",
        "mentor_management": "👥 Leadership & Management",
        "mentor_psychology": "🧘‍♂️ Psychology of Influence",
        "mentor_mlm": "🌐 MLM & Scaling",
        "mentor_ask": "Great choice. I'm ready. Describe your situation or ask your question:",
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
        "lang_stub": "✅ Тіл сақталды!",
        "welcome": (
            "Сәлем! Мен *InLeader* 🚢\n\n"
            "Посттар дайындауға және қарсылықтарды өңдеуге көмектесемін.\n"
            "Бастау үшін төмендегі батырманы басыңыз:"
        ),
        "menu_placeholder": "Әрекетті таңдаңыз",
        "menu_choose": "📋 Бөлімді таңдаңыз:",
        "menu_reply_hint": "⬇️ «Меню» батырмасы — әрқашан қолыңда",
        "btn_back_menu": "🏠 Менюге",
        "btn_back": "🔙 Артқа",
        "btn_menu": "📋 Меню",
        "btn_balance": "💰 Менің балансым",
        "btn_topup": "💰 Толықтыру",
        "btn_tariffs": "💎 Тарифтер",
        "btn_registration": "📝 Тіркеу",
        "btn_referral": "🔗 Реферал",
        "btn_continue": "🚀 Жалғастыру",
        "btn_pay": "💳 Төлеу",
        "btn_pay_amount": "💳 {amount}₽ төлеу",
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
        "btn_account": "👤 Тіркелгіде жұмыс",
        "account_title": "👤 *Тіркелгіде жұмыс*\n\nБөлімді таңдаңыз:",
        "account_2fa_step_done": "✅ Орындадым, келесі қадамға",
        "account_2fa_finish": "✅ Дайын! Аяқтау",
        "account_2fa_start": "🚀 2FA орнатуды бастау",
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
        "trk_restart_sprint": "🔄 Спринтті қайта бастау",
        "trk_done_today": "✅ Бүгінгі жоспар орындалды!\n🔥 Стрик: {streak} күн. Ертең жалғастыру үшін қайт!",
        "trk_choose_tz": "🌍 Сені 20:00-да трекер туралы еске салу үшін уақыт белдеуін таңда:",
        "tz_2": "UTC+2 Еуропа",
        "tz_3": "UTC+3 Мәскеу",
        "tz_4": "UTC+4 Екатеринбург",
        "tz_5": "UTC+5 Астана/Ташкент",
        "tz_6": "UTC+6 Алматы/Бишкек",
        "tz_7": "UTC+7 Новосибирск/Бангкок",
        "tz_8": "UTC+8 Иркутск/Сингапур",
        "trk_task_done_already": "✅ Бұл тапсырма бүгін орындалды!",
        "trk_report_prompt": "📝 Тапсырма бойынша есеп: *{label}*\n\nҚысқаша жазыңыз: не істедіңіз?",
        "trk_report_too_short": "❌ Есеп тым қысқа. Толығырақ жазыңыз!",
        "trk_task_accepted": "✅ Тапсырма қабылданды!",
        "trk_sprint_reset": "🔄 Спринт қайта басталды!",
        "trk_reminder": "⏰ Капитан! 20:00, журналың бос! Трекерге кір, стрик өшеді!",
        "crm_reminder_header": "🔔 *Еске салу (Follow-up):*",
        "paywall_text": (
            "⚠️ <b>Қол жеткізу шектелген</b>\n\n"
            "Сынақ кезеңің немесе InCoins балансың таусылды. "
            "Бот құралдары сені күтуде, бірақ оларды қолдану үшін балансыңды толтыру керек.\n\n"
            "💎 <b>Балансыңды толтыр және AI-мен жасауын жалғастыр!</b>\n\n"
            "<i>Балансты толтыру үшін наставникке немесе әкімшіге хабарлас.</i>"
        ),
        "coin_deducted": "⚡️ Сәтті! 1 монета алынды. Қалдық: {coins} 🪙",
        "payment_success": "✅ <b>Төлем сәтті өтті!</b>\n\nБалансыңа <b>{coins} InCoins</b> 🪙 қосылды.\nТөлем сомасы: {amount:.2f} ₽",
        "payment_success_cryptopay": "💎 Құттықтаймыз! CryptoPay төлемі сәтті өтті. Баланс толтырылды.",
        "blocked_msg": "🚫 Ботқа қол жеткізу әкімші тарапынан бұғатталды.",
        "welcome_back": "Қайтқаныңызбен, {name}! 👋\n\nБалансыңда <b>{coins} InCoins</b> 🪙 қалды.",
        "wallet_text": "💳 <b>Әмиян:</b>\n\nҚол жетімді: <b>{coins} InCoins</b> 🪙\n\n<i>💡 1 ИИ генерация = 1 InCoin.</i>",
        "test_mode_text": (
            "⚙️ <b>Назар: Сынақ режимі</b>\n\n"
            "InLeader-ге жабық бета режимінде қол жеткіздіңіз. "
            "ИИ функцияларын тегін тексеру үшін <b>5 InCoins</b> 🪙 берілді.\n\n"
            "📉 <b>Құны:</b> 1 генерация = 1 InCoin.\n"
            "Монеталар біткенше баланс толтырғанша ИИ-ге қол жеткізу тоқтатылады.\n\n"
            "Құралдарымыздың күшін бағалау үшін монеталарды ақылы пайдаланыңыз! 🚢"
        ),
        "name_friend": "дос",
        "balance_screen": "💳 <b>Әмиян</b>\n\nҚол жетімді: <b>{coins} InCoins</b> 🪙\n\n<i>1 ИИ генерация = 1 InCoin</i>\n\nТолықтыру сомасын таңдаңыз:",
        "balance_topup_text": "💳 <b>{amount} ₽ толықтыру</b>\n\n1 ₽ = 1 InCoin\nТөлемнен кейін <b>{amount} InCoins</b> аласыз.\n\nТөлемге өту үшін батырманы басыңыз:",
        "balance_payment_error": "❌ Төлемді баптау қатесі. Әкімшіге хабарласыңыз.",
        "tariff_desc": "InLeader AI құралдарына қол жеткізу үшін InCoins пакетін таңдаңыз. InCoins контент жасауға, қарсылықтарды өңдеуге және профильді аудит жасауға мүмкіндік береді.",
        "tariff_title": "💎 <b>InCoins тарифтері</b>\n\n{desc}\n\nПакетті таңдаңыз:",
        "tariff_trial": "Сынақ",
        "tariff_standard": "Стандарт",
        "tariff_leader": "Лидер",
        "tariff_pay_text": "💎 <b>{label}</b> — {coins} InCoins\n\nТөлем сомасы: <b>{amount} ₽</b>\n\nТөлемге өту үшін батырманы басыңыз:",
        "admin_free": "👑 Әкімші ботты тегін пайдаланады.",
        "tariff_error": "❌ Тариф таңдау қатесі.",
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
        "sim_persona_student": "🎓 Студент (Барлығын бірден қалайды, достардың пікірінен қорқады)",
        "sim_persona_pensioner": "👵 Зейнеткер (Саяхаттағанды қалайды, алдаудан қорқады)",
        "sim_persona_office": "👔 Кеңсе қызметкері (Босатуды армандайды, тәуекелден қорқады)",
        "sim_persona_blogger": "📸 Блогер (Контент керек, «сатуды» қаламайды)",
        "sim_persona_entrepreneur": "🏠 Кәсіпкер (Жүйе іздейді, желіге сенбейді)",
        "sim_persona_skeptic": "🤨 Скептик серіктес (Фактілер мен заңдылық сұрайды)",
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
        "ob_tourist": "🏖️ Турист (Клуб артықшылықтары +)",
        "ob_partner": "💼 Серіктес (Бизнес және табыс)",
        "ob_navigator": "🚀 AI-Навигатор: Менің табыс жоспарым",
        "ob_welcome": "👋 InCruises командасына қош келдің!\n\nСенің жеке даму жоспарыңды дайындау үшін қазіргі мақсатыңды таңда:",
        # analyzer
        "btn_analyzer": "🧠 Кездесу талдаушы",
        "mentor_title": "🧠 <b>Жеке Директорлар Кеңесің сенімен!</b>\n\nМұнда сусыз — тек терең талдау мен стратегиялар. Қай саланы дамытайық? Маман таңда:",
        "mentor_mindset": "🧠 Майндсет және Ойлау",
        "mentor_sales": "💰 Сату Өнері",
        "mentor_coaching": "🎯 Стратегиялық Коучинг",
        "mentor_management": "👥 Көшбасшылық және Менеджмент",
        "mentor_psychology": "🧘‍♂️ Әсер Психологиясы",
        "mentor_mlm": "🌐 MLM және Масштабтау",
        "mentor_ask": "Тамаша таңдау. Дайынмын. Қазіргі жағдайыңды немесе сұрағыңды сипатта:",
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
