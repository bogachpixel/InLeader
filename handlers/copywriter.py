import logging
import os
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config.i18n import TEXTS
from config.prompts import get_system_instruction
from services import ai_service
from services import db
from services.language import t

router = Router()
logger = logging.getLogger(__name__)

ADMIN_ID = int(os.getenv("ADMIN_ID", "5925660014"))

class CopywriterState(StatesGroup):
    waiting_for_custom_topic = State()

def _build_copywriter_keyboard(user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=t(user_id, "copy_story"), callback_data="copy:story")
    kb.button(text=t(user_id, "copy_free"), callback_data="copy:free")
    kb.button(text=t(user_id, "copy_top5"), callback_data="copy:top5")
    kb.button(text=t(user_id, "copy_money"), callback_data="copy:money")
    kb.button(text=t(user_id, "copy_kids"), callback_data="copy:kids")
    kb.button(text=t(user_id, "copy_myths"), callback_data="copy:myths")
    kb.button(text=t(user_id, "copy_motivation"), callback_data="copy:motivation")
    kb.button(text=t(user_id, "copy_liner"), callback_data="copy:liner")
    kb.button(text=t(user_id, "copy_custom"), callback_data="copy:custom")
    kb.button(text=t(user_id, "btn_back_menu"), callback_data="menu:main")
    kb.adjust(2)
    return kb.as_markup()

@router.callback_query(F.data == "menu:copywriter")
async def menu_copywriter(callback: CallbackQuery, state: FSMContext):
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
    await callback.message.answer(t(uid, "copywriter_title"), reply_markup=_build_copywriter_keyboard(uid))

@router.callback_query(F.data.startswith("copy:"))
async def process_copy_preset(callback: CallbackQuery, state: FSMContext):
    topic_key = callback.data.split(":")[1]
    uid = callback.from_user.id
    
    if topic_key == "custom":
        await state.set_state(CopywriterState.waiting_for_custom_topic)
        await callback.message.answer(t(uid, "copy_ask_custom"))
        await callback.answer()
        return

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
            await callback.message.answer(text, parse_mode="HTML")
            await callback.answer()
            return
    coins = db.get_user_coins(uid)

    # 2. ВРЕМЕННОЕ СООБЩЕНИЕ
    wait_msg = await callback.message.answer("⏳ Готовлю ответ. Пожалуйста, подождите...")
    await callback.answer()

    topic_text = t(uid, f"copy_{topic_key}")
    prompt = f"Напиши пост для инстаграм по теме «{topic_text}». Учитывай контекст выбранной кнопки. Используй смайлики и призыв к действию."

    try:
        # 3. ГЕНЕРАЦИЯ ТЕКСТА
        response_text = await ai_service.generate_text(prompt, get_system_instruction(uid), task_type="copywriter")
        
        if response_text.startswith("⚠️"):
            await wait_msg.edit_text(response_text, parse_mode=None)
            return

        await wait_msg.edit_text(response_text, parse_mode=None)
        
        # 6. СПИСАНИЕ ТОЛЬКО ПРИ УСПЕХЕ
        if uid != ADMIN_ID:
            db.add_user_coins_admin(uid, -1)
            await callback.message.answer(f"⚡️ Успешно! Списана 1 монета. Остаток: {coins - 1} 🪙")
            
    except Exception as e:
        print(f"🔥 ОШИБКА ГЕНЕРАЦИИ (СМОТРЕТЬ СЮДА): {repr(e)}") # Вывод в консоль PyCharm!
        await wait_msg.edit_text("❌ Ошибка соединения с нейросетью. Монеты не списаны. Обратитесь к администратору.", parse_mode=None)
        return

@router.message(CopywriterState.waiting_for_custom_topic)
async def process_custom_copy(message: Message, state: FSMContext):
    uid = message.from_user.id
    prompt = message.text
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
    coins = db.get_user_coins(uid)

    wait_msg = await message.answer("⏳ Готовлю ответ. Пожалуйста, подождите...")

    try:
        response_text = await ai_service.generate_text(prompt, get_system_instruction(uid), task_type="copywriter")
        
        if response_text.startswith("⚠️"):
            await wait_msg.edit_text(response_text, parse_mode=None)
            return

        await wait_msg.edit_text(response_text, parse_mode=None)
        
        if uid != ADMIN_ID:
            db.add_user_coins_admin(uid, -1)
            await message.answer(f"⚡️ Успешно! Списана 1 монета. Остаток: {coins - 1} 🪙")
            
    except Exception as e:
        print(f"🔥 ОШИБКА ГЕНЕРАЦИИ (СМОТРЕТЬ СЮДА): {repr(e)}") # Вывод в консоль PyCharm!
        await wait_msg.edit_text("❌ Ошибка соединения с нейросетью. Монеты не списаны. Обратитесь к администратору.", parse_mode=None)
        return
