import json
import logging
import os
import re
from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config.i18n import TEXTS
from services import db
from services.ai_service import generate_text, format_admin_footer
from services.language import t
from services.scheduler import send_reminder

logger = logging.getLogger(__name__)
ADMIN_ID = int(os.getenv("ADMIN_ID", "5925660014"))
router = Router()

_ALL_CRM_BUTTONS = {
    texts["btn_crm"] for texts in TEXTS.values() if "btn_crm" in texts
}

PARSER_SYSTEM_PROMPT = (
    "Текущее время сервера: {now}.\n"
    "Пользователь напишет задачу с указанием времени.\n"
    "Извлеки суть задачи и точную дату/время срабатывания.\n"
    'Верни СТРОГО валидный JSON: {{"datetime": "YYYY-MM-DD HH:MM:SS", "task": "суть задачи"}}.\n'
    "Никакого лишнего текста, никакого markdown — только JSON."
)


class CRMState(StatesGroup):
    waiting_for_task = State()


def _build_crm_menu(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=t(user_id, "crm_add_reminder"),
        callback_data="crm:add",
    )
    builder.button(
        text=t(user_id, "crm_list_reminders"),
        callback_data="crm:list",
    )
    builder.button(text=t(user_id, "btn_back_menu"), callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


# ── Entry point ────────────────────────────────────────────────────────────

@router.callback_query(F.data == "menu:crm")
async def menu_crm(callback: CallbackQuery, state: FSMContext) -> None:
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
        t(uid, "crm_title"),
        reply_markup=_build_crm_menu(uid),
        parse_mode=None,
    )


@router.message(F.text.func(lambda text: text in _ALL_CRM_BUTTONS))
async def crm_menu(message: Message, state: FSMContext) -> None:
    uid = message.from_user.id
    if uid != ADMIN_ID:
        coins = db.get_user_coins(uid)
        if coins < 1:
            await message.answer(t(uid, "paywall_text"), parse_mode="HTML")
            return
    await state.clear()
    await message.answer(
        t(uid, "crm_title"),
        reply_markup=_build_crm_menu(uid),
        parse_mode=None,
    )


# ── Add reminder flow ─────────────────────────────────────────────────────

@router.callback_query(F.data == "crm:add")
async def crm_add_start(callback: CallbackQuery, state: FSMContext) -> None:
    uid = callback.from_user.id
    await callback.answer()
    await callback.message.answer(
        t(uid, "crm_ask_task"),
        parse_mode=None,
    )
    await state.set_state(CRMState.waiting_for_task)


@router.message(CRMState.waiting_for_task)
async def crm_process_task(message: Message, state: FSMContext) -> None:
    uid = message.from_user.id
    await state.clear()

    status = await message.answer(t(uid, "crm_thinking"))

    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    system_prompt = PARSER_SYSTEM_PROMPT.format(now=now_str)
    gen = await generate_text(
        prompt=message.text,
        system_instruction=system_prompt,
        task_type="crm",
        user_id=uid,
    )
    raw = gen.text

    parsed = _parse_ai_response(raw, now)
    if parsed is None:
        try:
            await status.edit_text(t(uid, "crm_parse_error"), parse_mode=None)
        except Exception:
            await message.answer(t(uid, "crm_parse_error"), parse_mode=None)
        return

    run_date, task_text = parsed

    if run_date <= now + timedelta(seconds=10):
        try:
            await status.edit_text(t(uid, "crm_past_date"), parse_mode=None)
        except Exception:
            await message.answer(t(uid, "crm_past_date"), parse_mode=None)
        return

    run_at_str = run_date.strftime("%Y-%m-%d %H:%M:%S")
    db.add_crm_reminder(uid, run_at_str, task_text)
    db.add_user_coins_admin(uid, -1)

    formatted_dt = run_date.strftime("%d.%m.%Y в %H:%M")
    confirm = t(uid, "crm_confirmed", task=task_text, dt=formatted_dt) + format_admin_footer(gen, uid)
    try:
        await status.edit_text(confirm, parse_mode=None)
    except Exception:
        await message.answer(confirm, parse_mode=None)


# ── List active reminders ─────────────────────────────────────────────────

@router.callback_query(F.data == "crm:list")
async def crm_list_reminders(callback: CallbackQuery) -> None:
    uid = callback.from_user.id
    await callback.answer()

    reminders = db.get_user_crm_reminders(uid)

    if not reminders:
        await callback.message.answer(
            t(uid, "crm_no_reminders"),
            parse_mode=None,
        )
        return

    lines = [t(uid, "crm_list_header")]
    for i, r in enumerate(reminders, 1):
        run_at = r.get("run_at", "")
        task_text = r.get("task_text", "—")
        try:
            dt_obj = datetime.strptime(run_at, "%Y-%m-%d %H:%M:%S")
            dt_str = dt_obj.strftime("%d.%m.%Y %H:%M")
        except ValueError:
            dt_str = run_at
        lines.append(f"  {i}. {dt_str} — {task_text}")

    await callback.message.answer("\n".join(lines), parse_mode=None)


# ── AI response parser ────────────────────────────────────────────────────

def _parse_ai_response(raw: str, now: datetime) -> tuple[datetime, str] | None:
    if raw.startswith("❌"):
        return None

    cleaned = raw.strip()
    json_match = re.search(r"\{.*}", cleaned, re.DOTALL)
    if not json_match:
        return None

    try:
        data = json.loads(json_match.group())
    except json.JSONDecodeError:
        return None

    dt_str = data.get("datetime")
    task = data.get("task")
    if not dt_str or not task:
        return None

    try:
        parsed_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            parsed_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return None

    return parsed_dt, task
