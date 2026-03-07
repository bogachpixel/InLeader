import logging
import os
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config.i18n import TEXTS
from services import ai_service
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

def _build_mentor_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧠 Майндсет и Мышление", callback_data="mentor:mindset")],
        [InlineKeyboardButton(text="💰 Искусство Продаж", callback_data="mentor:sales")],
        [InlineKeyboardButton(text="🎯 Стратегический Коучинг", callback_data="mentor:coaching")],
        [InlineKeyboardButton(text="👥 Лидерство и Менеджмент", callback_data="mentor:management")],
        [InlineKeyboardButton(text="🧘‍♂️ Психология Влияния", callback_data="mentor:psychology")],
        [InlineKeyboardButton(text="🌐 MLM и Масштабирование", callback_data="mentor:mlm")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="menu:main")]
    ])
    return kb

@router.callback_query(F.data == "menu:mentor")
async def menu_mentor(callback: CallbackQuery, state: FSMContext) -> None:
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
    await callback.message.answer(
        "🧠 <b>Твой личный Совет Директоров на связи!</b>\n\nЗдесь нет воды — только глубокий анализ, выжимка опыта и четкие стратегии. В любой непонятной ситуации обращайся к своим AI-наставникам.\n\nКакую сферу будем прокачивать сейчас? Выбери эксперта:",
        reply_markup=_build_mentor_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("mentor:"))
async def mentor_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    mentor_key = callback.data.split(":")[1]
    prompt = MENTOR_PROMPTS.get(mentor_key)
    
    await callback.answer()
    await state.update_data(system_prompt=prompt)
    await state.set_state(MentorState.waiting_for_question)
    await callback.message.answer("Отличный выбор. Я готов. Опиши свою текущую ситуацию или задай вопрос:", parse_mode=None)

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
        response_text = await ai_service.generate_text(message.text, system_prompt, task_type="mentor")
        await wait_msg.edit_text(response_text, parse_mode=None)
        
        if uid != ADMIN_ID:
            db.add_user_coins_admin(uid, -1)
            await message.answer(f"⚡️ Успешно! Списана 1 монета. Остаток: {coins - 1} 🪙")
            
    except Exception as e:
        print(f"🔥 ОШИБКА ГЕНЕРАЦИИ (СМОТРЕТЬ СЮДА): {repr(e)}") # Вывод в консоль PyCharm!
        await wait_msg.edit_text("❌ Ошибка соединения с нейросетью. Монеты не списаны. Обратитесь к администратору.", parse_mode=None)
        return
