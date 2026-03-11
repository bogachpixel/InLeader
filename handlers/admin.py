import os
import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.db import (
    get_total_users, 
    get_all_user_ids, 
    get_user_profile, 
    get_all_users_admin, 
    get_setting, 
    set_setting,
    reset_all_authorizations,
    find_user_by_id_or_username,
    add_user_coins_admin,
    get_user_coins,
    give_all_coins_admin,
    get_usage_for_user,
    get_usage_aggregate,
    get_usage_costs_by_period,
    get_usage_by_user_period,
)
from services.ai_service import generate_text, generate_image_ai, format_admin_footer, IMAGE_FORMAT_REELS, IMAGE_FORMAT_POST, IMAGE_MODELS

router = Router()
logger = logging.getLogger(__name__)

ADMIN_ID = int(os.getenv("ADMIN_ID", "5925660014"))

# task_type → русское название кнопки/раздела (как пользователь видит в меню)
TASK_TYPE_LABELS = {
    "copywriter": "✍️ Умный копирайтер",
    "objections": "🛡 База возражений",
    "simulator": "🎭 AI-Тренажер продаж",
    "tracker_report": "🎯 Трекер действий",
    "general": "📋 Прочее",
    "marketing": "📊 Маркетинг-план",
    "analyzer": "🧠 Аналитик встреч",
    "mentor": "🧠 AI-Ментор",
    "crm": "📅 CRM и Напоминания",
    "registration": "📝 Регистрация",
    "onboarding_navigator": "🚀 Запуск новичка",
    "onboarding_chat": "🚀 Запуск новичка",
}


def _task_label(task_type: str) -> str:
    return TASK_TYPE_LABELS.get(task_type, task_type)

class AdminState(StatesGroup):
    waiting_for_broadcast = State()
    waiting_for_user_id_analysis = State()
    waiting_for_custom_ai_prompt = State()
    waiting_for_personal_msg_id = State()
    waiting_for_personal_msg_text = State()
    waiting_for_new_password = State()
    waiting_for_coin_user = State()
    waiting_for_coin_amount = State()
    waiting_for_user_block = State()
    waiting_for_ai_letter_task = State()
    waiting_for_analysis_user_id = State()
    waiting_for_image_model = State()
    waiting_for_image_format = State()
    waiting_for_image_prompt = State()
    waiting_for_image_own = State()

