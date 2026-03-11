"""
Lightweight SQLite storage for gamification (scores & leaderboard).
The DB file lives next to bot.py as ``inleader.db``.
"""

import logging
import sqlite3
from datetime import date
from pathlib import Path

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).resolve().parent.parent / "inleader.db"

_conn: sqlite3.Connection | None = None


def _get_conn() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(str(DB_PATH))
        _conn.row_factory = sqlite3.Row
    return _conn


def init_db() -> None:
    conn = _get_conn()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id            INTEGER PRIMARY KEY,
            username           TEXT,
            full_name          TEXT,
            score              INTEGER DEFAULT 0,
            last_tracker_date  TEXT,
            streak             INTEGER DEFAULT 0,
            incoins            INTEGER DEFAULT 0,
            timezone           INTEGER,
            daily_progress     TEXT DEFAULT '0,0,0,0',
            is_authorized      INTEGER DEFAULT 0,
            is_blocked         INTEGER DEFAULT 0
        )
        """
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)"
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS payment_orders (
            order_id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            amount_rub REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS crm_reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            run_at TEXT NOT NULL,
            task_text TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS usage_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task_type TEXT NOT NULL,
            model TEXT NOT NULL,
            cost REAL,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    for col in ("streak", "incoins", "daily_progress", "full_name", "is_authorized", "is_blocked"):
        try:
            if col == "full_name":
                conn.execute("ALTER TABLE users ADD COLUMN full_name TEXT")
            elif col == "is_authorized":
                conn.execute("ALTER TABLE users ADD COLUMN is_authorized INTEGER DEFAULT 0")
            elif col == "is_blocked":
                conn.execute("ALTER TABLE users ADD COLUMN is_blocked INTEGER DEFAULT 0")
            else:
                default_val = "'0,0,0,0'" if col == "daily_progress" else "0"
                conn.execute(
                    f"ALTER TABLE users ADD COLUMN {col} INTEGER DEFAULT {default_val}" if col != "daily_progress" 
                    else f"ALTER TABLE users ADD COLUMN {col} TEXT DEFAULT {default_val}"
                )
            conn.commit()
        except sqlite3.OperationalError:
            pass
    try:
        conn.execute("ALTER TABLE users ADD COLUMN timezone INTEGER")
        conn.commit()
    except sqlite3.OperationalError:
        pass
    try:
        conn.execute("ALTER TABLE payment_orders ADD COLUMN amount_coins INTEGER")
        conn.commit()
    except sqlite3.OperationalError:
        pass
    conn.commit()
    logger.info("DB initialised: %s", DB_PATH)


def add_user(user_id: int, username: str | None, full_name: str | None = None) -> bool:
    """
    Пытается добавить пользователя в базу данных.
    Если пользователь уже существует, обновляет его данные и возвращает False.
    Если это абсолютно новый пользователь, начисляет ему 50 стартовых InCoins и возвращает True.
    """
    conn = _get_conn()
    
    # Проверяем, существует ли пользователь
    row = conn.execute(
        "SELECT user_id FROM users WHERE user_id = ?", (user_id,)
    ).fetchone()
    
    if row:
        # Обновляем существующего
        conn.execute(
            "UPDATE users SET username = ?, full_name = COALESCE(?, full_name) WHERE user_id = ?",
            (username, full_name, user_id)
        )
        conn.commit()
        return False
    else:
        # Создаем нового с 5 монетами (тестовый режим)
        conn.execute(
            "INSERT INTO users (user_id, username, full_name, incoins) VALUES (?, ?, ?, ?)",
            (user_id, username, full_name, 5)
        )
        conn.commit()
        return True


def add_user_coins_admin(user_id: int, amount: int) -> None:
    """Изменяет баланс InCoins пользователя (UPDATE users SET incoins = incoins + ?)."""
    conn = _get_conn()
    conn.execute(
        "UPDATE users SET incoins = COALESCE(incoins, 0) + ? WHERE user_id = ?",
        (amount, user_id)
    )
    conn.commit()


def get_user_coins(user_id: int) -> int:
    """Возвращает текущий баланс монет пользователя."""
    conn = _get_conn()
    row = conn.execute(
        "SELECT COALESCE(incoins, 0) as incoins FROM users WHERE user_id = ?", (user_id,)
    ).fetchone()
    return row["incoins"] if row else 0


def give_all_coins_admin(amount: int) -> int:
    """Начисляет монеты всем пользователям в базе. Возвращает количество затронутых строк."""
    conn = _get_conn()
    cursor = conn.execute("UPDATE users SET incoins = COALESCE(incoins, 0) + ?", (amount,))
    conn.commit()
    return cursor.rowcount


def spend_incoins(user_id: int, amount: int = 1) -> bool:
    """
    Пытается списать монеты за использование ИИ.
    Если баланса хватает — списывает и возвращает True.
    Если нет — возвращает False.
    Администратор (5925660014) пользуется бесплатно.
    """
    if user_id == 5925660014:  # ADMIN_ID
        return True

    conn = _get_conn()
    row = conn.execute(
        "SELECT COALESCE(incoins, 0) as incoins FROM users WHERE user_id = ?",
        (user_id,),
    ).fetchone()

    if not row or row["incoins"] < amount:
        return False

    conn.execute(
        "UPDATE users SET incoins = incoins - ? WHERE user_id = ?",
        (amount, user_id),
    )
    conn.commit()
    return True


def find_user_by_id_or_username(identifier: str) -> dict | None:
    """Ищет пользователя по ID или @username."""
    conn = _get_conn()
    identifier = identifier.strip()
    
    if identifier.startswith("@"):
        username = identifier.removeprefix("@")
        row = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
    elif identifier.isdigit():
        row = conn.execute(
            "SELECT * FROM users WHERE user_id = ?", (int(identifier),)
        ).fetchone()
    else:
        # Поиск по юзернейму без @
        row = conn.execute(
            "SELECT * FROM users WHERE username = ?", (identifier,)
        ).fetchone()
        
    return dict(row) if row else None


def upsert_user(user_id: int, username: str | None, full_name: str | None = None) -> None:
    """Для обратной совместимости: просто вызывает add_user."""
    add_user(user_id, username, full_name)


def add_score(user_id: int, points: int) -> bool:
    """
    Award *points* and stamp today's date.
    Returns True if points were actually awarded (first time today),
    False if the user already got points today.
    """
    conn = _get_conn()
    row = conn.execute(
        "SELECT last_tracker_date FROM users WHERE user_id = ?",
        (user_id,),
    ).fetchone()

    today = date.today().isoformat()

    if row and row["last_tracker_date"] == today:
        return False

    if row is None:
        conn.execute(
            "INSERT INTO users (user_id, score, last_tracker_date) VALUES (?, ?, ?)",
            (user_id, points, today),
        )
    else:
        conn.execute(
            "UPDATE users SET score = score + ?, last_tracker_date = ? WHERE user_id = ?",
            (points, today, user_id),
        )
    conn.commit()
    return True


def add_score_admin(user_id: int, points: int) -> None:
    """Изменяет общее количество очков (score) пользователя. Может быть отрицательным."""
    conn = _get_conn()
    conn.execute(
        "UPDATE users SET score = COALESCE(score, 0) + ? WHERE user_id = ?",
        (points, user_id)
    )
    conn.commit()


def get_timezone(user_id: int) -> int | None:
    """Возвращает timezone пользователя (смещение в часах) или None."""
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT timezone FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
    except sqlite3.OperationalError:
        return None
    if row is None:
        return None
    val = row["timezone"]
    return val if val is not None else None


def set_timezone(user_id: int, tz_offset: int) -> None:
    """Устанавливает timezone (смещение в часах, например 3 для UTC+3)."""
    conn = _get_conn()
    upsert_user(user_id, None)
    conn.execute(
        "UPDATE users SET timezone = ? WHERE user_id = ?", (tz_offset, user_id)
    )
    conn.commit()


def get_users_for_tracker_reminder(utc_hour: int) -> list[int]:
    """
    Возвращает user_id пользователей, у которых сейчас 20:00 по их локальному времени
    и last_tracker_date != сегодня. (utc_hour + timezone) % 24 == 20
    """
    today = date.today().isoformat()
    conn = _get_conn()
    try:
        rows = conn.execute(
            """
            SELECT user_id, timezone FROM users
            WHERE timezone IS NOT NULL
            AND (last_tracker_date IS NULL OR last_tracker_date != ?)
            """,
            (today,),
        ).fetchall()
    except sqlite3.OperationalError:
        return []
    return [
        r["user_id"]
        for r in rows
        if r["timezone"] is not None
        and (utc_hour + r["timezone"]) % 24 == 20
    ]


def get_tracker_data(user_id: int) -> dict:
    """Возвращает streak, last_tracker_date, incoins, daily_progress для конкретного пользователя."""
    conn = _get_conn()
    row = conn.execute(
        "SELECT last_tracker_date, COALESCE(streak, 0) as streak, COALESCE(incoins, 0) as incoins, COALESCE(daily_progress, '0,0,0,0') as daily_progress FROM users WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    
    if row is None:
        # Если пользователя нет, создаем его
        upsert_user(user_id, None)
        return {"streak": 0, "last_tracker_date": None, "incoins": 0, "daily_progress": "0,0,0,0"}
        
    return {
        "streak": row["streak"],
        "last_tracker_date": row["last_tracker_date"],
        "incoins": row["incoins"],
        "daily_progress": row["daily_progress"],
    }


def update_daily_progress(user_id: int, progress: str) -> None:
    """Обновляет строку прогресса для конкретного пользователя."""
    conn = _get_conn()
    conn.execute(
        "UPDATE users SET daily_progress = ? WHERE user_id = ?",
        (progress, user_id),
    )
    conn.commit()


def reset_tracker_sprint(user_id: int) -> None:
    """Обнуляет стрик и прогресс конкретного юзера."""
    conn = _get_conn()
    conn.execute(
        "UPDATE users SET streak = 0, daily_progress = '0,0,0,0' WHERE user_id = ?",
        (user_id,),
    )
    conn.commit()


def close_tracker_day(user_id: int) -> dict:
    """
    Закрывает день для конкретного юзера: обновляет дату, стрик и начисляет монеты.
    Возвращает {'awarded': bool, 'new_streak': int}.
    """
    from datetime import date, timedelta
    today = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    conn = _get_conn()
    row = conn.execute(
        "SELECT last_tracker_date, COALESCE(streak, 0) as streak FROM users WHERE user_id = ?",
        (user_id,),
    ).fetchone()

    if row and row["last_tracker_date"] == today:
        return {"awarded": False, "new_streak": row["streak"]}

    # Расчёт нового стрика
    if row and row["last_tracker_date"] == yesterday:
        new_streak = row["streak"] + 1
    else:
        new_streak = 1

    conn.execute(
        """
        UPDATE users
        SET last_tracker_date = ?,
            streak = ?,
            incoins = COALESCE(incoins, 0) + 10,
            daily_progress = '0,0,0,0'
        WHERE user_id = ?
        """,
        (today, new_streak, user_id),
    )
    conn.commit()
    return {"awarded": True, "new_streak": new_streak}


def get_users_without_tracker_today() -> list[int]:
    """Возвращает user_id всех, у кого last_tracker_date != сегодня."""
    today = date.today().isoformat()
    conn = _get_conn()
    rows = conn.execute(
        "SELECT user_id FROM users WHERE last_tracker_date IS NULL OR last_tracker_date != ?",
        (today,),
    ).fetchall()
    return [r["user_id"] for r in rows]


def get_top_users(limit: int = 10) -> list[dict]:
    conn = _get_conn()
    rows = conn.execute(
        "SELECT user_id, username, score FROM users WHERE score > 0 ORDER BY score DESC LIMIT ?",
        (limit,),
    ).fetchall()
    return [dict(r) for r in rows]


def has_reminders_for_today(user_id: int, current_date: str) -> bool:
    """
    Проверяет, есть ли у пользователя задачи в CRM (таблица reminders) на указанную дату.
    Предполагается, что поле даты называется remind_date.
    """
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT 1 FROM reminders WHERE user_id = ? AND remind_date = ? LIMIT 1",
            (user_id, current_date),
        ).fetchone()
        return row is not None
    except sqlite3.OperationalError:
        # Если таблицы или поля нет, считаем что задач нет
        return False


# ── CRM reminders (crm_reminders) ────────────────────────────────────────────

def add_crm_reminder(user_id: int, run_at: str, task_text: str) -> int:
    """Добавляет напоминание. run_at: ISO datetime. Возвращает id."""
    conn = _get_conn()
    cur = conn.execute(
        "INSERT INTO crm_reminders (user_id, run_at, task_text) VALUES (?, ?, ?)",
        (user_id, run_at, task_text),
    )
    conn.commit()
    return cur.lastrowid or 0


def get_user_crm_reminders(user_id: int) -> list[dict]:
    """Возвращает активные напоминания пользователя (run_at >= now)."""
    conn = _get_conn()
    rows = conn.execute(
        """
        SELECT id, user_id, run_at, task_text
        FROM crm_reminders
        WHERE user_id = ? AND run_at >= datetime('now')
        ORDER BY run_at
        """,
        (user_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def get_due_crm_reminders() -> list[dict]:
    """Возвращает напоминания, которые пора отправить."""
    conn = _get_conn()
    rows = conn.execute(
        """
        SELECT id, user_id, task_text
        FROM crm_reminders
        WHERE run_at <= datetime('now')
        """
    ).fetchall()
    return [dict(r) for r in rows]


def delete_crm_reminder(reminder_id: int) -> None:
    """Удаляет напоминание."""
    conn = _get_conn()
    conn.execute("DELETE FROM crm_reminders WHERE id = ?", (reminder_id,))
    conn.commit()


def get_total_users() -> int:
    """Возвращает общее количество пользователей."""
    conn = _get_conn()
    row = conn.execute("SELECT COUNT(*) FROM users").fetchone()
    return row[0] if row else 0


def get_all_user_ids() -> list[int]:
    """Возвращает список всех user_id."""
    conn = _get_conn()
    rows = conn.execute("SELECT user_id FROM users").fetchall()
    return [r[0] for r in rows]


def get_user_profile(user_id: int) -> dict | None:
    """Возвращает данные профиля пользователя для AI-анализа."""
    conn = _get_conn()
    row = conn.execute(
        "SELECT user_id, username, full_name, score, last_tracker_date, streak, incoins, timezone FROM users WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    return dict(row) if row else None


def get_all_users_admin() -> list[dict]:
    """Возвращает список всех пользователей для админ-панели."""
    conn = _get_conn()
    rows = conn.execute(
        "SELECT user_id, username, full_name, streak, is_blocked FROM users"
    ).fetchall()
    return [dict(r) for r in rows]


def set_user_block_status(user_id: int, is_blocked: bool) -> None:
    """Устанавливает статус блокировки пользователя."""
    conn = _get_conn()
    conn.execute(
        "UPDATE users SET is_blocked = ? WHERE user_id = ?",
        (1 if is_blocked else 0, user_id)
    )
    conn.commit()


def is_user_blocked(user_id: int) -> bool:
    """Возвращает True, если пользователь заблокирован."""
    conn = _get_conn()
    row = conn.execute(
        "SELECT is_blocked FROM users WHERE user_id = ?", (user_id,)
    ).fetchone()
    return bool(row["is_blocked"]) if row else False


def check_authorization(user_id: int) -> bool:
    """Возвращает True, если пользователь авторизован."""
    conn = _get_conn()
    row = conn.execute(
        "SELECT is_authorized FROM users WHERE user_id = ?", (user_id,)
    ).fetchone()
    return bool(row["is_authorized"]) if row else False


def authorize_user(user_id: int) -> None:
    """Устанавливает статус авторизации для пользователя (is_authorized = 1)."""
    conn = _get_conn()
    conn.execute(
        "UPDATE users SET is_authorized = 1 WHERE user_id = ?", (user_id,)
    )
    conn.commit()


def reset_all_authorizations(admin_id: int) -> None:
    """Сбрасывает авторизацию всем пользователям, кроме администратора."""
    conn = _get_conn()
    conn.execute(
        "UPDATE users SET is_authorized = 0 WHERE user_id != ?", (admin_id,)
    )
    conn.commit()


def reset_test_period_for_all(admin_id: int) -> int:
    """
    Сбрасывает условие тестового периода для всех пользователей:
    устанавливает incoins = 5 (как при первом входе).
    Возвращает количество обновлённых строк. Администратор не затрагивается.
    """
    conn = _get_conn()
    cursor = conn.execute(
        "UPDATE users SET incoins = 5 WHERE user_id != ?", (admin_id,)
    )
    conn.commit()
    return cursor.rowcount


def get_setting(key: str, default_value: str) -> str:
    """Возвращает значение настройки из таблицы settings."""
    conn = _get_conn()
    row = conn.execute(
        "SELECT value FROM settings WHERE key = ?", (key,)
    ).fetchone()
    return row["value"] if row else default_value


def create_payment_order(order_id: str, user_id: int, amount_rub: float, amount_coins: int | None = None) -> None:
    """Создаёт запись о заказе на пополнение. amount_coins — для тарифов (иначе 1₽=1 монета)."""
    conn = _get_conn()
    conn.execute(
        "INSERT INTO payment_orders (order_id, user_id, amount_rub, amount_coins, status) VALUES (?, ?, ?, ?, 'pending')",
        (order_id, user_id, amount_rub, amount_coins),
    )
    conn.commit()


def get_payment_order(order_id: str) -> dict | None:
    """Возвращает заказ по order_id или None."""
    conn = _get_conn()
    row = conn.execute(
        "SELECT order_id, user_id, amount_rub, COALESCE(amount_coins, 0) as amount_coins, status FROM payment_orders WHERE order_id = ?",
        (order_id,),
    ).fetchone()
    return dict(row) if row else None


def mark_payment_paid(order_id: str) -> bool:
    """Помечает заказ как оплаченный. Возвращает True если обновлён."""
    conn = _get_conn()
    cursor = conn.execute(
        "UPDATE payment_orders SET status = 'paid' WHERE order_id = ? AND status = 'pending'",
        (order_id,),
    )
    conn.commit()
    return cursor.rowcount > 0


def log_usage(user_id: int, task_type: str, model: str, cost: float | None) -> None:
    """Логирует одну генерацию для аналитики."""
    conn = _get_conn()
    conn.execute(
        "INSERT INTO usage_log (user_id, task_type, model, cost) VALUES (?, ?, ?, ?)",
        (user_id, task_type, model, cost if cost is not None else 0.0),
    )
    conn.commit()


def get_usage_for_user(user_id: int) -> list[dict]:
    """Возвращает список генераций пользователя для отчёта."""
    conn = _get_conn()
    rows = conn.execute(
        """SELECT task_type, model, cost, created_at FROM usage_log 
           WHERE user_id = ? ORDER BY created_at DESC""",
        (user_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def get_usage_aggregate() -> dict:
    """Агрегированная статистика по всем пользователям: по user_id, общая стоимость, топ активных."""
    conn = _get_conn()
    by_user = conn.execute(
        """SELECT user_id, COUNT(*) as cnt, COALESCE(SUM(cost), 0) as total_cost
           FROM usage_log GROUP BY user_id"""
    ).fetchall()
    totals = conn.execute(
        "SELECT COUNT(*) as total_gen, COALESCE(SUM(cost), 0) as total_cost FROM usage_log"
    ).fetchone()
    by_task = conn.execute(
        """SELECT task_type, COUNT(*) as cnt FROM usage_log GROUP BY task_type"""
    ).fetchall()
    return {
        "by_user": [dict(r) for r in by_user],
        "total_gen": totals["total_gen"] if totals else 0,
        "total_cost": float(totals["total_cost"]) if totals else 0,
        "by_task": [dict(r) for r in by_task],
    }


def get_usage_costs_by_period() -> dict:
    """
    Возвращает суммы затрат и количество генераций за сегодня, 7 дней и месяц.
    Учитываются ВСЕ пользователи. Без фильтрации.
    """
    conn = _get_conn()
    today_filter = "date(created_at) = date('now', 'localtime')"
    filter_7d = "created_at >= datetime('now', '-7 days')"
    filter_30d = "created_at >= datetime('now', '-30 days')"

    def _row(q):
        r = conn.execute(q).fetchone()
        return r[0] if r else 0

    return {
        "cost_today": float(_row(f"SELECT COALESCE(SUM(cost), 0) FROM usage_log WHERE {today_filter}")),
        "cost_7d": float(_row(f"SELECT COALESCE(SUM(cost), 0) FROM usage_log WHERE {filter_7d}")),
        "cost_month": float(_row(f"SELECT COALESCE(SUM(cost), 0) FROM usage_log WHERE {filter_30d}")),
        "gen_today": int(_row(f"SELECT COUNT(*) FROM usage_log WHERE {today_filter}")),
        "gen_7d": int(_row(f"SELECT COUNT(*) FROM usage_log WHERE {filter_7d}")),
        "gen_month": int(_row(f"SELECT COUNT(*) FROM usage_log WHERE {filter_30d}")),
    }


def get_usage_by_user_period() -> list[dict]:
    """
    Для каждого пользователя: затраты и генерации за сегодня, 7 дней, месяц и всего.
    ВСЕ пользователи из usage_log, без исключений.
    """
    conn = _get_conn()
    today_filter = "date(created_at) = date('now', 'localtime')"
    filter_7d = "created_at >= datetime('now', '-7 days')"
    filter_30d = "created_at >= datetime('now', '-30 days')"

    rows = conn.execute(
        """SELECT user_id,
           COALESCE(SUM(CASE WHEN """ + today_filter + """ THEN cost ELSE 0 END), 0) as cost_today,
           COALESCE(SUM(CASE WHEN """ + filter_7d + """ THEN cost ELSE 0 END), 0) as cost_7d,
           COALESCE(SUM(CASE WHEN """ + filter_30d + """ THEN cost ELSE 0 END), 0) as cost_month,
           COALESCE(SUM(cost), 0) as cost_total,
           COUNT(CASE WHEN """ + today_filter + """ THEN 1 END) as gen_today,
           COUNT(CASE WHEN """ + filter_7d + """ THEN 1 END) as gen_7d,
           COUNT(CASE WHEN """ + filter_30d + """ THEN 1 END) as gen_month,
           COUNT(*) as gen_total
           FROM usage_log GROUP BY user_id"""
    ).fetchall()
    return [dict(r) for r in rows]


def set_setting(key: str, value: str) -> None:
    """Сохраняет или обновляет настройку в таблице settings."""
    conn = _get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
        (key, value),
    )
    conn.commit()
