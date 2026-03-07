import asyncio
import json
import logging
import os
import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile, CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config.i18n import TEXTS
from config.knowledge_base import INSIDER_DISCOUNT_PCT, MAX_RP_COVERAGE_PCT, RP_VALUE_USD
from services import db
from services.ai_service import generate_text
from services.image_gen import (
    generate_tourist_receipt,
    generate_cruise_receipt,
    generate_conversion_receipt,
)
from services.language import get_language, t

logger = logging.getLogger(__name__)
ADMIN_ID = int(os.getenv("ADMIN_ID", "5925660014"))
router = Router()

_ALL_CALC_BUTTONS = {
    texts["btn_calc"] for texts in TEXTS.values() if "btn_calc" in texts
}

MONTHLY_CONTRIBUTION = 100
REWARD_POINTS_PER_MONTH = 200


class TouristCalcState(StatesGroup):
    waiting_for_months = State()


class CruiseCalcState(StatesGroup):
    waiting_for_price = State()
    waiting_for_rp = State()


class ConversionCalcState(StatesGroup):
    waiting_for_cruise_data = State()


CONVERSION_JSON_PROMPT = (
    "Пользователь описывает стоимость круиза и сборов. "
    "Твоя задача — извлечь цифры. "
    'Верни СТРОГО валидный JSON в формате: {"price": 3500, "fees": 350}. '
    'Если сборы не указаны, передай в "fees" 0. '
    "Никакого текста, только JSON."
)


def _build_calc_menu(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(user_id, "calc_tourist_btn"), callback_data="calc:tourist")
    builder.button(text=t(user_id, "calc_cruise_btn"), callback_data="calc:cruise")
    builder.button(text=t(user_id, "calc_conversion_btn"), callback_data="calc:conversion")
    builder.button(text=t(user_id, "calc_free_member"), callback_data="calc:free")
    builder.button(text=t(user_id, "btn_back_menu"), callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


@router.callback_query(F.data == "menu:calc")
async def menu_calc(callback: CallbackQuery, state: FSMContext) -> None:
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
        t(uid, "calc_title"),
        reply_markup=_build_calc_menu(uid),
        parse_mode="Markdown",
    )


@router.message(F.text.func(lambda text: text in _ALL_CALC_BUTTONS))
async def calc_menu(message: Message, state: FSMContext) -> None:
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
    await message.answer(
        t(uid, "calc_title"),
        reply_markup=_build_calc_menu(uid),
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "calc:free")
async def calc_free_info(callback: CallbackQuery):
    uid = callback.from_user.id
    await callback.message.answer(t(uid, "calc_free_member_text"))
    await callback.answer()


# ── Tourist Calculator ───────────────────────────────────────────

