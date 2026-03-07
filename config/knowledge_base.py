"""
Facts from official inCruises documents.
Used to ground AI answers and power the calculators.

Sources:
  341RU_NOBODY_CRUISES_BETTER.pdf  (May 2025 edition)
  101RU_SIMPLE_COMPANY_PRESENTATION.pptx
  214RU_RUKOVODSTVO_PO_DOHODAM_I_VOZNAGRAGHDENIYAM.pdf (May 14, 2025)
  103EN_CORPORATE_DUE_DILIGENCE.pdf (December 27, 2024)
  documents/marketing/Rank.pdf или Rank.txt — ранги (если есть)
"""

from pathlib import Path

# Жёсткий лимит текста из файлов для экономии контекста ИИ (~10–15 страниц)
MAX_DOCUMENT_CHARS = 30000


def _load_file_from_paths(bases: list[Path], names: tuple[str, ...]) -> str:
    """Загружает текст из первого найденного файла. Поддерживает .txt, .md, .pdf, .fb2."""
    for base in bases:
        for name in names:
            path = base / name
            if not path.exists():
                continue
            try:
                content = ""
                if name.endswith(".pdf"):
                    from pypdf import PdfReader
                    reader = PdfReader(path)
                    content = "\n".join((p.extract_text() or "") for p in reader.pages).strip()
                elif name.endswith(".fb2"):
                    import re
                    raw = path.read_text(encoding="utf-8", errors="replace")
                    paras = re.findall(r"<p>(.*?)</p>", raw, flags=re.DOTALL)
                    content = "\n".join(paras).strip()
                else:
                    content = path.read_text(encoding="utf-8", errors="replace").strip()
                if len(content) > MAX_DOCUMENT_CHARS:
                    content = content[:MAX_DOCUMENT_CHARS] + "... [текст обрезан для экономии контекста]"
                return content
            except Exception:
                pass
    return ""


def get_mlm_library_facts() -> str:
    """
    Автоматически сканирует папку documents и загружает контент из всех текстовых файлов
    (pdf, fb2, txt, md), чтобы ИИ всегда имел актуальные обучающие материалы.
    """
    docs_dir = Path(__file__).resolve().parent.parent / "documents"
    if not docs_dir.exists():
        return ""

    # Список файлов, которые мы уже обрабатываем отдельно (чтобы не дублировать)
    ignored_files = {
        "2FA.pdf", "2fa.pdf", "2FA.txt", "2fa.txt",
        "политика.pdf", "политика.txt",
        "защита круиза.pdf", "защита круиза.txt",
        "вознаграждения.pdf", "вознаграждения.txt"
    }

    content = []
    total_chars = 0
    # Берём только первые файлы до достижения лимита (один файл на запрос по сути)
    for ext in ("*.pdf", "*.fb2", "*.txt", "*.md"):
        for path in docs_dir.rglob(ext):
            if path.name in ignored_files:
                continue
            if total_chars >= MAX_DOCUMENT_CHARS:
                break
            text = _load_file_from_paths([path.parent], (path.name,))
            if text:
                chunk = f"--- ДОКУМЕНТ: {path.name} ---\n{text}"
                remain = MAX_DOCUMENT_CHARS - total_chars - len(chunk)
                if remain < 0:
                    chunk = chunk[:MAX_DOCUMENT_CHARS - total_chars] + "... [текст обрезан для экономии контекста]"
                content.append(chunk)
                total_chars += len(chunk)
        if total_chars >= MAX_DOCUMENT_CHARS:
            break

    if not content:
        return ""
    document_text = "\n\n".join(content)
    if len(document_text) > MAX_DOCUMENT_CHARS:
        document_text = document_text[:MAX_DOCUMENT_CHARS] + "... [текст обрезан для экономии контекста]"
    return (
        "\n\n=== АКТУАЛЬНАЯ БАЗА ЗНАНИЙ И ОБУЧАЮЩИЕ МАТЕРИАЛЫ ===\n"
        "Используй эти данные для профессионального анализа и ответов в контексте запроса клиента.\n\n"
        + document_text
        + "\n\n========================================================\n"
    )


def _load_rank_file() -> str:
    """Загружает текст из documents/marketing/Rank.*"""
    docs = Path(__file__).resolve().parent.parent / "documents"
    return _load_file_from_paths(
        [docs / "marketing"],
        ("Rank.txt", "Rank.md", "Rank.pdf"),
    )


