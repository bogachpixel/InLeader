"""
Работа в аккаунте — 2FA настройка, Политика.
"""

import logging
from pathlib import Path

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile, CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config.i18n import TEXTS
from config.knowledge_base import get_2fa_steps_and_facts, get_policy_facts_for_ai
from config.prompts import get_system_instruction
from services.ai_service import generate_text
from services.language import t

logger = logging.getLogger(__name__)

router = Router()

_ALL_ACCOUNT_BUTTONS = {
    texts.get("btn_account", texts.get("btn_media", "Работа в аккаунте"))
    for texts in TEXTS.values()
}


class TwoFAState(StatesGroup):
    step = State()


class PolicyState(StatesGroup):
    chat = State()


def _build_account_keyboard(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(user_id, "account_2fa"), callback_data="account:2fa_start")
    builder.button(text=t(user_id, "account_policy"), callback_data="account:policy")
    builder.button(text=t(user_id, "btn_back_menu"), callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


def _build_policy_keyboard(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(user_id, "account_btn_back_account"), callback_data="account:policy_back")
    builder.adjust(1)
    return builder.as_markup()


def _build_2fa_confirm_keyboard(step_index: int, total: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if step_index < total - 1:
        builder.button(text="✅ Выполнил, к следующему шагу", callback_data=f"account:2fa_next:{step_index}")
    else:
        builder.button(text="✅ Готово! Завершить", callback_data=f"account:2fa_done:{step_index}")
    return builder.as_markup()


def _build_2fa_start_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🚀 Начать настройку 2FA", callback_data="account:2fa_step:0")
    return builder.as_markup()


@router.callback_query(F.data == "menu:media")
@router.callback_query(F.data == "menu:account")
async def menu_account(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.clear()
    uid = callback.from_user.id
    title = t(uid, "account_title")
    await callback.message.answer(
        title,
        reply_markup=_build_account_keyboard(uid),
        parse_mode=None,
    )


@router.message(F.text.func(lambda text: text in _ALL_ACCOUNT_BUTTONS))
async def account_menu(message: Message) -> None:
    uid = message.from_user.id
    await message.answer(
        t(uid, "account_title"),
        reply_markup=_build_account_keyboard(uid),
        parse_mode=None,
    )


@router.callback_query(F.data == "account:2fa_start")
async def account_2fa_start(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    uid = callback.from_user.id
    steps, raw = get_2fa_steps_and_facts()
    if not steps:
        await callback.message.answer(
            t(uid, "account_2fa_no_file"),
            parse_mode=None,
        )
        return
    await state.update_data(twofa_steps=steps, twofa_current=0)
    intro = t(uid, "account_2fa_intro")
    await callback.message.answer(
        intro,
        reply_markup=_build_2fa_start_keyboard(),
        parse_mode=None,
    )


@router.callback_query(F.data.startswith("account:2fa_step:"))
@router.callback_query(F.data.startswith("account:2fa_next:"))
async def account_2fa_show_step(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    uid = callback.from_user.id
    data = await state.get_data()
    steps: list = data.get("twofa_steps", [])
    if not steps:
        await callback.message.answer(t(uid, "account_2fa_no_file"), parse_mode=None)
        await state.clear()
        return
    idx = int(callback.data.split(":")[-1])
    if "next" in callback.data:
        idx += 1
    if idx >= len(steps):
        await state.clear()
        return
    step = steps[idx]
    total = len(steps)
    caption = f"🔐 {step['title']} из {total}\n\n{step['text']}"
    kb = _build_2fa_confirm_keyboard(idx, total)
    if step.get("image_path") and Path(step["image_path"]).exists():
        try:
            photo = BufferedInputFile(Path(step["image_path"]).read_bytes(), filename="step.png")
            await callback.message.answer_photo(photo=photo, caption=caption, reply_markup=kb, parse_mode=None)
        except Exception as e:
            logger.warning("2FA step image failed: %s", e)
            await callback.message.answer(caption, reply_markup=kb, parse_mode=None)
    else:
        await callback.message.answer(caption, reply_markup=kb, parse_mode=None)
    await state.update_data(twofa_current=idx)


@router.callback_query(F.data.startswith("account:2fa_done:"))
async def account_2fa_done(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    uid = callback.from_user.id
    await state.clear()
    congrats = t(uid, "account_2fa_congrats")
    await callback.message.answer(congrats, parse_mode=None)


# ─── Политика (Lama + файл политика) ─────────────────────────────────────────


@router.callback_query(F.data == "account:policy")
async def account_policy_start(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    uid = callback.from_user.id
    facts = get_policy_facts_for_ai()
    if "не найден" in facts.lower():
        await callback.message.answer(t(uid, "account_policy_no_file"), parse_mode=None)
        return
    await state.set_state(PolicyState.chat)
    status = await callback.message.answer(t(uid, "account_policy_thinking"), parse_mode=None)
    system = get_system_instruction(uid) + "\n\n" + facts + "\n\n" + t(uid, "account_policy_system")
    prompt = t(uid, "account_policy_intro_prompt")
    result = await generate_text(
        prompt=prompt,
        system_instruction=system,
        task_type="general",
    )
    try:
        await status.edit_text(
            result + "\n\n" + t(uid, "account_policy_ask"),
            reply_markup=_build_policy_keyboard(uid),
            parse_mode=None,
        )
    except Exception as e:
        logger.error("policy intro: %s", e)
        await callback.message.answer(
            result + "\n\n" + t(uid, "account_policy_ask"),
            reply_markup=_build_policy_keyboard(uid),
            parse_mode=None,
        )


@router.callback_query(F.data == "account:policy_back")
async def account_policy_back(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.clear()
    uid = callback.from_user.id
    await callback.message.answer(
        t(uid, "account_title"),
        reply_markup=_build_account_keyboard(uid),
        parse_mode=None,
    )


@router.message(PolicyState.chat, F.text)
async def account_policy_chat(message: Message, state: FSMContext) -> None:
    uid = message.from_user.id
    facts = get_policy_facts_for_ai()
    if "не найден" in facts.lower():
        await state.clear()
        await message.answer(t(uid, "account_policy_no_file"), parse_mode=None)
        return
    status = await message.answer(t(uid, "account_policy_thinking"), parse_mode=None)
    system = get_system_instruction(uid) + "\n\n" + facts + "\n\n" + t(uid, "account_policy_system")
    prompt = t(uid, "account_policy_user_prompt", question=message.text)
    result = await generate_text(
        prompt=prompt,
        system_instruction=system,
        task_type="general",
    )
    try:
        await status.edit_text(
            result,
            reply_markup=_build_policy_keyboard(uid),
            parse_mode=None,
        )
    except Exception as e:
        logger.error("policy chat: %s", e)
        await message.answer(
            result,
            reply_markup=_build_policy_keyboard(uid),
            parse_mode=None,
        )