def get_admin_kb():
    buttons = [
        [InlineKeyboardButton(text="📢 Рассылка всем", callback_data="admin:broadcast")],
        [InlineKeyboardButton(text="🎁 Раздать всем 10 InCoins", callback_data="admin:give_all_10")],
        [InlineKeyboardButton(text="💰 Управление InCoins", callback_data="admin:add_coins")],
        [InlineKeyboardButton(text="📊 Анализ", callback_data="admin:analysis")],
        [InlineKeyboardButton(text="🧠 AI-Анализ партнера", callback_data="admin:ai_analyze")],
        [InlineKeyboardButton(text="🎯 Написать лично", callback_data="admin:personal_msg")],
        [InlineKeyboardButton(text="🪙 Проверка монет", callback_data="admin:check_coins")],
        [InlineKeyboardButton(text="🚫 Управление доступом", callback_data="admin:manage_access")],
        [InlineKeyboardButton(text="👥 Список пользователей", callback_data="admin:users_list")],
        [InlineKeyboardButton(text="🔑 Изменить пароль входа", callback_data="admin:change_pass")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("👑 Добро пожаловать в Панель Управления", reply_markup=get_admin_kb())

@router.callback_query(F.data == "admin:back")
async def admin_back(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        return
    await state.clear()
    await callback.message.edit_text("👑 Добро пожаловать в Панель Управления", reply_markup=get_admin_kb())
    await callback.answer()


# --- АНАЛИЗ (Lama бесплатный) ---

@router.callback_query(F.data == "admin:analysis")
async def admin_analysis_menu(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        return
    await state.clear()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Анализ затрат", callback_data="admin:analysis_costs")],
        [InlineKeyboardButton(text="📈 Общий анализ", callback_data="admin:analysis_general")],
        [InlineKeyboardButton(text="👤 Отдельный анализ", callback_data="admin:analysis_single")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin:back")],
    ])
    await callback.message.edit_text(
        "📊 <b>Анализ активности</b>\n\nВыбери тип отчёта:",
        reply_markup=kb,
        parse_mode="HTML",
    )
    await callback.answer()


def _build_analysis_user_kb() -> InlineKeyboardMarkup:
    """Список пользователей для отдельного анализа (имя + юзернейм)."""
    users = get_all_users_admin()
    kb = InlineKeyboardBuilder()
    for u in users[-20:]:
        name = u.get("full_name") or ""
        username = u.get("username") or ""
        label = f"{name} (@{username})" if username else (name or str(u["user_id"]))
        if len(label) > 40:
            label = label[:37] + "..."
        kb.button(text=label, callback_data=f"analysis_user:{u['user_id']}")
    kb.button(text="⌨️ Ввести ID вручную", callback_data="analysis_user:manual")
    kb.button(text="🔙 Назад", callback_data="admin:analysis")
    kb.adjust(1)
    return kb.as_markup()


@router.callback_query(F.data == "admin:analysis_costs")
async def admin_analysis_costs_run(callback: CallbackQuery, state: FSMContext):
    """Анализ затрат — обширная статистика: периоды, генерации, все пользователи с разбивкой."""
    if callback.from_user.id != ADMIN_ID:
        return
    await callback.answer()
    period = get_usage_costs_by_period()
    by_user_period = get_usage_by_user_period()
    total_cost = sum(float(u.get("cost_total", 0)) for u in by_user_period)

    sorted_users = sorted(by_user_period, key=lambda x: float(x.get("cost_total", 0)), reverse=True)

    lines = [
        "💰 <b>Анализ затрат</b>\n",
        "━━━━━━━━━━━━━━━━━━━━━",
        "<b>Сводка по периодам (все пользователи):</b>",
        f"  • Сегодня: {period['gen_today']} ген. | ${period['cost_today']:.4f}",
        f"  • За 7 дней: {period['gen_7d']} ген. | ${period['cost_7d']:.4f}",
        f"  • За месяц: {period['gen_month']} ген. | ${period['cost_month']:.4f}",
        "━━━━━━━━━━━━━━━━━━━━━",
        "<b>По пользователям (сегодня | 7д | мес | всего):</b>",
        "",
    ]
    for i, u in enumerate(sorted_users, 1):
        uid = u.get("user_id")
        prof = get_user_profile(uid)
        name = (prof.get("full_name") or prof.get("username") or f"ID{uid}") if prof else f"ID{uid}"
        if isinstance(name, str) and len(name) > 20:
            name = name[:17] + "..."
        ct = float(u.get("cost_today", 0))
        c7 = float(u.get("cost_7d", 0))
        cm = float(u.get("cost_month", 0))
        ctot = float(u.get("cost_total", 0))
        gt = int(u.get("gen_today", 0))
        g7 = int(u.get("gen_7d", 0))
        gm = int(u.get("gen_month", 0))
        gtot = int(u.get("gen_total", 0))
        lines.append(f"{i}. <b>{name}</b> (ID:{uid})")
        lines.append(f"   Сегодня: {gt} ген. | ${ct:.4f}")
        lines.append(f"   7 дней: {g7} ген. | ${c7:.4f}")
        lines.append(f"   Месяц: {gm} ген. | ${cm:.4f}")
        lines.append(f"   <b>Всего: {gtot} ген. | ${ctot:.4f}</b>")
        lines.append("")

    lines.append("━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"<b>ИТОГО (всё время):</b> ${total_cost:.4f}")

    text = "\n".join(lines)
    if len(text) > 4000:
        text = "\n".join(lines[:45] + ["...", "━━━━━━━━━━━━━━━━━━━━━", f"<b>ИТОГО (всё время):</b> ${total_cost:.4f}"])
    await callback.message.edit_text(text, parse_mode="HTML")


@router.callback_query(F.data == "admin:analysis_single")
async def admin_analysis_single_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        return
    await state.clear()
    await callback.message.edit_text(
        "👤 Выбери пользователя для отчёта:",
        reply_markup=_build_analysis_user_kb(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("analysis_user:"))
async def admin_analysis_user_selected(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        return
    target = callback.data.split(":")[1]
    if target == "manual":
        await state.set_state(AdminState.waiting_for_analysis_user_id)
        await callback.message.edit_text(
            "🔍 Введи ID или @username пользователя для анализа:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="admin:analysis_single")]
            ]),
        )
        await callback.answer()
        return

    user_id = int(target)
    await _run_single_analysis(callback, user_id)
    await callback.answer()


async def _run_single_analysis(callback_or_msg, user_id: int):
    """Отдельный анализ — чёткая структура по user_id."""
    profile = get_user_profile(user_id)
    usage = get_usage_for_user(user_id)
    if not profile:
        text = f"❌ Пользователь {user_id} не найден в базе."
        if hasattr(callback_or_msg, "message"):
            await callback_or_msg.message.answer(text)
        else:
            await callback_or_msg.answer(text)
        return

    total_cost = sum(float(u.get("cost") or 0) for u in usage)
    by_task = {}
    for u in usage:
        t = u.get("task_type", "?")
        by_task[t] = by_task.get(t, 0) + 1

    name = profile.get("full_name") or profile.get("username") or str(user_id)
    lines = [
        "👤 <b>Отдельный анализ</b>\n",
        "━━━━━━━━━━━━━━━━━━━━━",
        f"<b>Пользователь:</b> {name} (ID: {user_id})",
        f"<b>InCoins:</b> {profile.get('incoins', 0)} | <b>Стрик:</b> {profile.get('streak', 0)}",
        "",
        "<b>Генерации:</b>",
        f"  • Всего: {len(usage)}",
        f"  • Потрачено: ${total_cost:.4f}",
        "",
        "<b>По кнопкам (кто куда нажимал):</b>",
    ]
    for task, cnt in sorted(by_task.items(), key=lambda x: -x[1]):
        label = _task_label(task)
        lines.append(f"  • {label}: {cnt}")
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━")

    text = "\n".join(lines)
    if hasattr(callback_or_msg, "message"):
        await callback_or_msg.message.answer(text, parse_mode="HTML")
    else:
        await callback_or_msg.answer(text, parse_mode="HTML")


@router.callback_query(F.data == "admin:analysis_general")
async def admin_analysis_general_run(callback: CallbackQuery, state: FSMContext):
    """Общий анализ — чёткая структура, без Lama."""
    if callback.from_user.id != ADMIN_ID:
        return
    await callback.answer()
    agg = get_usage_aggregate()
    by_user = agg.get("by_user", [])
    total_gen = agg.get("total_gen", 0)
    total_cost = agg.get("total_cost", 0)
    by_task = agg.get("by_task", [])

    lines = [
        "📈 <b>Общий анализ</b>\n",
        "━━━━━━━━━━━━━━━━━━━━━",
        "",
        "<b>Итого:</b>",
        f"  • Генераций: {total_gen}",
        f"  • Потрачено: ${total_cost:.4f}",
        "",
        "<b>По кнопкам (кто куда нажимал):</b>",
    ]
    for t in sorted(by_task, key=lambda x: -x["cnt"]):
        label = _task_label(t["task_type"])
        lines.append(f"  • {label}: {t['cnt']}")
    lines.append("")
    lines.append("<b>Топ по затратам:</b>")

    top_by_cost = sorted(by_user, key=lambda x: float(x.get("total_cost", 0)), reverse=True)[:15]
    for i, u in enumerate(top_by_cost, 1):
        uid = u.get("user_id")
        cost = float(u.get("total_cost", 0))
        cnt = u.get("cnt", 0)
        prof = get_user_profile(uid)
        name = (prof.get("full_name") or prof.get("username") or f"ID{uid}") if prof else f"ID{uid}"
        if len(str(name)) > 20:
            name = str(name)[:17] + "..."
        lines.append(f"  {i}. {name} (ID:{uid}) — {cnt} ген. | ${cost:.4f}")

    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━")

    text = "\n".join(lines)
    if len(text) > 4000:
        text = "\n".join(lines[:35] + ["... (обрезано)", "━━━━━━━━━━━━━━━━━━━━━"])
    await callback.message.edit_text(text, parse_mode="HTML")


# --- СПИСОК ПОЛЬЗОВАТЕЛЕЙ ДЛЯ ВЫБОРА ---

def _build_user_selection_kb(users: list, action_prefix: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # Берем последних 15 пользователей для выбора
    for u in users[-15:]:
        name = u['full_name'] or u['username'] or str(u['user_id'])
        kb.button(text=name, callback_data=f"{action_prefix}:{u['user_id']}")
    kb.button(text="⌨️ Ввести ID вручную", callback_data=f"{action_prefix}:manual")
    kb.button(text="🔙 Назад", callback_data="admin:back")
    kb.adjust(1)
    return kb.as_markup()

# --- УПРАВЛЕНИЕ МОНЕТАМИ (INCOINS) ---

@router.callback_query(F.data == "admin:give_all_10")
async def admin_give_all_10(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    # Начисляем всем, кроме самого админа
    from services.db import _get_conn
    conn = _get_conn()
    cursor = conn.execute("UPDATE users SET incoins = COALESCE(incoins, 0) + 10 WHERE user_id != ?", (ADMIN_ID,))
    conn.commit()
    await callback.answer(f"✅ Успешно! {cursor.rowcount} чел. получили по 10 монет.", show_alert=True)

@router.callback_query(F.data == "admin:add_coins")
async def admin_add_coins_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID: return
    users = get_all_users_admin()
    await callback.message.edit_text("💰 Выбери пользователя для управления InCoins:", reply_markup=_build_user_selection_kb(users, "sel_coin"))
    await callback.answer()

@router.callback_query(F.data.startswith("sel_coin:"))
async def admin_sel_coin_user(callback: CallbackQuery, state: FSMContext):
    target = callback.data.split(":")[1]
    if target == "manual":
        await state.set_state(AdminState.waiting_for_coin_user)
        await callback.message.answer("🔍 Введите Telegram ID или @username партнера:")
    else:
        user_id = int(target)
        coins = get_user_coins(user_id)
        await state.update_data(target_user_id=user_id)
        await state.set_state(AdminState.waiting_for_coin_amount)
        await callback.message.answer(
            f"👤 Текущий баланс: <b>{coins} InCoins</b>\n\n"
            "Введите число для изменения (напр. <b>10</b> для начисления или <b>-5</b> для списания):",
            parse_mode="HTML"
        )
    await callback.answer()

@router.message(AdminState.waiting_for_coin_amount)
async def admin_coin_amount_final(message: Message, state: FSMContext):
    val = message.text.strip()
    try:
        amount = int(val)
    except ValueError:
        await message.answer("❌ Ошибка! Введи только число:")
        return
    data = await state.get_data()
    target_id = data['target_user_id']
    add_user_coins_admin(target_id, amount)
    new_coins = get_user_coins(target_id)
    await message.answer(f"✅ Баланс пользователя {target_id} изменен на {amount}. Теперь у него: {new_coins} 🪙")
    try:
        await message.bot.send_message(target_id, f"💳 Ваш баланс InCoins изменен администратором на {amount}. Теперь у вас: {new_coins} 🪙")
    except: pass
    await state.clear()
    await message.answer("👑 Возвращаюсь в управление", reply_markup=get_admin_kb())

# --- ОСТАЛЬНОЕ БЕЗ ИЗМЕНЕНИЙ ---

@router.callback_query(F.data == "admin:users_list")
async def admin_users_list(callback: CallbackQuery):
    """Список пользователей — ID, имя, username, стрик, статус блокировки."""
    if callback.from_user.id != ADMIN_ID:
        return
    users = get_all_users_admin()
    text = "<b>👥 Список пользователей</b>\n\n"
    for u in users:
        status = "🔴 ЗАБЛОКИРОВАН" if u.get("is_blocked") else "🟢"
        name = u.get("full_name") or ""
        username = u.get("username") or ""
        label = f"{name} (@{username})" if username else (name or f"ID{u['user_id']}")
        if len(label) > 35:
            label = label[:32] + "..."
        text += f"• {label} | ID:{u['user_id']} | Стрик:{u.get('streak', 0)} {status}\n"
    if len(text) > 4000:
        text = text[:3970] + "\n... (обрезано)"
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="admin:back")]])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode=ParseMode.HTML)
    await callback.answer()


@router.callback_query(F.data == "admin:check_coins")
async def admin_check_coins(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    users = get_all_users_admin()
    text = "<b>🪙 Баланс InCoins пользователей:</b>\n\n"
    for u in users:
        profile = get_user_profile(u['user_id'])
        coins = profile.get('incoins', 0) if profile else 0
        name = u['full_name'] or u['username'] or str(u['user_id'])
        text += f"👤 {name} | ID: {u['user_id']} | 💰 <b>{coins}</b>\n"
    await callback.message.answer(text, parse_mode=ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == "admin:manage_access")
async def manage_access_start(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    users = get_all_users_admin()
    text = "<b>🚫 Управление доступом</b>\n\nВыбери пользователя для блокировки/разблокировки:"
    kb = InlineKeyboardBuilder()
    for u in users[-15:]:
        status = "🔴 ЗАБЛОКАН" if u.get('is_blocked') else "🟢 Активен"
        name = u['full_name'] or u['username'] or str(u['user_id'])
        kb.button(text=f"{name} | {status}", callback_data=f"block_toggle:{u['user_id']}")
    kb.button(text="⌨️ Ввести ID вручную", callback_data="block_manual_id")
    kb.button(text="🔙 В админку", callback_data="admin:back")
    kb.adjust(1)
    await callback.message.edit_text(text, reply_markup=kb.as_markup(), parse_mode=ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data.startswith("block_toggle:"))
async def block_toggle_process(callback: CallbackQuery):
    from services.db import is_user_blocked, set_user_block_status
    target_id = int(callback.data.split(":")[1])
    if target_id == ADMIN_ID:
        await callback.answer("❌ Нельзя заблокировать админа!", show_alert=True)
        return
    new_status = not is_user_blocked(target_id)
    set_user_block_status(target_id, new_status)
    await callback.answer(f"✅ Статус изменен!")
    await manage_access_start(callback)

@router.callback_query(F.data == "admin:ai_analyze")
async def admin_ai_analyze_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID: return
    await state.set_state(AdminState.waiting_for_user_id_analysis)
    await callback.message.answer("🔍 Введи ID или @username для анализа (Llama 3.1):")
    await callback.answer()

@router.message(AdminState.waiting_for_analysis_user_id)
async def admin_analysis_manual_id(message: Message, state: FSMContext):
    """Ручной ввод ID для отдельного анализа."""
    if message.from_user.id != ADMIN_ID:
        return
    user = find_user_by_id_or_username(message.text)
    if not user:
        await message.answer("❌ Пользователь не найден.")
        return
    await state.clear()
    await _run_single_analysis(message, user["user_id"])


@router.message(AdminState.waiting_for_user_id_analysis)
async def admin_ai_analyze_process(message: Message, state: FSMContext):
    user = find_user_by_id_or_username(message.text)
    if not user:
        await message.answer("❌ Не найден.")
        return
    await state.update_data(target_user_id=user['user_id'])
    uid = message.from_user.id
    status = await message.answer("⏳ Анализирую активность...")
    prompt = f"Проанализируй партнера: {user}. Score: {user.get('score', 0)}, Coins: {user.get('incoins', 0)}."
    gen = await generate_text(prompt, "Ты MLM аналитик.", task_type="tracker_report", user_id=uid)
    display = gen.text + format_admin_footer(gen, uid)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Составить письмо", callback_data="admin:custom_ai_prompt")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin:back")]
    ])
    await status.edit_text(display, reply_markup=kb)