def _load_2fa_file() -> str:
    """Загружает текст из documents/2FA.pdf или documents/2FA.txt"""
    docs = Path(__file__).resolve().parent.parent / "documents"
    return _load_file_from_paths(
        [docs / "2FA", docs],
        ("2FA.pdf", "2FA.txt", "2fa.pdf", "2fa.txt"),
    )


def _parse_2fa_into_steps(raw: str) -> list[dict]:
    """Парсит текст в список шагов по маркерам «Шаг N:» и т.п."""
    import re
    docs = Path(__file__).resolve().parent.parent / "documents"
    fa_dir = docs / "2FA"
    steps = []
    parts = re.split(r"\n\s*(?=(?:шаг|step)\s*\d+[:\.])", raw, flags=re.IGNORECASE)
    if len(parts) <= 1:
        parts = re.split(r"\n-{3,}\n", raw)
    if len(parts) <= 1:
        parts = re.split(r"\n\s{2,}\n", raw)
    if len(parts) <= 1:
        parts = [raw]
    for p in parts:
        p = re.sub(r"^(?:шаг|step)\s*\d+[:\.\s]*", "", p, flags=re.IGNORECASE).strip()
        if not p or len(p) < 15:
            continue
        step_num = len(steps) + 1
        img_path = None
        for ext in (".png", ".jpg", ".jpeg"):
            candidate = fa_dir / f"step{step_num}{ext}"
            if candidate.exists():
                img_path = str(candidate)
                break
        steps.append({"title": f"Шаг {step_num}", "text": p[:3500], "image_path": img_path})
    return steps


def get_2fa_steps_and_facts() -> tuple[list[dict], str]:
    """
    Загружает 2FA-файл, парсит в шаги. Lama использует этот контент.
    Возвращает (steps, raw_text).
    """
    raw = _load_2fa_file()
    steps = _parse_2fa_into_steps(raw) if raw else []
    return steps, raw


def _load_cruise_protection_file() -> str:
    """Загружает текст из documents/защита круиза.pdf или защита круиза.txt"""
    docs = Path(__file__).resolve().parent.parent / "documents"
    return _load_file_from_paths(
        [docs],
        ("защита круиза.pdf", "защита круиза.txt", "cruise_protection.pdf", "cruise_protection.txt"),
    )


def _load_policy_file() -> str:
    """Загружает текст из documents/политика.pdf или политика.txt"""
    docs = Path(__file__).resolve().parent.parent / "documents"
    return _load_file_from_paths(
        [docs],
        ("политика.pdf", "политика.txt", "policy.pdf", "policy.txt"),
    )


def get_policy_facts_for_ai() -> str:
    """
    Текст из файла «Политика» для Lama.
    Используется в разделе Работа в аккаунте → Политика.
    """
    raw = _load_policy_file()
    if raw:
        return (
            "=== ДАННЫЕ ИЗ ФАЙЛА «ПОЛИТИКА» (используй ТОЛЬКО эти факты) ===\n\n"
            + raw
            + "\n\nDO NOT invent. Use ONLY data above."
        )
    return "Файл «Политика» не найден в documents/. Добавьте политика.pdf или политика.txt"


def get_cruise_protection_facts_for_ai() -> str:
    """
    Текст из файла «Защита круиза» для Lama.
    Если файла нет — возвращает подсказку.
    """
    raw = _load_cruise_protection_file()
    if raw:
        return (
            "=== ДАННЫЕ ИЗ ФАЙЛА «ЗАЩИТА КРУИЗА» (используй ТОЛЬКО эти факты) ===\n\n"
            + raw
            + "\n\nDO NOT invent. Use ONLY data above."
        )
    return "Файл «Защита круиза» не найден в documents/. Добавьте защита круиза.pdf или защита круиза.txt"


def _load_rewards_file() -> str:
    """Загружает весь текст из файла вознаграждения (documents/marketing или documents)."""
    docs = Path(__file__).resolve().parent.parent / "documents"
    return _load_file_from_paths(
        [docs / "marketing", docs],
        ("вознаграждения.pdf", "вознаграждения.txt"),
    )


# ── Membership pricing ───────────────────────────────────────────────────────

MONTHLY_CONTRIBUTION_USD = 100        # regular Club Member monthly fee
PARTNERSHIP_FEE_USD = 95              # Partnership fee, renewed every 6 months
CLASSIC_FIRST_ENTRY_USD = 295         # First entry on Classic tariff + partnership (one-time)
REWARD_POINTS_PER_MONTH = 200         # RP earned per $100 monthly contribution
RP_VALUE_USD = 1.0                    # 1 Reward Point = $1.00 toward cruise booking

