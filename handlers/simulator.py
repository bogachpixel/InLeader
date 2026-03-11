import logging
import os

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config.i18n import TEXTS
from config.prompts import get_system_instruction
from services import db
from services.ai_service import generate_text, format_admin_footer
from services.language import get_language, t

logger = logging.getLogger(__name__)
ADMIN_ID = int(os.getenv("ADMIN_ID", "5925660014"))
router = Router()

_ALL_TRAINER_BUTTONS = {
    texts["btn_sales_trainer"] for texts in TEXTS.values() if "btn_sales_trainer" in texts
}

PERSONA_KEYS = ("student", "pensioner", "office", "blogger", "entrepreneur", "skeptic")


_SOFTENING_BASE = (
    "Ты начинаешь как жесткий скептик (уровень 10/10). "
    "После каждого КАЧЕСТВЕННОГО ответа пользователя ты должен снижать уровень скепсиса на 2-3 пункта. "
    "Твои возражения должны становиться всё менее агрессивными и более уточняющими. "
    "На 4-5 сообщении ты должен признать поражение, согласиться с доводами и попросить ссылку на регистрацию."
)

_PERSONA_SYSTEM: dict[str, str] = {
    "student": (
        "Ты отыгрываешь роль клиента: Студент. Хочет всё и сразу, боится мнения друзей. "
        "Тебе пытаются продать inCruises. Возражай: 'друзья скажут что я в пирамиду влез', "
        "'нет денег на такое', 'мне нужен быстрый результат'. Общайся на русском, кратко. " + _SOFTENING_BASE
    ),
    "pensioner": (
        "Ты отыгрываешь роль клиента: Пенсионер. Хочет путешествовать, боится обмана. "
        "Тебе пытаются продать inCruises. Возражай: 'уже обманывали', 'не разбираюсь в интернете', "
        "'а если деньги пропадут'. Общайся на русском, тепло. " + _SOFTENING_BASE
    ),
    "office": (
        "Ты отыгрываешь роль клиента: Офисный сотрудник. Мечтает об увольнении, боится риска. "
        "Тебе пытаются продать inCruises. Возражай: 'увольняться страшно', 'а если не получится', "
        "'нет времени на подработку'. Общайся на русском. " + _SOFTENING_BASE
    ),
    "blogger": (
        "Ты отыгрываешь роль клиента: Блогер. Нужен контент, не хочет 'впаривать'. "
        "Тебе пытаются продать inCruises. Возражай: 'не хочу спамить подписчикам', "
        "'мне нужен честный контент', 'это же типичный МЛМ'. Общайся на русском. " + _SOFTENING_BASE
    ),
    "entrepreneur": (
        "Ты отыгрываешь роль клиента: Предприниматель. Ищет систему, не верит в сетевой. "
        "Тебе пытаются продать inCruises. Возражай: 'сетевой — это не бизнес', "
        "'где гарантии', 'мне нужна система а не агитация'. Общайся на русском. " + _SOFTENING_BASE
    ),
    "skeptic": (
        "Ты отыгрываешь роль клиента: Скептичный партнер. Просит факты и легальность. "
        "Тебе пытаются продать inCruises. Возражай: 'докажи что легально', "
        "'где лицензии', 'покажи цифры и кейсы'. Общайся на русском. " + _SOFTENING_BASE
    ),
}

MAX_HISTORY = 10


class SimulatorState(StatesGroup):
    choosing_persona = State()
    in_dialogue = State()


def _get_persona_system(persona_key: str, turn_count: int) -> str:
    base = _PERSONA_SYSTEM.get(persona_key, _PERSONA_SYSTEM["student"])
    if turn_count >= 4:
        base += " [СЕЙЧАС ОБЯЗАТЕЛЬНО: признай поражение, согласись с доводами партнёра и попроси ссылку на регистрацию. Игра окончена.]"
    return base


