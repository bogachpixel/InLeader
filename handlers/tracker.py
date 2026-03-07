"""
Трекер действий — геймификация со спринтами и строгой изоляцией данных по user_id.
"""

import logging
import os
from datetime import date

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from config.i18n import TEXTS
from services.ai_service import generate_text
from services.db import (
    close_tracker_day,
    get_timezone,
    get_tracker_data,
    get_user_coins,
    set_timezone,
    upsert_user,
    update_daily_progress,
    reset_tracker_sprint,
)
from services.language import t

logger = logging.getLogger(__name__)
ADMIN_ID = int(os.getenv("ADMIN_ID", "5925660014"))
router = Router()

_ALL_TRACKER_BUTTONS = {texts["btn_tracker"] for texts in TEXTS.values()}

# 4 задачи
TASK_IDS = (1, 2, 3, 4)
TASK_LABELS = ("contacts", "followup", "content", "study")

TIMEZONE_OPTIONS = [
    (2, "UTC+2 Европа"),
    (3, "UTC+3 Москва"),
    (4, "UTC+4 Екатеринбург"),
    (5, "UTC+5 Астана/Ташкент"),
    (6, "UTC+6 Алматы/Бишкек"),
    (7, "UTC+7 Новосибирск/Бангкок"),
    (8, "UTC+8 Иркутск/Сингапур"),
]


class TrackerState(StatesGroup):
    choosing_timezone = State()
    in_tracker = State()
    waiting_for_task_report = State()


def _build_timezone_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=label, callback_data=f"tz:{offset}")]
        for offset, label in TIMEZONE_OPTIONS
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def _build_tracker_keyboard(user_id: int, progress_str: str) -> InlineKeyboardMarkup:
    # progress_str format: "0,0,0,0"
    progress = progress_str.split(",")
    buttons: list[list[InlineKeyboardButton]] = []
    
    for i, key in enumerate(TASK_LABELS):
        done = progress[i] == "1"
        icon = "✅" if done else "❌"
        label = t(user_id, f"trk_{key}")
        buttons.append([
            InlineKeyboardButton(
                text=f"[{icon}] {label}",
                callback_data=f"task_click:{i+1}",
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text=t(user_id, "trk_finish"),
            callback_data="tracker:finish",
        )
    ])
    buttons.append([
        InlineKeyboardButton(
            text="🔄 Начать спринт заново",
            callback_data="tracker:reset_sprint",
        )
    ])
    buttons.append([
        InlineKeyboardButton(
            text=t(user_id, "btn_back_menu"),
            callback_data="menu:main",
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def _show_tracker(callback_or_msg: CallbackQuery | Message, uid: int, state: FSMContext) -> None:
    """Показывает трекер с проверкой данных из БД для конкретного юзера."""
    data = get_tracker_data(uid)
    streak = data.get("streak", 0)
    last_date = data.get("last_tracker_date")
    progress_str = data.get("daily_progress", "0,0,0,0")
    today = date.today().isoformat()

    # Проверка блокировки (день уже закрыт)
    if last_date == today:
        text = f"✅ План на сегодня выполнен!\n🔥 Твой стрик: {streak} дней. Возвращайся завтра, чтобы продолжить спринт!"
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="🏠 В меню", callback_data="menu:main")
        ]])
        if isinstance(callback_or_msg, CallbackQuery):
            await callback_or_msg.message.edit_text(text, reply_markup=kb)
        else:
            await callback_or_msg.answer(text, reply_markup=kb)
        return

    # Проверка сброса (новый день)
    if last_date is None or today > last_date:
        if progress_str != "0,0,0,0":
            progress_str = "0,0,0,0"
            update_daily_progress(uid, progress_str)

    await state.set_state(TrackerState.in_tracker)
    text = f"🔥 Твой спринт: {streak} из 7 дней.\n\n{t(uid, 'trk_title')}"
    kb = _build_tracker_keyboard(uid, progress_str)

    if isinstance(callback_or_msg, CallbackQuery):
        try:
            await callback_or_msg.message.edit_text(text, reply_markup=kb)
        except Exception:
            await callback_or_msg.message.answer(text, reply_markup=kb)
    else:
        await callback_or_msg.answer(text, reply_markup=kb)


@router.callback_query(F.data == "menu:tracker")
async def menu_tracker(callback: CallbackQuery, state: FSMContext) -> None:
    uid = callback.from_user.id
    if uid != ADMIN_ID:
        coins = get_user_coins(uid)
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
    upsert_user(uid, callback.from_user.username or callback.from_user.first_name)

    tz = get_timezone(uid)
    if tz is None:
        await state.set_state(TrackerState.choosing_timezone)
        await callback.message.answer(
            "🌍 Чтобы я напоминал тебе о трекере ровно в 20:00, выбери свой часовой пояс:",
            reply_markup=_build_timezone_keyboard(),
        )
        return

    await _show_tracker(callback, uid, state)