@router.callback_query(F.data == "admin:broadcast")
async def admin_broadcast_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.waiting_for_broadcast)
    await callback.message.answer("📢 Введите текст рассылки:")
    await callback.answer()

@router.message(AdminState.waiting_for_broadcast)
async def admin_broadcast_process(message: Message, state: FSMContext):
    uids = get_all_user_ids()
    count = 0
    for uid in uids:
        try:
            await message.bot.send_message(uid, message.text)
            count += 1
        except: pass
    await message.answer(f"✅ Рассылка завершена: {count} чел.")
    await state.clear()


@router.message(Command("image"))
async def admin_image_gen_cmd(message: Message, state: FSMContext):
    """Команда /image — только для админа. Выбор модели -> формат -> запрос."""
    if message.from_user.id != ADMIN_ID:
        return
    await state.clear()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1️⃣ Nano Banana 2", callback_data="imgmodel:nanobanana")],
        [InlineKeyboardButton(text="2️⃣ Flux 2 Pro", callback_data="imgmodel:flux")],
        [InlineKeyboardButton(text="3️⃣ Gemini 2.5 Flash Image", callback_data="imgmodel:gemini25flash")],
        [InlineKeyboardButton(text="4️⃣ Riverflow V2 Fast", callback_data="imgmodel:riverflow_fast")],
        [InlineKeyboardButton(text="5️⃣ Riverflow V2 Standard", callback_data="imgmodel:riverflow_std")],
        [InlineKeyboardButton(text="6️⃣ Flux 2 Pro (alt)", callback_data="imgmodel:flux2pro")],
        [InlineKeyboardButton(text="📷 Своя", callback_data="imgmodel:own")],
    ])
    await state.set_state(AdminState.waiting_for_image_model)
    await message.answer("🖼 Выбери модель для генерации:", reply_markup=kb, parse_mode=None)


