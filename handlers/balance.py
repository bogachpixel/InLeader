"""
Пополнение баланса InCoins через FreeKassa.
"""

import logging
import os
import time
from aiogram import Router
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

from services.db import get_user_coins, create_payment_order, add_user
from services.freekassa import build_payment_url
from services.language import t

router = Router()
logger = logging.getLogger(__name__)

ADMIN_ID = int(os.getenv("ADMIN_ID", "5925660014"))

# Суммы для быстрого выбора (рубли)
AMOUNTS = [100, 250, 500, 1000, 2500, 5000]


def _build_amounts_kb(user_id: int) -> InlineKeyboardMarkup:
    kb = []
    row = []
    for a in AMOUNTS:
        row.append(InlineKeyboardButton(text=f"{a} ₽", callback_data=f"balance:topup:{a}"))
        if len(row) == 3:
            kb.append(row)
            row = []
    if row:
        kb.append(row)
    kb.append([InlineKeyboardButton(text=t(user_id, "btn_back"), callback_data="menu:main")])
    return InlineKeyboardMarkup(inline_keyboard=kb)


@router.callback_query(lambda c: c.data and c.data == "menu:balance")
async def menu_balance(callback: CallbackQuery):
    """Экран баланса с кнопкой пополнения."""
    await callback.answer()
    uid = callback.from_user.id
    if uid == ADMIN_ID:
        await callback.message.edit_text(
            "👑 Администратор пользуется ботом бесплатно.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=t(uid, "btn_back_menu"), callback_data="menu:main")]
            ]),
        )
        return

    coins = get_user_coins(uid)
    text = t(uid, "balance_screen", coins=coins)
    await callback.message.edit_text(text, reply_markup=_build_amounts_kb(uid), parse_mode="HTML")


@router.callback_query(lambda c: c.data and c.data.startswith("balance:topup:"))
async def balance_topup(callback: CallbackQuery):
    """Генерация платёжной ссылки и редирект."""
    await callback.answer()
    uid = callback.from_user.id
    if uid == ADMIN_ID:
        return

    try:
        amount = int(callback.data.split(":")[-1])
    except (ValueError, IndexError):
        amount = 100

    if amount < 10:
        amount = 100

    add_user(uid, callback.from_user.username, callback.from_user.full_name)
    order_id = f"inc_{uid}_{int(time.time() * 1000)}"
    create_payment_order(order_id, uid, float(amount))

    url = build_payment_url(order_id, float(amount))
    if not url:
        await callback.message.answer(t(uid, "balance_payment_error"))
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid, "btn_pay"), url=url)],
        [InlineKeyboardButton(text=t(uid, "btn_back"), callback_data="menu:balance")],
    ])
    await callback.message.edit_text(
        t(uid, "balance_topup_text", amount=amount),
        reply_markup=kb,
        parse_mode="HTML",
    )
