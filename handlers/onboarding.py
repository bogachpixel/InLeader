import logging
import os
from pathlib import Path
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

from config.i18n import TEXTS
from services import db
from services.ai_service import generate_text
from services.language import t
from pypdf import PdfReader

router = Router()
logger = logging.getLogger(__name__)
ADMIN_ID = int(os.getenv("ADMIN_ID", "5925660014"))

_ALL_ONBOARDING_BUTTONS = {
    texts["btn_onboarding"] for texts in TEXTS.values() if "btn_onboarding" in texts
}

class OnboardingState(StatesGroup):
    choosing_role = State()
    chatting = State()
    navigator_q1 = State()
    navigator_q2 = State()
    navigator_q3 = State()

def read_pdf_content(file_path: Path) -> str:
    """Читает текст из PDF файла."""
    if not file_path.exists():
        return ""
    try:
        reader = PdfReader(file_path)
        return "\n".join((p.extract_text() or "") for p in reader.pages).strip()
    except Exception as e:
        logger.error(f"Error reading PDF {file_path}: {e}")
        return ""

@router.callback_query(F.data == "menu:onboarding")
async def menu_onboarding(callback: CallbackQuery, state: FSMContext) -> None:
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
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏖️ Турист (Клубные привилегии +)", callback_data="newbie:tourist")],
        [InlineKeyboardButton(text="💼 Партнер (Бизнес и доход)", callback_data="newbie:partner")],
        [InlineKeyboardButton(text="🚀 ИИ-Навигатор: Мой план успеха", callback_data="newbie:navigator")]
    ])
    
    await callback.message.answer(
        "👋 Добро пожаловать в команду InCruises!\n\nЧтобы я подготовил для тебя персональный план развития, выбери свою текущую цель:",
        reply_markup=kb
    )
    await state.set_state(OnboardingState.choosing_role)

@router.message(F.text.func(lambda text: text in _ALL_ONBOARDING_BUTTONS))
async def onboarding_start(message: Message, state: FSMContext) -> None:
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
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏖️ Турист (Клубные привилегии +)", callback_data="newbie:tourist")],
        [InlineKeyboardButton(text="💼 Партнер (Бизнес и доход)", callback_data="newbie:partner")],
        [InlineKeyboardButton(text="🚀 ИИ-Навигатор: Мой план успеха", callback_data="newbie:navigator")]
    ])
    
    await message.answer(
        "👋 Добро пожаловать в команду InCruises!\n\nЧтобы я подготовил для тебя персональный план развития, выбери свою текущую цель:",
        reply_markup=kb
    )
    await state.set_state(OnboardingState.choosing_role)

NAVIGATOR_QUESTIONS = [
    "1️⃣ Какая твоя главная цель в inCruises на ближайшие 30 дней?",
    "2️⃣ Какой у тебя опыт в MLM или прямых продажах?",
    "3️⃣ Сколько времени в неделю готов уделять развитию?",
]

@router.callback_query(F.data.startswith("newbie:"))
async def process_role_choice(callback: CallbackQuery, state: FSMContext) -> None:
    role = callback.data.split(":")[1]
    await state.update_data(role=role)
    
    if role == "navigator":
        await state.update_data(navigator_answers=[], navigator_step=0)
        await state.set_state(OnboardingState.navigator_q1)
        await callback.message.answer(NAVIGATOR_QUESTIONS[0])
        await callback.answer()
        return
    
    base_path = Path(__file__).resolve().parent.parent
    
    if role == "tourist":
        file_path = base_path / "documents" / "341RU_NOBODY_CRUISES_BETTER.pdf"
        welcome_msg = "🏖️ Отличный выбор! Я помогу разобраться с клубными привилегиями и круизами. Обязательно спроси про «Как перейти в Партнеры и экономить 100%»!\n\nЗадай любой вопрос о членстве, круизах или переходе в Партнеры:"
    else:
        file_path = base_path / "marketing" / "маркетинг.pdf"
        welcome_msg = "💼 Приветствую, будущий Лидер! Я помогу тебе освоить бизнес-модель inCruises и выйти на доход.\n\nЗадай любой вопрос про маркетинг-план, ранги или первые шаги:"

    content = read_pdf_content(file_path)
    if role == "tourist":
        content += "\n\n[ОБЯЗАТЕЛЬНЫЙ РАЗДЕЛ] Как перейти в Партнеры и экономить 100%: Партнёрское членство позволяет получать скидки и бонусы, экономить до 100% на круизах за счёт накопленных баллов и реферальных вознаграждений. Переход из Туриста в Партнера — бесплатный, требуется только регистрация как партнёр в личном кабинете."
    await state.update_data(file_content=content[:30000])
    
    await callback.message.answer(welcome_msg)
    await state.set_state(OnboardingState.chatting)
    await callback.answer()

