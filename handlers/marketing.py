import logging
import os

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config.i18n import TEXTS
from config.knowledge_base import (
    FREE_MEMBERSHIP_FACTS_FOR_AI,
    get_rank_facts_for_ai,
    get_rewards_file_facts_for_ai,
    REWARDS_FACTS_FOR_AI,
)
from config.prompts import get_system_instruction
from services import db
from services.ai_service import generate_text, format_admin_footer
from services.language import t

logger = logging.getLogger(__name__)
ADMIN_ID = int(os.getenv("ADMIN_ID", "5925660014"))
router = Router()

_ALL_MARKETING_BUTTONS = {
    texts["btn_marketing"] for texts in TEXTS.values()
}


class MarketingState(StatesGroup):
    waiting_for_question = State()


def _build_marketing_keyboard(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(user_id, "mkt_ranks"), callback_data="marketing:ranks")
    builder.button(text=t(user_id, "mkt_rewards"), callback_data="marketing:rewards")
    builder.button(text=t(user_id, "mkt_free_membership"), callback_data="marketing:free_membership")
    builder.button(text=t(user_id, "mkt_ask_ai"), callback_data="marketing:ask_ai")
    builder.button(text=t(user_id, "btn_back_menu"), callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


@router.callback_query(F.data == "menu:marketing")
async def menu_marketing(callback: CallbackQuery) -> None:
    uid = callback.from_user.id
    if uid != ADMIN_ID:
        coins = db.get_user_coins(uid)
        if coins < 1:
            await callback.message.answer(t(uid, "paywall_text"), parse_mode="HTML")
            await callback.answer()
            return
    await callback.answer()
    await callback.message.answer(
        t(callback.from_user.id, "mkt_title"),
        reply_markup=_build_marketing_keyboard(callback.from_user.id),
        parse_mode="Markdown",
    )


@router.message(F.text.func(lambda text: text in _ALL_MARKETING_BUTTONS))
async def marketing_menu(message: Message) -> None:
    uid = message.from_user.id
    if uid != ADMIN_ID:
        coins = db.get_user_coins(uid)
        if coins < 1:
            await message.answer(t(uid, "paywall_text"), parse_mode="HTML")
            return
    await message.answer(
        t(uid, "mkt_title"),
        reply_markup=_build_marketing_keyboard(uid),
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "marketing:ranks")
async def marketing_ranks(callback: CallbackQuery) -> None:
    await callback.answer()
    uid = callback.from_user.id
    status = await callback.message.answer(t(uid, "mkt_thinking"))
    system = get_system_instruction(uid) + "\n\n" + get_rank_facts_for_ai()
    prompt = t(uid, "mkt_ranks_ai_prompt")
    gen = await generate_text(
        prompt=prompt,
        system_instruction=system,
        task_type="marketing",
        user_id=uid,
    )
    display = gen.text + format_admin_footer(gen, uid)
    try:
        await status.edit_text(display, parse_mode=None)
    except Exception as e:
        logger.error("Failed to edit marketing ranks message: %s", e)
        await callback.message.answer(display, parse_mode=None)


@router.callback_query(F.data == "marketing:rewards")
async def marketing_rewards(callback: CallbackQuery) -> None:
    await callback.answer()
    uid = callback.from_user.id
    status = await callback.message.answer(t(uid, "mkt_thinking"))
    system = get_system_instruction(uid) + "\n\n" + get_rewards_file_facts_for_ai()
    prompt = t(uid, "mkt_rewards_ai_prompt")
    gen = await generate_text(
        prompt=prompt,
        system_instruction=system,
        task_type="marketing",
        user_id=uid,
    )
    display = gen.text + format_admin_footer(gen, uid)
    try:
        await status.edit_text(display, parse_mode=None)
    except Exception as e:
        logger.error("Failed to edit rewards message: %s", e)
        await callback.message.answer(display, parse_mode=None)


@router.callback_query(F.data == "marketing:free_membership")
async def marketing_free_membership(callback: CallbackQuery) -> None:
    await callback.answer()
    uid = callback.from_user.id
    status = await callback.message.answer(t(uid, "mkt_thinking"))
    system = get_system_instruction(uid) + "\n\n" + FREE_MEMBERSHIP_FACTS_FOR_AI
    prompt = t(uid, "mkt_free_ai_prompt")
    gen = await generate_text(
        prompt=prompt,
        system_instruction=system,
        task_type="marketing",
        user_id=uid,
    )
    display = gen.text + format_admin_footer(gen, uid)
    try:
        await status.edit_text(display, parse_mode=None)
    except Exception as e:
        logger.error("Failed to edit free membership message: %s", e)
        await callback.message.answer(display, parse_mode=None)


@router.callback_query(F.data == "marketing:ask_ai")
async def marketing_ask_ai(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.answer(
        t(callback.from_user.id, "mkt_ask_prompt"),
        parse_mode=None,
    )
    await state.set_state(MarketingState.waiting_for_question)


@router.message(MarketingState.waiting_for_question)
async def marketing_ai_answer(message: Message, state: FSMContext) -> None:
    uid = message.from_user.id
    await state.clear()

    status_message = await message.answer(t(uid, "mkt_thinking"))

    prompt = t(uid, "mkt_ai_prompt", question=message.text)
    system = get_system_instruction(uid) + "\n\n" + REWARDS_FACTS_FOR_AI
    gen = await generate_text(
        prompt=prompt,
        system_instruction=system,
        task_type="marketing",
        user_id=uid,
    )

    display = gen.text + format_admin_footer(gen, uid)
    try:
        await status_message.edit_text(display, parse_mode=None)
    except Exception as e:
        logger.error("Failed to edit status message: %s", e)
        await message.answer(display, parse_mode=None)
