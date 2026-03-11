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
from services.ai_service import format_admin_footer
from services import db
from services.language import t

router = Router()
logger = logging.getLogger(__name__)
ADMIN_ID = int(os.getenv("ADMIN_ID", "5925660014"))

class ObjectionsState(StatesGroup):
    waiting_for_custom_objection = State()

def _build_objections_keyboard(user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=t(user_id, "obj_money"), callback_data="obj:money")
    kb.button(text=t(user_id, "obj_time"), callback_data="obj:time")
    kb.button(text=t(user_id, "obj_pyramid"), callback_data="obj:pyramid")
    kb.button(text=t(user_id, "obj_family"), callback_data="obj:family")
    kb.button(text=t(user_id, "obj_invite"), callback_data="obj:invite")
    kb.button(text=t(user_id, "obj_seasick"), callback_data="obj:seasick")
    kb.button(text=t(user_id, "obj_visa"), callback_data="obj:visa")
    kb.button(text=t(user_id, "obj_language"), callback_data="obj:language")
    kb.button(text=t(user_id, "obj_custom"), callback_data="obj:custom")
    kb.button(text=t(user_id, "btn_back_menu"), callback_data="menu:main")
    kb.adjust(2)
    return kb.as_markup()

@router.callback_query(F.data == "menu:objections")
async def menu_objections(callback: CallbackQuery, state: FSMContext):
    uid = callback.from_user.id
    if uid != ADMIN_ID:
        coins = db.get_user_coins(uid)
        if coins < 1:
            await callback.message.answer(t(uid, "paywall_text"), parse_mode="HTML")
            await callback.answer()
            return
    await callback.answer()
    await state.clear()
    await callback.message.answer(t(uid, "objections_title"), reply_markup=_build_objections_keyboard(uid))

@router.callback_query(F.data.startswith("obj:"))
async def process_objection_preset(callback: CallbackQuery, state: FSMContext):
    obj_key = callback.data.split(":")[1]
    uid = callback.from_user.id
    
    if obj_key == "custom":
        await state.set_state(ObjectionsState.waiting_for_custom_objection)
        await callback.message.answer(t(uid, "obj_ask_custom"))
        await callback.answer()
        return

    # 1. Мягкий пэйволл (турникет)
    if uid != ADMIN_ID:
        coins = db.get_user_coins(uid)
        if coins < 1:
            await callback.message.answer(t(uid, "paywall_text"), parse_mode="HTML")
            await callback.answer()
            return
    coins = db.get_user_coins(uid)

    wait_msg = await callback.message.answer("⏳ Готовлю ответ. Пожалуйста, подождите...")
    await callback.answer()

    obj_text = t(uid, f"obj_{obj_key}")
    prompt = f"Клиент говорит: {obj_text}. Дай 3 убийственных аргумента для отработки этого возражения в inCruises."

    try:
        gen = await ai_service.generate_text(prompt, get_system_instruction(uid), task_type="objections")
        display = gen.text + format_admin_footer(gen, uid)
        await wait_msg.edit_text(display, parse_mode=None)
        
        if uid != ADMIN_ID:
            db.add_user_coins_admin(uid, -1)
            await callback.message.answer(t(uid, "coin_deducted", coins=coins - 1))
            
    except Exception as e:
        print(f"🔥 ОШИБКА ГЕНЕРАЦИИ (СМОТРЕТЬ СЮДА): {repr(e)}") # Вывод в консоль PyCharm!
        await wait_msg.edit_text("❌ Ошибка соединения с нейросетью. Монеты не списаны. Обратитесь к администратору.", parse_mode=None)
        return

@router.message(ObjectionsState.waiting_for_custom_objection)
async def process_custom_objection(message: Message, state: FSMContext):
    uid = message.from_user.id
    prompt = message.text
    await state.clear()

    # 1. Мягкий пэйволл (турникет)
    if uid != ADMIN_ID:
        coins = db.get_user_coins(uid)
        if coins < 1:
            await message.answer(t(uid, "paywall_text"), parse_mode="HTML")
            return
    coins = db.get_user_coins(uid)

    wait_msg = await message.answer("⏳ Готовлю ответ. Пожалуйста, подождите...")

    try:
        gen = await ai_service.generate_text(prompt, get_system_instruction(uid), task_type="objections")
        display = gen.text + format_admin_footer(gen, uid)
        await wait_msg.edit_text(display, parse_mode=None)
        
        if uid != ADMIN_ID:
            db.add_user_coins_admin(uid, -1)
            await message.answer(t(uid, "coin_deducted", coins=coins - 1))
            
    except Exception as e:
        print(f"🔥 ОШИБКА ГЕНЕРАЦИИ (СМОТРЕТЬ СЮДА): {repr(e)}") # Вывод в консоль PyCharm!
        await wait_msg.edit_text("❌ Ошибка соединения с нейросетью. Монеты не списаны. Обратитесь к администратору.", parse_mode=None)
        return
