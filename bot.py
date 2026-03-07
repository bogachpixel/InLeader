import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from dotenv import load_dotenv

from handlers.analyzer import router as analyzer_router
from handlers.calculator import router as calculator_router
from handlers.copywriter import router as copywriter_router
from handlers.crm import router as crm_router
from handlers.leaderboard import router as leaderboard_router
from handlers.mentor import router as mentor_router
from handlers.marketing import router as marketing_router
from handlers.account import router as account_router
from handlers.documents import router as documents_router
from handlers.objections import router as objections_router
from handlers.onboarding import router as onboarding_router
from handlers.simulator import router as simulator_router
from handlers.start import router as start_router
from handlers.tracker import router as tracker_router
from handlers.admin import router as admin_router
from services.db import init_db
from services.scheduler import scheduler, tracker_reminder_job

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def set_bot_commands(bot: Bot) -> None:
    """Настройка команд бота в меню."""
    admin_id_str = os.getenv("ADMIN_ID", "5925660014")
    try:
        admin_id = int(admin_id_str)
    except ValueError:
        admin_id = 0

    # Команды для обычных пользователей — пусто (без / в меню)
    await bot.set_my_commands([], scope=BotCommandScopeDefault())

    # Команды для администратора
    if admin_id:
        admin_commands = [
            BotCommand(command="start", description="🔄 Перезапустить бота"),
            BotCommand(command="admin", description="👑 Панель управления"),
            BotCommand(command="image", description="🖼 Генерация картинки"),
        ]
        try:
            await bot.set_my_commands(
                admin_commands, 
                scope=BotCommandScopeChat(chat_id=admin_id)
            )
        except Exception as e:
            logger.warning(f"Не удалось установить команды для админа ({admin_id}): {e}")


async def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise EnvironmentError("TELEGRAM_BOT_TOKEN is not set in .env")

    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
    )
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(copywriter_router)
    dp.include_router(objections_router)
    dp.include_router(account_router)
    dp.include_router(marketing_router)
    dp.include_router(documents_router)
    dp.include_router(tracker_router)
    dp.include_router(calculator_router)
    dp.include_router(simulator_router)
    dp.include_router(crm_router)
    dp.include_router(onboarding_router)
    dp.include_router(analyzer_router)
    dp.include_router(mentor_router)
    dp.include_router(leaderboard_router)
    dp.include_router(admin_router)

    init_db()
    
    # Установка команд в меню
    await set_bot_commands(bot)

    scheduler.add_job(
        tracker_reminder_job,
        "cron",
        minute=0,
        args=[bot],
        id="tracker_reminder",
        replace_existing=True,
    )
    scheduler.start()
    
    logger.info("InLeader bot is starting...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