@router.callback_query(F.data.startswith("imgmodel:"))
async def admin_image_model_chosen(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        return
    model_key = callback.data.split(":")[1]
    if model_key == "own":
        await state.set_state(AdminState.waiting_for_image_own)
        await callback.message.edit_text("📷 Выбери картинку из галереи телефона и отправь сюда:")
        await callback.answer()
        return
    if model_key not in IMAGE_MODELS:
        await callback.answer("❌ Модель не найдена", show_alert=True)
        return
    await state.update_data(image_model=model_key)
    await state.set_state(AdminState.waiting_for_image_format)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 В рилс (вертикальный 9:16)", callback_data="imgfmt:reels")],
        [InlineKeyboardButton(text="🖼 В пост (горизонтальный 16:9)", callback_data="imgfmt:post")],
    ])
    model_name = IMAGE_MODELS[model_key]["name"]
    await callback.message.edit_text(f"🖼 Модель: <b>{model_name}</b>\n\nВыбери формат:", reply_markup=kb, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("imgfmt:"))
async def admin_image_format_chosen(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        return
    fmt = callback.data.split(":")[1]
    aspect = IMAGE_FORMAT_REELS if fmt == "reels" else IMAGE_FORMAT_POST
    await state.update_data(image_aspect_ratio=aspect)
    await state.set_state(AdminState.waiting_for_image_prompt)
    data = await state.get_data()
    model_name = IMAGE_MODELS.get(data.get("image_model", "nanobanana"), {}).get("name", "Nano Banana 2")
    await callback.message.edit_text(f"🖼 Напиши текстовый запрос для генерации ({model_name}):")
    await callback.answer()


@router.message(AdminState.waiting_for_image_own, F.photo)
async def admin_image_own_photo(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    photo = message.photo[-1]
    file_id = photo.file_id
    await state.update_data(image_file_id=file_id, image_as_photo=True)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Отправить картинку всем пользователям", callback_data="admin:broadcast_image")]
    ])
    await message.answer("Картинка получена. Отправить всем?", reply_markup=kb)
    await state.set_state(AdminState.waiting_for_image_own)


