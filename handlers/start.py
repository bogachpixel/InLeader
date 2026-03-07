import os
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config.i18n import LANGUAGES, TEXTS
from services.db import add_user, is_user_blocked, get_user_coins
from services.language import set_language, t

router = Router()
ADMIN_ID = int(os.getenv("ADMIN_ID", "5925660014"))


_ALL_MENU_BUTTONS = {
    texts.get("btn_menu", "📋 Меню")
    for texts in TEXTS.values()
    if texts.get("btn_menu")
}


def build_menu_reply_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    """Постоянная кнопка «Меню» внизу экрана — при нажатии открывает inline-меню."""
    keyboard = [[KeyboardButton(text=t(user_id, "btn_menu"))]]
    
    # Кнопка баланса для обычных пользователей
    if user_id != ADMIN_ID:
        keyboard.append([KeyboardButton(text="💰 Мой баланс")])
        
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


@router.message(F.text == "💰 Мой баланс")
async def show_balance_handler(message: Message):
    from services import db
    uid = message.from_user.id
    coins = db.get_user_coins(uid)
    
    text = (
        f"💳 <b>Ваш кошелек:</b>\n\n"
        f"Доступно: <b>{coins} InCoins</b> 🪙\n\n"
        f"<i>💡 Напоминаем: 1 генерация ИИ стоит 1 InCoin.</i>"
    )
    await message.answer(text, parse_mode='HTML')


def build_main_menu_inline(user_id: int) -> InlineKeyboardMarkup:
    """Умное меню — inline, не закрывает экран. Пользователь скроллит сам."""
    b = InlineKeyboardBuilder()
    b.button(text=t(user_id, "btn_copywriter"), callback_data="menu:copywriter")
    b.button(text=t(user_id, "btn_objections"), callback_data="menu:objections")
    b.button(text=t(user_id, "btn_calc"), callback_data="menu:calc")
    b.button(text=t(user_id, "btn_marketing"), callback_data="menu:marketing")
    b.button(text=t(user_id, "btn_tracker"), callback_data="menu:tracker")
    b.button(text=t(user_id, "btn_sales_trainer"), callback_data="menu:simulator")
    b.button(text=t(user_id, "btn_crm"), callback_data="menu:crm")
    b.button(text=t(user_id, "btn_analyzer"), callback_data="menu:analyzer")
    b.button(text=t(user_id, "btn_mentor"), callback_data="menu:mentor")
    b.button(text=t(user_id, "btn_onboarding"), callback_data="menu:onboarding")
    b.button(text="📝 Регистрация", callback_data="menu:registration")
    b.button(text="🔗 Рефералка", callback_data="menu:referral")
    b.adjust(2)  # 2 в ряд — компактно
    return b.as_markup()


@router.callback_query(F.data == "menu:registration")
async def registration_handler(callback: CallbackQuery) -> None:
    from services import db
    from services.ai_service import generate_text
    uid = callback.from_user.id

    # 1. Мягкий пэйволл (турникет)
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

    # Временное сообщение
    status = await callback.message.answer("⏳ Готовлю пошаговую инструкцию по регистрации, секунду...")
    await callback.answer()

    system_prompt = (
        "Ты — официальный гид клуба inCruises. Напиши четкую, пошаговую инструкцию для новичка: "
        "как зарегистрироваться на официальном сайте incruises.com. Обязательно укажи следующие шаги: "
        "1) Переход по реферальной ссылке пригласителя (это обязательно). "
        "2) Заполнение личных данных (Имя и Фамилия строго латиницей, как в загранпаспорте). "
        "3) Ввод актуального email и номера телефона. "
        "4) Создание надежного пароля. "
        "5) Нажатие кнопки 'Регистрация' или 'Присоединиться'. "
        "Инструкция должна быть структурированной, использовать эмодзи, быть дружелюбной и "
        "максимально понятной для человека, который не очень хорошо разбирается в компьютерах."
    )

    result = await generate_text(
        prompt="Как зарегистрироваться в inCruises?",
        system_instruction=system_prompt,
        task_type="registration",
        user_id=uid
    )

    try:
        await status.edit_text(result, parse_mode="Markdown")
    except Exception:
        await callback.message.answer(result, parse_mode="Markdown")

    if not result.startswith("⚠️") and uid != ADMIN_ID:
        db.add_user_coins_admin(uid, -1)
        coins = db.get_user_coins(uid)
        await callback.message.answer(f"⚡️ Успешно! Списана 1 монета. Остаток: {coins} 🪙")