# ── Cruise discounts (from official document) ────────────────────────────────

INSIDER_DISCOUNT_PCT = 17             # INsider Pricing: -17 % off inCruises listed price
MAX_RP_COVERAGE_PCT = 50              # Bonus Points can cover up to 50% of listed price
                                      # (booking 90+ days in advance required)
ADVANCE_BOOKING_DAYS = 90             # Minimum days ahead for RP-50% discount

# ── Real pricing example (2 pax, illustrative) ───────────────────────────────

EXAMPLE = {
    "direct_price_usd": 6111.57,
    "incruises_listed_usd": 5845.14,
    "insider_price_usd": 4696.32,          # ~19.7% off listed (doc says "≈17%")
    "with_50pct_rp_member_usd": 4393.61,   # $2929.07 RP + $1464.35 cash
    "with_50pct_rp_partner_usd": 2929.07,  # Free Membership covers cash part
    "with_100pct_rp_partner_usd": 0.0,     # Full Free Membership + rank
}

# ── Price Match Guarantee ────────────────────────────────────────────────────

PRICE_MATCH_MIN_DIFF_USD = 100        # Competitor must be $100+ cheaper
PRICE_MATCH_APPROVAL_HOURS = 72       # Team reviews within 72 hours
PRICE_MATCH_BOOKING_DEADLINE_HOURS = 72  # Must book within 72h after approval

# ── Quick-reference text (used in AI system prompt) ──────────────────────────

FACTS_FOR_AI = """
=== OFFICIAL inCruises PRICING FACTS (use ONLY these numbers) ===

⚠️ ЗАПРЕЩЕНО упоминать любые круизные линии (Royal Caribbean и др.). Работаем ТОЛЬКО с inCruises.

MEMBERSHIP:
- Regular Club Member: $100/month → earns 200 Reward Points/month
- Partnership: $95 fee, пролонгация каждые 6 месяцев
- Classic first entry: $295 — первый вход на тариф Classic + партнёрство (разово)
- 1 Reward Point (RP) = $1.00 value when applied to cruise booking

CRUISE DISCOUNTS (for Active Club Members):
- INsider Pricing: instant -17% off the inCruises listed price (select cruises)
- Bonus Points / RP: can cover UP TO 50% of the listed cruise price
  (requires booking 90+ days in advance)
- Partners with rank + Free Membership: can potentially cover 100% with RP

FREE MEMBERSHIP PROGRAM (безоплатное членство):
Требуется выполнить ОДНО из условий:
- 5 человек ежемесячно активны (каждый платит $100/мес по своим счетам), ИЛИ
- 2 подключения на премиум-тариф, ИЛИ
- 3 подключения на тариф Classic

PRICE MATCH GUARANTEE:
- If a competitor offers the SAME cruise for $100+ USD less, inCruises
  will match that price AND still allow Bonus Points usage
- Applies only when booking WITH Bonus Points
- Request via inCruises.com/cruises (step 6 of booking)
- Approval within 72 hours; must complete booking within 72h of approval

REAL EXAMPLE (2 pax, illustrative):
- Direct price:                      $6,111.57
- inCruises listed price:            $5,845.14  (save $253)
- With INsider Pricing (-17%):       $4,696.32
- With 50% RP (member pays cash):    $4,393.61
- With 50% RP (partner Free Memb.):  $2,929.07
- With 100% RP (partner + rank):     $0 (full cruise FREE)

DO NOT invent numbers. DO NOT mention Royal Caribbean or other cruise lines.
=================================================================================
"""

# ── Compensation & Rewards (from 214RU, May 2025) ─────────────────────────────
# Used by Marketing AI for questions about income, bonuses, ranks.