@router.message(AdminState.waiting_for_image_own)
async def admin_image_own_not_photo(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("❌ Отправь картинку (фото из галереи).")


@router.message(AdminState.waiting_for_image_prompt)
async def admin_image_gen_process(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    prompt = (message.text or "").strip()
    if not prompt:
        await message.answer("❌ Введи непустой текст запроса.")
        return
    data = await state.get_data()
    aspect_ratio = data.get("image_aspect_ratio") or "1:1"
    model_key = data.get("image_model") or "nanobanana"
    model_name = IMAGE_MODELS.get(model_key, {}).get("name", "Flux")
    status = await message.answer("⏳ Генерирую картинку...")
    img_bytes, cost = await generate_image_ai(prompt, aspect_ratio=aspect_ratio, model_key=model_key)
    try:
        await status.delete()
    except Exception:
        pass
    if not img_bytes:
        await message.answer("❌ Не удалось сгенерировать картинку. Проверь OPENROUTER_API_KEY и доступность модели.")
        await state.clear()
        return
    from aiogram.types import BufferedInputFile
    file = BufferedInputFile(img_bytes, filename="image.png")
    sent = await message.answer_document(
        document=file,
        caption=(
            f"🖼 <b>{model_name}</b> | По запросу: {prompt[:80]}…\n\n"
            "💡 Можешь использовать в работе — отправь команде для постов, сторис или мотивации."
        ),
        parse_mode="HTML",
    )
    await state.update_data(image_file_id=sent.document.file_id)
    cost_text = f"💰 <b>Стоимость генерации:</b> ${cost:.4f}" if cost is not None else "💰 Стоимость: не указана в ответе API"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Отправить картинку всем пользователям", callback_data="admin:broadcast_image")]
    ])
    await message.answer(f"Картинка сгенерирована.\n\n{cost_text}\n\nОтправь команде?", reply_markup=kb, parse_mode="HTML")
    await state.set_state(AdminState.waiting_for_image_prompt)  # остаёмся в состоянии (храним file_id в data)


@router.callback_query(F.data == "admin:broadcast_image")
async def admin_broadcast_image(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        return
    data = await state.get_data()
    file_id = data.get("image_file_id")
    if not file_id:
        await callback.answer("❌ Картинка не найдена. Сгенерируй или загрузи новую.", show_alert=True)
        return
    await callback.answer("⏳ Отправляю всем пользователям...")
    uids = get_all_user_ids()
    count = 0
    caption = (
        "✨ <b>Картинка для тебя от InLeader</b>\n\n"
        "Используй в постах, сторис или для мотивации команды — "
        "твоя аудитория ждёт качественного контента! 🚀"
    )
    as_photo = data.get("image_as_photo", False)
    for uid in uids:
        if uid == ADMIN_ID:
            continue
        try:
            if as_photo:
                await callback.bot.send_photo(uid, photo=file_id, caption=caption, parse_mode="HTML")
            else:
                await callback.bot.send_document(uid, document=file_id, caption=caption, parse_mode="HTML")
            count += 1
        except Exception:
            pass
    await callback.message.answer(f"✅ Картинка отправлена {count} пользователям.")
    await state.clear()
