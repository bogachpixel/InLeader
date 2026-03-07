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

TRACKER_REMINDER_TEXT = (
    "⏰ Капитан! Время 20:00, а твой Журнал пуст! "
    "Зайди в Трекер, иначе твой стрик сгорит!"
)


async def tracker_reminder_job(bot: Bot) -> None:
    """Каждый час проверяет: кому сейчас 20:00 по локальному времени — отправляет пуш."""
    from datetime import datetime

    from services.db import get_users_for_tracker_reminder

    utc_hour = datetime.utcnow().hour
    user_ids = get_users_for_tracker_reminder(utc_hour)
    for uid in user_ids:
        try:
            await bot.send_message(uid, TRACKER_REMINDER_TEXT, parse_mode=None)
        except Exception as e:
            logger.warning("Tracker reminder to %s: %s", uid, e)


async def send_reminder(bot: Bot, chat_id: int, text: str) -> None:
    try:
        await bot.send_message(
            chat_id,
            f"🔔 *Напоминание (Follow-up):*\n\n{text}",
            parse_mode=None,
        )
    except Exception as e:
        logger.error("Failed to send reminder to %s: %s", chat_id, e)