REWARDS_FACTS_FOR_AI = """
=== РУКОВОДСТВО ПО ДОХОДАМ И ВОЗНАГРАЖДЕНИЯМ (use ONLY these facts) ===

ТРЕБОВАНИЯ ДЛЯ ЗАРАБОТКА: Партнёры каждые 6 мес. оплачивают $95 за продление. MD и выше — минимальные прямые активации: $200/30д, $600/90д, $1200/180д, $2400/365д (Board of Directors освобождены).

5 ИСТОЧНИКОВ ДОХОДА:

1. БОНУСЫ ЗА АКТИВАЦИЮ:
   - Ежедневный (DAB): STARTER/CLASSIC $20, PREMIUM $50 — в течение 24ч после активации.
   - Ежемесячный (MAB): при 3+ активациях в месяц. CLASSIC 3-4: $20, 5-9: $30, 10+: $40; PREMIUM 3-4: $50, 5-9: $75, 10+: $100. Выплата 8-го числа.

2. ЕЖЕНЕДЕЛЬНЫЙ МАТЧИНГ-БОНУС: Личный объём $200+ и командный $600+ за неделю = 100% матчинг DAB+MAB прямых Партнёров. Выплата в понедельник (неделя Пн 00:00 — Вс 23:59 UTC).

3. КОМАНДНЫЙ ЛИДЕРСКИЙ БОНУС (КЛБ): Квалиф. объём продаж + Общий объём активаций. Правило 40% (макс. % с ветки). MD: $3000/$600; SMD: $10000/$2000; RD: $25000/$5000; ND: $50000/$10000; ID: $100000/$20000; ED: $250000/$50000; BOD: $550000/$110000; Amb BOD: $750000/$300000; Prem Amb BOD: $750000/$1M; Glob Amb BOD: $1M/$400000; Roy Amb BOD: $1M/$2M. Выплата 10-го. MD без $600 активаций — ранг есть, КЛБ нет. SMD+ без $600 — ранг MD, КЛБ нет. SMD+ с $600+ но без полного Объёма — 50% КЛБ.

4. РЕКУРРЕНТНЫЙ ДОХОД: min $5 за каждые $100 Квалиф. рекуррентного объёма. Правило 40%, пороги КРО. Мультипликатор: $0-8999→$5; $9000-15999→$6; $16000-22999→$7; $23000-29999→$8; $30000→$9; Суперфундамент→$10. BOD с ФБ $5850+ — мин. $55000/мес. Выплата 15-го. Бесплатное членство НЕ учитывается в Рекурренте.

5. БОНУС ФУНДАМЕНТ БИЗНЕСА: MD+ от объёма ФБ и ИКБ. $5k-9999→5%; $10k-29999→10%; $30k+→30%. ИКБ ≥65% — 100% бонуса; <65% — % ИКБ от бонуса. Выплата 15-го. Суперфундамент: при $100k ФБ + 1 команда Int.Dir. — доп. 5% от ФБ, ED+ также 5% от команд Int.Dir.

5 ВОЗНАГРАЖДЕНИЙ:
- Бесплатное членство: $500 прямых продаж/мес → 200 RP, взнос $100 не списывается. 5 активных × $100.
- Быстрый старт: MD в 1-й полный месяц → $500 вместо $300. Спонсор получает $500 матчинг при удержании МД.
- Элитные туристические преимущества: 3 КЛБ (МД+) → 100% круиза BP. ND+ — неограниченные брони BP.
- Соревнования за BP: еженедельно топ-25 ($400+ прямой объём); ежемесячно топ-25 по рангам ($1000+ командный, $400+ прямой). 20-500 BP.
- Международный Лидерский Саммит: конкурсы, призы — проживание и т.д.

ВЫПЛАТЫ: DAB — 24ч; MAB — 8-е; Матчинг — понедельник; КЛБ — 10-е; Рекуррент — 15-е; ФБ/СуперфБ — 15-е. Если дата выходная — ближайший рабочий день.

DO NOT invent numbers. Use ONLY official data above.
=================================================================================
"""

# ── Free Membership (from 214RU, вознаграждения.pdf) ─────────────────────────
# Used by Marketing AI for the "Безоплатное членство" button.

