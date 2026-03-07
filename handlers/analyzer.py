import logging
import os

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from config.i18n import TEXTS
from services import db
from services.ai_service import generate_text
from services.language import t

logger = logging.getLogger(__name__)
ADMIN_ID = int(os.getenv("ADMIN_ID", "5925660014"))

router = Router()

_ALL_ANALYZER_BUTTONS = {
    texts["btn_analyzer"] for texts in TEXTS.values() if "btn_analyzer" in texts
}

ANALYZER_SYSTEM_PROMPT = (
    "Ты — жёсткий, но справедливый топ-лидер inCruises и гений продаж. "
    "Проанализируй отчёт о встрече. Выдай ответ строго по структуре:\n\n"
    "1. 🧠 Психология клиента (что он на самом деле имел в виду, когда возражал).\n"
    "2. ❌ Твои ошибки (где ты недожал, какую выгоду не продал).\n"
    "3. 💬 Сообщение для дожима (напиши 1 готовый, мощный вариант SMS/сообщения, "
    "которое партнёр может скопировать и отправить клиенту прямо сейчас, "
    "чтобы вывести его на следующий шаг).\n\n"
    "Форматируй ответ красиво, без лишней воды. Ответ на русском."
)


class AnalyzerState(StatesGroup):
    waiting_for_summary = State()


@router.callback_query(F.data == "menu:analyzer")
async def menu_analyzer(callback: CallbackQuery, state: FSMContext) -> None:
    uid = callback.from_user.id
    if uid != ADMIN_ID:
        coins = db.get_user_coins(uid)
        if coins < 1:
            text = (
                "⚠️ <b>Доступ ограничен</b>\n\n"
                "Твой тестовый период или текущий баланс InCoins подошли к концу. "
                "Инструменты бота ждут тебя, но для их запуска необходимо подзарядить кошелек.\n\n"
                "💎 <b>Пополни баланс и продолжай творить вместе с ИИ!</b>\n\n"
                "<i>Для пополнения баланса и активации всех функций обратись к своему наставнику или администратору.</i>"
            )
            await callback.message.answer(text, parse_mode="HTML")
            await callback.answer()
            return
    await callback.answer()
    await state.clear()
    await callback.message.answer(t(uid, "analyzer_ask"), parse_mode=None)
    await state.set_state(AnalyzerState.waiting_for_summary)


@router.message(F.text.func(lambda text: text in _ALL_ANALYZER_BUTTONS))
async def analyzer_menu(message: Message, state: FSMContext) -> None:
    uid = message.from_user.id
    if uid != ADMIN_ID:
        coins = db.get_user_coins(uid)
        if coins < 1:
            text = (
                "⚠️ <b>Доступ ограничен</b>\n\n"
                "Твой тестовый период или текущий баланс InCoins подошли к концу. "
                "Инструменты бота ждут тебя, но для их запуска необходимо подзарядить кошелек.\n\n"
                "💎 <b>Пополни баланс и продолжай творить вместе с ИИ!</b>\n\n"
                "<i>Для пополнения баланса и активации всех функций обратись к своему наставнику или администратору.</i>"
            )
            await message.answer(text, parse_mode="HTML")
            return
    await state.clear()
    await message.answer(t(uid, "analyzer_ask"), parse_mode=None)
    await state.set_state(AnalyzerState.waiting_for_summary)


@router.message(AnalyzerState.waiting_for_summary)
async def analyzer_process(message: Message, state: FSMContext) -> None:
    uid = message.from_user.id
    await state.clear()

    # 1. Мягкий пэйволл (турникет)
    if uid != ADMIN_ID:
        coins = db.get_user_coins(uid)
        if coins < 1:
            text = (
                "⚠️ <b>Доступ ограничен</b>\n\n"
                "Твой тестовый период или текущий баланс InCoins подошли к концу. "
                "Инструменты бота ждут тебя, но для их запуска необходимо подзарядить кошелек.\n\n"
                "💎 <b>Пополни баланс и продолжай творить вместе с ИИ!</b>\n\n"
                "<i>Для пополнения баланса и активации всех функций обратись к своему наставнику или администратору.</i>"
            )
            await message.answer(text, parse_mode="HTML")
            return

    status = await message.answer(t(uid, "analyzer_thinking"))

    result = await generate_text(
        prompt=message.text,
        system_instruction=ANALYZER_SYSTEM_PROMPT,
        task_type="analyzer",
        user_id=uid,
    )

    try:
        await status.edit_text(result, parse_mode=None)
    except Exception:
        await message.answer(result, parse_mode=None)

    if not result.startswith("⚠️") and uid != ADMIN_ID:
        db.add_user_coins_admin(uid, -1)
        coins = db.get_user_coins(uid)
        await message.answer(f"⚡️ Успешно! Списана 1 монета. Остаток: {coins} 🪙")
