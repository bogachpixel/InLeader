"""
APScheduler-based reminder service.

scheduler  — singleton AsyncIOScheduler (start it once in bot.py)
send_reminder() — callback that fires when a reminder is due
"""

import logging

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

async def tracker_reminder_job(bot: Bot) -> None:
    """Каждый час проверяет: кому сейчас 20:00 по локальному времени — отправляет пуш."""
    from datetime import datetime

    from services.db import get_users_for_tracker_reminder
    from services.language import t

    utc_hour = datetime.utcnow().hour
    user_ids = get_users_for_tracker_reminder(utc_hour)
    for uid in user_ids:
        try:
            text = t(uid, "trk_reminder")
            await bot.send_message(uid, text, parse_mode=None)
        except Exception as e:
            logger.warning("Tracker reminder to %s: %s", uid, e)


async def send_reminder(bot: Bot, chat_id: int, text: str) -> None:
    from services.language import t

    try:
        header = t(chat_id, "crm_reminder_header")
        await bot.send_message(
            chat_id,
            f"{header}\n\n{text}",
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error("Failed to send reminder to %s: %s", chat_id, e)


async def crm_delivery_job(bot: Bot) -> None:
    """Каждую минуту проверяет БД на просроченные напоминания, отправляет и удаляет."""
    from services.db import get_due_crm_reminders, delete_crm_reminder

    due = get_due_crm_reminders()
    for r in due:
        rid = r.get("id")
        uid = r.get("user_id")
        task_text = r.get("task_text", "—")
        try:
            await send_reminder(bot, uid, task_text)
            if rid is not None:
                delete_crm_reminder(rid)
        except Exception as e:
            logger.warning("CRM reminder to %s failed: %s", uid, e)