@router.callback_query(F.data == "menu:referral")
async def referral_handler(callback: CallbackQuery) -> None:
    uid = callback.from_user.id
    bot_info = await callback.bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start=ref_{uid}"
    
    text = (
        f"💸 <b>Строй сеть и зарабатывай реальные деньги!</b>\n\n"
        f"Скоро мы запускаем мощную партнерскую программу. За каждого новичка, который присоединится к боту по твоей ссылке, "
        f"ты будешь получать <b>реальную денежную скидку</b> на оплату доступа (а не просто InCoins)!\n\n"
        f"🛠 <i>Сейчас система начислений находится в режиме закрытого бета-тестирования, но ты уже можешь строить свою структуру. "
        f"Мы запомним каждого, кто перейдет по твоей ссылке.</i>\n\n"
        f"🔗 <b>Твоя личная пригласительная ссылка:</b>\n"
        f"<code>{ref_link}</code>\n\n"
        f"Отправляй её своей команде и закрепляй партнеров за собой! 🚀"
    )
    
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()


def _build_lang_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for code, label in LANGUAGES.items():
        builder.button(text=label, callback_data=f"lang:{code}")
    builder.adjust(2)  # 2 columns
    return builder.as_markup()


async def _send_welcome_package(message: Message, uid: int):
    """Отправляет обучающий гид и меню после выбора языка."""
    guide = t(uid, "start_guide")

    await message.answer(guide, parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())
    await message.answer(
        t(uid, "menu_choose"),
        reply_markup=build_main_menu_inline(uid),
        parse_mode=None,
    )
    await message.answer(
        t(uid, "menu_reply_hint"),
        reply_markup=build_menu_reply_keyboard(uid),
        parse_mode=None,
    )


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    uid = message.from_user.id
    if uid != ADMIN_ID and is_user_blocked(uid):
        await message.answer("🚫 Ваш доступ к боту заблокирован администратором.")
        return

    user = message.from_user
    is_new = add_user(uid, user.username, user.full_name)

    await state.clear()

    # Возвращающийся пользователь — не показываем "10 коинов начислено", только баланс
    if not is_new:
        coins = get_user_coins(uid)
        name = user.first_name or user.username or "друг"
        await message.answer(
            f"С возвращением, {name}! 👋\n\n"
            f"На твоём балансе осталось <b>{coins} InCoins</b> 🪙",
            parse_mode="HTML",
        )
        await message.answer(
            t(uid, "menu_choose"),
            reply_markup=build_main_menu_inline(uid),
            parse_mode=None,
        )
        await message.answer(
            t(uid, "menu_reply_hint"),
            reply_markup=build_menu_reply_keyboard(uid),
            parse_mode=None,
        )
        return

    name = user.first_name or user.username or "друг"
    greeting = t(uid, "start_greeting", name=name)
    choose = t(uid, "choose_lang")

    await message.answer(
        f"{greeting}\n\n{choose}",
        reply_markup=_build_lang_keyboard(),
        parse_mode="Markdown",
    )


@router.callback_query(F.data.startswith("lang:"))
async def lang_chosen(callback: CallbackQuery) -> None:
    lang = callback.data.removeprefix("lang:")
    uid = callback.from_user.id
    set_language(uid, lang)
    await callback.answer(t(uid, "lang_stub"))
    
    # ЭКРАН ТЕСТОВОГО РЕЖИМА
    test_mode_text = (
        "⚙️ <b>Внимание: Тестовый режим</b>\n\n"
        "Вы получили доступ к InLeader в режиме закрытого бета-тестирования. "
        "Вам начислено <b>10 InCoins</b> 🪙 для бесплатного тестирования ИИ-функций.\n\n"
        "📉 <b>Стоимость:</b> 1 генерация = 1 InCoin.\n"
        "Когда монеты закончатся, доступ к ИИ будет приостановлен до пополнения баланса.\n\n"
        "Используйте монеты с умом, чтобы оценить мощь наших инструментов! 🚢"
    )
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Продолжить", callback_data="start:continue")]
    ])
    
    await callback.message.answer(test_mode_text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data == "start:continue")
async def start_continue(callback: CallbackQuery):
    uid = callback.from_user.id
    await callback.answer()
    await _send_welcome_package(callback.message, uid)


@router.callback_query(F.data == "menu:main")
async def menu_main(callback: CallbackQuery) -> None:
    uid = callback.from_user.id
    await callback.answer()
    await callback.message.answer(
        t(uid, "menu_choose"),
        reply_markup=build_main_menu_inline(uid),
        parse_mode=None,
    )


@router.message(F.text.func(lambda text: text in _ALL_MENU_BUTTONS))
async def menu_button(message: Message) -> None:
    """Обработка нажатия кнопки «Меню» — показывает inline-меню."""
    uid = message.from_user.id
    await message.answer(
        t(uid, "menu_choose"),
        reply_markup=build_main_menu_inline(uid),
        parse_mode=None,
    )


@router.message(Command("menu"))
async def cmd_menu(message: Message) -> None:
    uid = message.from_user.id
    await message.answer(
        t(uid, "menu_choose"),
        reply_markup=build_main_menu_inline(uid),
        parse_mode=None,
    )
