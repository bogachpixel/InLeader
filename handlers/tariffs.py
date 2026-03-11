"""
Тарифы InCoins: генерация платёжных ссылок FreeKassa.
"""

import logging
import os
import time
from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from services.db import add_user, create_payment_order
from services.freekassa import generate_payment_link
from services.language import t

router = Router()
logger = logging.getLogger(__name__)

ADMIN_ID = int(os.getenv("ADMIN_ID", "5925660014"))

# (coins, amount_rub, label_key)
TARIFFS = [
    (50, 75, "tariff_trial"),
    (500, 600, "tariff_standard"),
    (1000, 1000, "tariff_leader"),
]


def _build_tariffs_kb(user_id: int) -> InlineKeyboardMarkup:
    kb = []
    for coins, amount, label_key in TARIFFS:
        label = t(user_id, label_key)
        kb.append([
            InlineKeyboardButton(
                text=f"{label} ({coins} InCoins) — {amount} ₽",
                callback_data=f"tariff:{coins}:{amount}",
            )
        ])
    kb.append([InlineKeyboardButton(text=t(user_id, "btn_back"), callback_data="menu:main")])
    return InlineKeyboardMarkup(inline_keyboard=kb)


@router.callback_query(lambda c: c.data == "menu:tariffs")
async def menu_tariffs(callback: CallbackQuery):
    """Экран тарифов с тремя пакетами."""
    await callback.answer()
    uid = callback.from_user.id
    if uid == ADMIN_ID:
        await callback.message.edit_text(
            t(uid, "admin_free"),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=t(uid, "btn_back_menu"), callback_data="menu:main")]
            ]),
        )
        return

    desc = t(uid, "tariff_desc")
    text = t(uid, "tariff_title", desc=desc)
    await callback.message.edit_text(text, reply_markup=_build_tariffs_kb(uid), parse_mode="HTML")


@router.callback_query(lambda c: c.data and c.data.startswith("tariff:"))
async def tariff_chosen(callback: CallbackQuery):
    """Генерация платёжной ссылки для выбранного тарифа."""
    await callback.answer()
    uid = callback.from_user.id
    if uid == ADMIN_ID:
        return

    try:
        parts = callback.data.split(":")
        coins = int(parts[1])
        amount = int(parts[2])
    except (ValueError, IndexError):
        await callback.message.answer(t(uid, "tariff_error"))
        return

    label_key = next((x[2] for x in TARIFFS if x[0] == coins and x[1] == amount), "tariff_trial")
    label = t(uid, label_key)
    add_user(uid, callback.from_user.username, callback.from_user.full_name)
    order_id = f"pay_{uid}_{int(time.time() * 1000)}"
    create_payment_order(order_id, uid, float(amount), amount_coins=coins)

    url = generate_payment_link(order_id, float(amount))
    if not url:
        await callback.message.answer(t(uid, "balance_payment_error"))
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid, "btn_pay_amount", amount=amount), url=url)],
        [InlineKeyboardButton(text=t(uid, "btn_back"), callback_data="menu:tariffs")],
    ])
    await callback.message.edit_text(
        t(uid, "tariff_pay_text", label=label, coins=coins, amount=amount),
        reply_markup=kb,
        parse_mode="HTML",
    )