@router.message(OnboardingState.navigator_q1)
async def navigator_answer_1(message: Message, state: FSMContext) -> None:
    await state.update_data(nav_a1=message.text)
    await state.set_state(OnboardingState.navigator_q2)
    await message.answer(NAVIGATOR_QUESTIONS[1])


@router.message(OnboardingState.navigator_q2)
async def navigator_answer_2(message: Message, state: FSMContext) -> None:
    await state.update_data(nav_a2=message.text)
    await state.set_state(OnboardingState.navigator_q3)
    await message.answer(NAVIGATOR_QUESTIONS[2])


@router.message(OnboardingState.navigator_q3)
async def navigator_answer_3(message: Message, state: FSMContext) -> None:
    uid = message.from_user.id
    await state.update_data(nav_a3=message.text)
    await state.set_state(OnboardingState.choosing_role)
    status = await message.answer("⏳ Составляю твой план на 30 дней...")
    
    data = await state.get_data()
    a1 = data.get("nav_a1", "")
    a2 = data.get("nav_a2", "")
    a3 = data.get("nav_a3", "")
    
    system_prompt = "Ты — топ-лидер InCruises. На основе ответов пользователя составь краткий, вдохновляющий план действий на первые 30 дней. Структурируй по неделям, добавь конкретные шаги и мотивацию."
    prompt = f"Ответы пользователя:\n1. Главная цель: {a1}\n2. Опыт: {a2}\n3. Время в неделю: {a3}\n\nСоставь персональный план на 30 дней."
    
    result = await generate_text(
        prompt=prompt,
        system_instruction=system_prompt,
        task_type="onboarding_navigator",
        user_id=uid,
    )
    
    try:
        await status.edit_text(result, parse_mode=None)
    except Exception:
        await message.answer(result, parse_mode=None)
    
    if uid != ADMIN_ID and not result.startswith("⚠️"):
        db.add_user_coins_admin(uid, -1)
        coins = db.get_user_coins(uid)
        await message.answer(f"⚡️ Списано 1 InCoin. Остаток: {coins} 🪙")
    await state.clear()


@router.message(OnboardingState.chatting)
async def onboarding_chat(message: Message, state: FSMContext) -> None:
    uid = message.from_user.id
    data = await state.get_data()
    role = data.get("role")
    file_content = data.get("file_content", "")

    if role == "tourist":
        system_prompt = (
            f"Ты — заботливый консультант InCruises. Твоя цель — рассказать о выгодах путешествий, круизах и экономии. "
            f"Опирайся СТРОГО на этот документ: {file_content}. "
            f"Отвечай дружелюбно, не предлагай строить бизнес, если не спросят."
        )
    else:
        system_prompt = (
            f"Ты — топ-лидер и бизнес-тренер InCruises. Твоя цель — погрузить новичка в бизнес, "
            f"рассказать про маркетинг-план, лидерство и пассивный доход. "
            f"Опирайся СТРОГО на этот документ: {file_content}. "
            f"Мотивируй на действия."
        )

    status = await message.answer(t(uid, "ob_thinking"))

    result = await generate_text(
        prompt=message.text,
        system_instruction=system_prompt,
        task_type="onboarding_chat",
        user_id=uid,
    )

    MAX_TG_LEN = 4096
    if len(result) <= MAX_TG_LEN:
        try:
            await status.edit_text(result, parse_mode=None)
        except Exception:
            await message.answer(result, parse_mode=None)
    else:
        try:
            await status.delete()
        except Exception:
            pass
        for i in range(0, len(result), MAX_TG_LEN):
            chunk = result[i : i + MAX_TG_LEN]
            await message.answer(chunk, parse_mode=None)
