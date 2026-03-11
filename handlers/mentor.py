import logging
import os
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config.i18n import TEXTS
from services import ai_service
from services.ai_service import format_admin_footer
from services import db
from services.language import t

router = Router()
logger = logging.getLogger(__name__)
ADMIN_ID = int(os.getenv("ADMIN_ID", "5925660014"))

MENTOR_PROMPTS = {
    "mindset": "Ты — Эксперт по мышлению миллионеров. Твоя цель: расширять сознание пользователя, снимать ограничивающие убеждения и страхи, заряжать мощной энергией. Общайся вдохновляюще, уверенно, на 'ты'. Используй метафоры.",
    "sales": "Ты — Гений продаж и жесткий клоузер. Твоя цель: давать конкретные скрипты, техники дожима, работы с возражениями и НЛП в продажах. Никакой воды. Общайся дерзко, четко, как акула бизнеса. На 'ты'.",
    "coaching": "Ты — Топовый Бизнес-коуч. Твоя цель: не давать готовых ответов, а задавать сильные, глубокие вопросы, которые приведут пользователя к инсайту. Помогай декомпозировать цели и строить пошаговые планы.",
    "management": "Ты — Эксперт по менеджменту и управлению. Твоя цель: учить строить системы, делегировать, мотивировать команду и разрешать конфликты. Общайся структурно, по делу, оперируй терминами управления и эффективности.",
    "psychology": "Ты — Глубокий Психолог. Твоя цель: помочь пользователю с эмоциональным выгоранием, стрессом, пониманием мотивов других людей (эмпатией). Общайся мягко, с пониманием, как мудрый наставник.",
    "mlm": "Ты — Легендарный топ-лидер сетевого бизнеса (MLM). Твоя цель: давать стратегии рекрутинга, удержания команды, дупликации и работы с глубиной. Общайся энергично, как спонсор, который верит в своего партнера."
}

class MentorState(StatesGroup):
    waiting_for_question = State()

def _build_mentor_keyboard(user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(user_id, "mentor_mindset"), callback_data="mentor:mindset")],
        [InlineKeyboardButton(text=t(user_id, "mentor_sales"), callback_data="mentor:sales")],
        [InlineKeyboardButton(text=t(user_id, "mentor_coaching"), callback_data="mentor:coaching")],
        [InlineKeyboardButton(text=t(user_id, "mentor_management"), callback_data="mentor:management")],
        [InlineKeyboardButton(text=t(user_id, "mentor_psychology"), callback_data="mentor:psychology")],
        [InlineKeyboardButton(text=t(user_id, "mentor_mlm"), callback_data="mentor:mlm")],
        [InlineKeyboardButton(text=t(user_id, "btn_back_menu"), callback_data="menu:main")]
    ])
    return kb

@router.callback_query(F.data == "menu:mentor")
async def menu_mentor(callback: CallbackQuery, state: FSMContext) -> None:
    uid = callback.from_user.id
    if uid != ADMIN_ID:
        coins = db.get_user_coins(uid)
        if coins < 1:
            await callback.message.answer(t(uid, "paywall_text"), parse_mode="HTML")
            await callback.answer()
            return
    await callback.answer()
    await state.clear()
    await callback.message.answer(
        t(uid, "mentor_title"),
        reply_markup=_build_mentor_keyboard(uid),
        parse_mode="HTML",
    )

@router.callback_query(F.data.startswith("mentor:"))
async def mentor_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    mentor_key = callback.data.split(":")[1]
    prompt = MENTOR_PROMPTS.get(mentor_key)
    
    await callback.answer()
    await state.update_data(system_prompt=prompt)
    await state.set_state(MentorState.waiting_for_question)
    await callback.message.answer(t(callback.from_user.id, "mentor_ask"), parse_mode=None)

@router.message(MentorState.waiting_for_question)
async def mentor_answer(message: Message, state: FSMContext) -> None:
    uid = message.from_user.id
    data = await state.get_data()
    system_prompt = data.get("system_prompt")
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
        gen = await ai_service.generate_text(message.text, system_prompt, task_type="mentor")
        display = gen.text + format_admin_footer(gen, uid)
        await wait_msg.edit_text(display, parse_mode=None)
        
        if uid != ADMIN_ID:
            db.add_user_coins_admin(uid, -1)
            await message.answer(t(message.from_user.id, "coin_deducted", coins=coins - 1))
            
    except Exception as e:
        print(f"🔥 ОШИБКА ГЕНЕРАЦИИ (СМОТРЕТЬ СЮДА): {repr(e)}") # Вывод в консоль PyCharm!
        await wait_msg.edit_text("❌ Ошибка соединения с нейросетью. Монеты не списаны. Обратитесь к администратору.", parse_mode=None)
        return
