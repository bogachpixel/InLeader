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
    give_all_coins_admin
)
from services.ai_service import generate_text, generate_image_ai, IMAGE_FORMAT_REELS, IMAGE_FORMAT_POST, IMAGE_MODELS

router = Router()
logger = logging.getLogger(__name__)

ADMIN_ID = int(os.getenv("ADMIN_ID", "5925660014"))

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
    waiting_for_image_model = State()
    waiting_for_image_format = State()
    waiting_for_image_prompt = State()
    waiting_for_image_own = State()

def get_admin_kb():
    buttons = [
        [InlineKeyboardButton(text="📢 Рассылка всем", callback_data="admin:broadcast")],
        [InlineKeyboardButton(text="🎁 Раздать всем 10 InCoins", callback_data="admin:give_all_10")],
        [InlineKeyboardButton(text="💰 Управление InCoins", callback_data="admin:add_coins")],
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

@router.message(AdminState.waiting_for_user_id_analysis)
async def admin_ai_analyze_process(message: Message, state: FSMContext):
    user = find_user_by_id_or_username(message.text)
    if not user:
        await message.answer("❌ Не найден.")
        return
    await state.update_data(target_user_id=user['user_id'])
    status = await message.answer("⏳ Анализирую активность...")
    prompt = f"Проанализируй партнера: {user}. Score: {user.get('score', 0)}, Coins: {user.get('incoins', 0)}."
    res = await generate_text(prompt, "Ты MLM аналитик.", task_type="tracker_report")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Составить письмо", callback_data="admin:custom_ai_prompt")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin:back")]
    ])
    await status.edit_text(res, reply_markup=kb)

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
    await message.answer("🖼 Выбери модель для генерации:", reply_markup=kb)


@router.callback_query(F.data.startswith("imgmodel:"), StateFilter(AdminState.waiting_for_image_model))
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


@router.callback_query(F.data.startswith("imgfmt:"), StateFilter(AdminState.waiting_for_image_format))
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