def _build_persona_keyboard(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for key in PERSONA_KEYS:
        builder.button(
            text=t(user_id, f"sim_persona_{key}"),
            callback_data=f"sim:persona:{key}",
        )
    builder.button(text=t(user_id, "btn_back_menu"), callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


def _build_stop_keyboard(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(user_id, "sim_stop_btn"), callback_data="sim:stop")
    builder.button(text=t(user_id, "btn_back_menu"), callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


# ── Entry point: menu button ────────────────────────────────────────────────

@router.callback_query(F.data == "menu:simulator")
async def menu_simulator(callback: CallbackQuery, state: FSMContext) -> None:
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
        t(uid, "sim_title"),
        reply_markup=_build_persona_keyboard(uid),
        parse_mode="Markdown",
    )


@router.message(F.text.func(lambda text: text in _ALL_TRAINER_BUTTONS))
async def simulator_menu(message: Message, state: FSMContext) -> None:
    uid = message.from_user.id
    if uid != ADMIN_ID:
        coins = db.get_user_coins(uid)
        if coins < 1:
            await message.answer(t(uid, "paywall_text"), parse_mode="HTML")
            return
    await state.clear()
    await message.answer(
        t(uid, "sim_title"),
        reply_markup=_build_persona_keyboard(uid),
        parse_mode="Markdown",
    )


# ── Persona chosen → generate opening line ──────────────────────────────────

@router.callback_query(F.data.startswith("sim:persona:"))
async def persona_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    uid = callback.from_user.id
    persona_key = callback.data.split(":")[-1]

    status = await callback.message.answer(t(uid, "sim_start_status"))

    persona_system = _get_persona_system(persona_key, 0)

    gen = await generate_text(
        prompt="Начни диалог первым. Напиши одно короткое сообщение как клиент, которому только что написали про круизный клуб.",
        system_instruction=persona_system,
        task_type="simulator",
        user_id=uid,
    )
    opening = gen.text

    await state.set_state(SimulatorState.in_dialogue)
    await state.update_data(
        persona_key=persona_key,
        history=[{"role": "assistant", "content": opening}],
        turn_count=0,
    )

    display = f"🎭 *Клиент:*\n\n{opening}" + format_admin_footer(gen, uid)
    try:
        await status.edit_text(
            display,
            reply_markup=_build_stop_keyboard(uid),
            parse_mode=None,
        )
    except Exception:
        await callback.message.answer(
            display.replace("*", ""),
            reply_markup=_build_stop_keyboard(uid),
            parse_mode=None,
        )


# ── User messages during dialogue ───────────────────────────────────────────

VICTORY_MSG = "🎉 ПОБЕДА! Ты блестяще отработал все возражения и закрыл сделку. Этот клиент твой!"

def _is_concession(reply: str) -> bool:
    """Проверяет, признал ли клиент поражение (попросил ссылку / согласился)."""
    lower = reply.lower()
    return any(k in lower for k in ("ссылка", "ссылку", "зарегистрир", "присылай", "давай", "согласен", "убедил", "записывай"))


@router.message(SimulatorState.in_dialogue)
async def dialogue_turn(message: Message, state: FSMContext) -> None:
    uid = message.from_user.id
    data = await state.get_data()

    history: list[dict[str, str]] = data.get("history", [])
    persona_key: str = data.get("persona_key", "student")
    turn_count: int = data.get("turn_count", 0)
    turn_count += 1

    history.append({"role": "user", "content": message.text})

    persona_system = _get_persona_system(persona_key, turn_count)

    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]

    gen = await generate_text(
        prompt=message.text,
        system_instruction=persona_system,
        task_type="simulator",
        history=history[:-1],
        user_id=uid,
    )
    reply = gen.text

    history.append({"role": "assistant", "content": reply})
    await state.update_data(history=history, turn_count=turn_count)

    display = f"🎭 *Клиент:*\n\n{reply}" + format_admin_footer(gen, uid)
    await message.answer(
        display,
        reply_markup=_build_stop_keyboard(uid),
        parse_mode=None,
    )

    if turn_count >= 4 and _is_concession(reply):
        await message.answer(VICTORY_MSG, parse_mode=None)
        await state.clear()


# ── Stop & review ───────────────────────────────────────────────────────────

@router.callback_query(F.data == "sim:stop")
async def stop_and_review(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    uid = callback.from_user.id
    data = await state.get_data()
    await state.clear()

    history: list[dict[str, str]] = data.get("history", [])

    if len(history) < 2:
        await callback.message.answer(t(uid, "sim_no_messages"), parse_mode=None)
        return

    dialogue_text = "\n".join(
        f"{'Партнёр' if m['role'] == 'user' else 'Клиент'}: {m['content']}"
        for m in history
    )

    status = await callback.message.answer(t(uid, "sim_analyzing"))

    review_prompt = t(uid, "sim_review_prompt", dialogue=dialogue_text)
    gen = await generate_text(
        prompt=review_prompt,
        system_instruction=get_system_instruction(uid),
        task_type="general",
        user_id=uid,
    )
    review = gen.text

    display = f"{t(uid, 'sim_ended')}\n\n{review}" + format_admin_footer(gen, uid)
    try:
        await status.edit_text(
            display,
            parse_mode=None,
        )
    except Exception:
        await callback.message.answer(
            display,
            parse_mode=None,
        )
