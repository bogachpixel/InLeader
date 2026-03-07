"""
Раздел Документы — материалы для партнёров.
"""

import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config.i18n import TEXTS
from config.knowledge_base import get_cruise_protection_facts_for_ai
from config.prompts import get_system_instruction
from services.ai_service import generate_text
from services.language import t

logger = logging.getLogger(__name__)

router = Router()

_ALL_DOCS_BUTTONS = {
    texts["btn_documents"] for texts in TEXTS.values() if "btn_documents" in texts
}


def _build_documents_keyboard(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(user_id, "doc_cruise_protection"), callback_data="doc:cruise_protection")
    builder.button(text=t(user_id, "btn_back_menu"), callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


@router.callback_query(F.data == "menu:documents")
async def menu_documents(callback: CallbackQuery) -> None:
    await callback.answer()
    uid = callback.from_user.id
    await callback.message.answer(
        t(uid, "doc_title"),
        reply_markup=_build_documents_keyboard(uid),
        parse_mode="Markdown",
    )


@router.message(F.text.func(lambda text: text in _ALL_DOCS_BUTTONS))
async def documents_menu(message: Message) -> None:
    uid = message.from_user.id
    await message.answer(
        t(uid, "doc_title"),
        reply_markup=_build_documents_keyboard(uid),
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "doc:cruise_protection")
async def doc_cruise_protection(callback: CallbackQuery) -> None:
    await callback.answer()
    uid = callback.from_user.id
    status = await callback.message.answer(t(uid, "doc_thinking"))
    system = get_system_instruction(uid) + "\n\n" + get_cruise_protection_facts_for_ai()
    prompt = t(uid, "doc_cruise_protection_prompt")
    result = await generate_text(
        prompt=prompt,
        system_instruction=system,
        task_type="general",
    )
    try:
        await status.edit_text(result, parse_mode=None)
    except Exception as e:
        logger.error("doc cruise protection: %s", e)
        await callback.message.answer(result, parse_mode=None)