@router.message(F.text.func(lambda text: text in _ALL_TRACKER_BUTTONS))
async def tracker_menu(message: Message, state: FSMContext) -> None:
    uid = message.from_user.id
    if uid != ADMIN_ID:
        coins = get_user_coins(uid)
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
    upsert_user(uid, message.from_user.username or message.from_user.first_name)

    tz = get_timezone(uid)
    if tz is None:
        await state.set_state(TrackerState.choosing_timezone)
        await message.answer(
            "🌍 Чтобы я напоминал тебе о трекере ровно в 20:00, выбери свой часовой пояс:",
            reply_markup=_build_timezone_keyboard(),
        )
        return

    await _show_tracker(message, uid, state)


@router.callback_query(F.data.startswith("tz:"), TrackerState.choosing_timezone)
async def timezone_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    uid = callback.from_user.id
    offset = int(callback.data.split(":")[1])
    set_timezone(uid, offset)
    await state.clear()
    await _show_tracker(callback, uid, state)


@router.callback_query(F.data.startswith("task_click:"), TrackerState.in_tracker)
async def task_click(callback: CallbackQuery, state: FSMContext) -> None:
    uid = callback.from_user.id
    task_id = int(callback.data.split(":")[1])
    
    # Получаем данные СТРОГО из БД по user_id
    data = get_tracker_data(uid)
    progress = data.get("daily_progress", "0,0,0,0").split(",")
    
    if progress[task_id-1] == "1":
        await callback.answer("✅ Это задание уже выполнено сегодня!", show_alert=True)
        return

    await callback.answer()
    await state.update_data(current_task_id=task_id)
    await state.set_state(TrackerState.waiting_for_task_report)
    
    label = t(uid, f"trk_{TASK_LABELS[task_id-1]}")
    await callback.message.answer(
        f"📝 Отчет по заданию: *{label}*\n"
        "Напиши кратко, что именно сделано?",
        parse_mode="Markdown"
    )


@router.message(TrackerState.waiting_for_task_report, F.text)
async def process_task_report(message: Message, state: FSMContext) -> None:
    uid = message.from_user.id
    report_text = message.text.strip()
    state_data = await state.get_data()
    task_id = state_data.get("current_task_id")

    if not report_text or len(report_text) < 5:
        await message.answer("❌ Слишком короткий отчет. Распиши подробнее!")
        return

    system_prompt = (
        "Ты — куратор курса. Оцени отчет студента. Если это просто набор букв или отписка, "
        'ответь "REJECT: Опиши подробнее!". '
        'Если норм, ответь "ACCEPT: Отлично!"'
    )

    ai_response = await generate_text(
        prompt=report_text,
        system_instruction=system_prompt,
        task_type="tracker_report",
    )

    if "REJECT:" in ai_response.upper():
        reject_msg = ai_response.split("REJECT:")[-1].strip()
        await message.answer(f"❌ {reject_msg}")
        return

    # Успех: обновляем прогресс в БД СТРОГО для текущего user_id
    data = get_tracker_data(uid)
    progress = data.get("daily_progress", "0,0,0,0").split(",")
    progress[task_id-1] = "1"
    new_progress_str = ",".join(progress)
    update_daily_progress(uid, new_progress_str)

    await message.answer("✅ Задание принято!")
    await _show_tracker(message, uid, state)


@router.callback_query(F.data == "tracker:reset_sprint", TrackerState.in_tracker)
async def reset_sprint(callback: CallbackQuery, state: FSMContext) -> None:
    uid = callback.from_user.id
    reset_tracker_sprint(uid)
    await callback.answer("🔄 Спринт сброшен!", show_alert=True)
    await _show_tracker(callback, uid, state)


@router.callback_query(F.data == "tracker:finish", TrackerState.in_tracker)
async def finish_day_handler(callback: CallbackQuery, state: FSMContext) -> None:
    uid = callback.from_user.id
    # Проверяем прогресс СТРОГО по данным из БД для этого юзера
    data = get_tracker_data(uid)
    progress_str = data.get("daily_progress", "0,0,0,0")
    
    if "0" in progress_str:
        await callback.answer(
            "⚠️ Выполни все задания (все крестики должны стать галочками)!",
            show_alert=True,
        )
        return

    await callback.answer()
    # close_tracker_day обнулит прогресс и обновит дату СТРОГО по user_id
    result = close_tracker_day(uid)
    
    if not result["awarded"]:
        await callback.message.answer(t(uid, "trk_coins_already"))
        return

    new_streak = result["new_streak"]
    await callback.message.answer(
        f"🏁 День закрыт! Твой стрик: {new_streak} 🔥. Возвращайся завтра!"
    )
    await state.clear()
    # Показываем финальный экран блокировки
    await _show_tracker(callback, uid, state)