@router.callback_query(F.data == "calc:tourist")
async def tourist_start(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.answer(
        t(callback.from_user.id, "calc_tourist_ask"),
        parse_mode=None,
    )
    await state.set_state(TouristCalcState.waiting_for_months)


@router.message(TouristCalcState.waiting_for_months)
async def tourist_result(message: Message, state: FSMContext) -> None:
    uid = message.from_user.id
    await state.clear()

    text = message.text.strip()
    if not text.isdigit() or int(text) <= 0:
        await message.answer(t(uid, "calc_bad_number"), parse_mode=None)
        return

    months = int(text)
    if months > 120:
        months = 120

    total_paid = months * MONTHLY_CONTRIBUTION
    total_points = months * REWARD_POINTS_PER_MONTH

    lines = [t(uid, "calc_tourist_header")]
    lines.append("")

    running_paid = 0
    running_points = 0
    for m in range(1, months + 1):
        running_paid += MONTHLY_CONTRIBUTION
        running_points += REWARD_POINTS_PER_MONTH
        lines.append(
            t(uid, "calc_tourist_row",
              month=str(m),
              paid=f"${running_paid}",
              points=str(running_points))
        )

    lines.append("")
    lines.append(
        t(uid, "calc_tourist_total",
          total_paid=f"${total_paid}",
          total_points=str(total_points))
    )
    lines.append("")
    lines.append(t(uid, "calc_tourist_tip"))

    await message.answer("\n".join(lines), parse_mode=None)

    try:
        lang = get_language(uid)
        img_bytes = await asyncio.to_thread(
            generate_tourist_receipt, months, total_paid, total_points, lang,
        )
        await message.answer_photo(
            BufferedInputFile(img_bytes, filename="tourist_receipt.png"),
            caption=t(uid, "calc_image_caption"),
        )
    except Exception as e:
        logger.error("Failed to generate tourist receipt image: %s", e)


# ── Cruise ББ Calculator ─────────────────────────────────────────

@router.callback_query(F.data == "calc:cruise")
async def cruise_start(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.answer(
        t(callback.from_user.id, "calc_cruise_ask_price"),
        parse_mode=None,
    )
    await state.set_state(CruiseCalcState.waiting_for_price)


@router.message(CruiseCalcState.waiting_for_price)
async def cruise_ask_rp(message: Message, state: FSMContext) -> None:
    uid = message.from_user.id
    raw = message.text.strip().replace(",", ".").replace(" ", "")

    try:
        price = float(raw)
        if price <= 0:
            raise ValueError
    except ValueError:
        await message.answer(t(uid, "calc_bad_number"), parse_mode=None)
        return

    await state.update_data(cruise_price=price)
    await message.answer(t(uid, "calc_cruise_ask_rp"), parse_mode=None)
    await state.set_state(CruiseCalcState.waiting_for_rp)


@router.message(CruiseCalcState.waiting_for_rp)
async def cruise_result(message: Message, state: FSMContext) -> None:
    uid = message.from_user.id
    raw = message.text.strip().replace(" ", "")

    try:
        user_rp = int(raw)
        if user_rp < 0:
            raise ValueError
    except ValueError:
        await state.clear()
        await message.answer(t(uid, "calc_bad_number"), parse_mode=None)
        return

    data = await state.get_data()
    await state.clear()

    cruise_price: float = data.get("cruise_price", 0.0)

    # INsider Pricing: -17% of listed price
    insider_price = cruise_price * (1 - INSIDER_DISCOUNT_PCT / 100)
    insider_save = cruise_price - insider_price

    # RP can cover up to MAX_RP_COVERAGE_PCT (50%) of listed price
    max_rp_cover = cruise_price * (MAX_RP_COVERAGE_PCT / 100)
    rp_usable = min(user_rp * RP_VALUE_USD, max_rp_cover)
    rp_used_points = int(rp_usable / RP_VALUE_USD)
    cash_needed = cruise_price - rp_usable
    total_savings = rp_usable
    covers_full_50 = (user_rp * RP_VALUE_USD) >= max_rp_cover

    def fmt(val: float) -> str:
        return f"{val:,.2f}"

    lines = [t(uid, "calc_cruise_header"), ""]
    lines.append(t(uid, "calc_cruise_listed", price=fmt(cruise_price)))
    lines.append(t(uid, "calc_cruise_insider",
                   price=fmt(insider_price),
                   save=fmt(insider_save)))
    lines.append("")
    lines.append(t(uid, "calc_cruise_rp_avail",
                   rp=str(user_rp),
                   value=fmt(user_rp * RP_VALUE_USD)))

    if covers_full_50:
        lines.append(t(uid, "calc_cruise_rp_usable",
                       rp=str(rp_used_points),
                       value=fmt(rp_usable)))
    else:
        lines.append(t(uid, "calc_cruise_rp_not_enough",
                       rp=str(user_rp)))

    lines.append(t(uid, "calc_cruise_cash", cash=fmt(cash_needed)))
    lines.append(t(uid, "calc_cruise_savings", save=fmt(total_savings)))
    lines.append("")
    lines.append(t(uid, "calc_cruise_booking_tip"))
    lines.append("")
    lines.append(t(uid, "calc_cruise_partner_tip"))

    await message.answer("\n".join(lines), parse_mode=None)

    try:
        lang = get_language(uid)
        img_bytes = await asyncio.to_thread(
            generate_cruise_receipt,
            cruise_price, rp_used_points, cash_needed, total_savings, lang,
        )
        await message.answer_photo(
            BufferedInputFile(img_bytes, filename="cruise_receipt.png"),
            caption=t(uid, "calc_image_caption"),
        )
    except Exception as e:
        logger.error("Failed to generate cruise receipt image: %s", e)


# ── Conversion BB Calculator ───────────────────────────────────────

@router.callback_query(F.data == "calc:conversion")
async def conversion_start(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.answer(
        t(callback.from_user.id, "calc_conversion_ask"),
        parse_mode=None,
    )
    await state.set_state(ConversionCalcState.waiting_for_cruise_data)


@router.message(ConversionCalcState.waiting_for_cruise_data)
async def conversion_result(message: Message, state: FSMContext) -> None:
    uid = message.from_user.id
    await state.clear()

    status = await message.answer("⏳ Извлекаю цифры...", parse_mode=None)

    raw = await generate_text(
        prompt=message.text,
        system_instruction=CONVERSION_JSON_PROMPT,
        task_type="general",
        user_id=uid
    )

    parsed = None
    if not raw.startswith("❌"):
        match = re.search(r"\{[^{}]*\}", raw)
        if match:
            try:
                parsed = json.loads(match.group())
            except json.JSONDecodeError:
                pass

    if parsed is None:
        try:
            await status.edit_text(t(uid, "calc_conversion_parse_error"), parse_mode=None)
        except Exception:
            await message.answer(t(uid, "calc_conversion_parse_error"), parse_mode=None)
        return

    price = float(parsed.get("price", 0))
    fees = float(parsed.get("fees", 0))
    if fees == 0:
        fees = price * 0.10

    if price <= 0:
        try:
            await status.edit_text(t(uid, "calc_bad_number"), parse_mode=None)
        except Exception:
            await message.answer(t(uid, "calc_bad_number"), parse_mode=None)
        return

    standard_points = price / 2
    converted_points = standard_points * 2
    subtotal = standard_points + converted_points
    final_total = subtotal + fees

    receipt = t(
        uid,
        "calc_conversion_receipt",
        price=f"{price:,.0f}",
        standard_points=f"{standard_points:,.0f}",
        converted_points=f"{converted_points:,.0f}",
        subtotal=f"{subtotal:,.0f}",
        fees=f"{fees:,.0f}",
        final_total=f"{final_total:,.0f}",
    )

    try:
        await status.edit_text(receipt, parse_mode=None)
    except Exception:
        await message.answer(receipt, parse_mode=None)

    try:
        lang = get_language(uid)
        img_bytes = await asyncio.to_thread(
            generate_conversion_receipt,
            price, standard_points, converted_points, fees, final_total, lang,
        )
        await message.answer_photo(
            BufferedInputFile(img_bytes, filename="conversion_receipt.png"),
            caption=t(uid, "calc_image_caption"),
        )
    except Exception as e:
        logger.error("Failed to generate conversion receipt image: %s", e)