FREE_MEMBERSHIP_FACTS_FOR_AI = """
=== БЕСПЛАТНОЕ ЧЛЕНСТВО — официальные данные (use ONLY these facts) ===

УСЛОВИЯ КВАЛИФИКАЦИИ (выполнить ОДНО):
- 5 прямых Активных Членов Клуба (каждый платит $100/мес по своим счетам) = $500 прямых продаж в месяц, ИЛИ
- 1 подключение на тариф PREMIUM, ИЛИ
- 3 подключения на тариф Classic

ЧТО ПОЛУЧАЕШЬ: Активный Член-Партнёр с $500+ прямых активаций в месяц — не платит $100 ежемесячного взноса. inCruises начисляет 200 Бонусных Баллов, не списывая взнос. Только Партнёр (без членства) при квалификации — получает 200 BP.

ВАЖНЫЕ ПРАВИЛА:
- Прямые Члены-Партнёры с бесплатным членством НЕ учитываются в твоих $500 прямых продаж. Они также не учитываются в Квалифицированном объёме продаж и Общем объёме продаж (КЛБ, ранги).
- Счёт БЕСПЛАТНЫЙ только если на момент выставления счёта у тебя есть $500 в объёме прямых продаж.
- Если на момент создания счёта нет $500 — счёт НЕ бесплатный, нужно оплатить. Без рекуррентных платежей аккаунт → «Ожидание».
- Если счёт помечен «БЕСПЛАТНЫЙ», но кто-то из твоих активных Членов запрашивает возврат/отмену и объём падает ниже $500 — ты теряешь статус бесплатного. 200 BP списываются, приходит счёт $100.
- Только Партнёр: 15-го числа должен соответствовать требованиям для вознаграждения «Бесплатное членство».
- Партнёры в рангах МД и выше могут квалифицироваться на бесплатное членство, даже если не выполняют Требование к минимальному количеству Активаций.

ПЛАНЫ STARTER и PREMIUM:
- STARTER с бесплатным членством: отмена $50/мес, зачисление 50 BP.
- PREMIUM с бесплатным: отмена $100 из $250/мес, зачисление 200 BP; остаётся оплатить $150 разницу.

DO NOT invent numbers. Use ONLY official data above.
=================================================================================
"""


def get_rewards_file_facts_for_ai() -> str:
    """
    Полный текст из файла вознаграждения для кнопки «Вознаграждения».
    Ищет вознаграждения.pdf / вознаграждения.txt в documents/marketing и documents/.
    """
    raw = _load_rewards_file()
    if raw:
        return (
            "=== ДАННЫЕ ИЗ ФАЙЛА ВОЗНАГРАЖДЕНИЯ (используй ТОЛЬКО эти факты) ===\n\n"
            + raw
            + "\n\nDO NOT invent numbers. Use ONLY data above."
        )
    return REWARDS_FACTS_FOR_AI


def get_rank_facts_for_ai() -> str:
    """
    Факты о рангах для Lama в разделе Маркетинг.
    Если есть documents/marketing/Rank.pdf или Rank.txt — использует его.
    Иначе — REWARDS_FACTS_FOR_AI.
    """
    raw = _load_rank_file()
    if raw:
        return (
            "=== ДАННЫЕ ИЗ ФАЙЛА Rank (documents/marketing) — используй ТОЛЬКО эти факты ===\n\n"
            + raw
            + "\n\nDO NOT invent numbers. Use ONLY data above."
        )
    return REWARDS_FACTS_FOR_AI


# ── Corporate Due Diligence (from 103EN, December 2024) ────────────────────────
# Used by Marketing AI for questions about company, leadership, compliance, legality.

CORPORATE_FACTS_FOR_AI = """
=== CORPORATE DUE DILIGENCE — inCruises (use ONLY these facts) ===

КОМПАНИЯ: inCruises — эксклюзивный Travel Membership Club, 190+ стран. «Total game changer» для планирования и оплаты отпусков. Прямые продажи через Direct to Consumer - Referral Marketing.

РУКОВОДСТВО: Michael Hutchison (CEO), Anthony Varvaro (COO/CFO), Kenneth Hernandez (CTO), Jovanska Taveras (Legal), Doug Corrigan (CMO), Jessica Camacho (HR), Dr. Kees-Jan de Maa (Media), Laz Vitos (Support), Jonathan Iñesta (Product), Hector Ortíz (Financial Controller), Mario Rodriguez (Operations), Nanette Evans (Compliance).

ЮРИДИЧЕСКИЙ СТАТУС: LLC Delaware с 24.08.2015 (ID #5809499). Штаб-квартира в Пуэрто-Рико. Seller of Travel: California 2146142-50, Florida ST-42861, Washington 604-762-223. Dun & Bradstreet DUNS #08-008-2396. CLIA #00027506.

ФИНАНСЫ: Без долгов, положительный cash flow. Нет коммерческих судебных разбирательств в истории руководства. 14-дневная гарантия возврата денег на все покупки.

ПРОДУКТ: 21,000+ глобальных круизных маршрутов. Более 35 млн человек будут круизовать к 2025. Партнёрам: обучение, маркетинг-инструменты, менторство, инновационный компенсационный план, бесплатные поездки.

БЛАГОТВОРИТЕЛЬНОСТЬ: $1M+ помощь Украине (с 2021), $1M+ Mercy Ships (с марта 2022).

⚠️ ЗАПРЕЩЕНО упоминать круизные линии (Royal Caribbean и др.). Работаем только с inCruises.
=================================================================================
"""
