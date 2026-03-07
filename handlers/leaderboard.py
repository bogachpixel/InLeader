from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from config.i18n import TEXTS
from services.db import get_top_users
from services.language import t

router = Router()

_ALL_LB_BUTTONS = {
    texts["btn_leaderboard"] for texts in TEXTS.values() if "btn_leaderboard" in texts
}

_MEDALS = {1: "🥇", 2: "🥈", 3: "🥉"}


@router.callback_query(F.data == "menu:leaderboard")
async def menu_leaderboard(callback: CallbackQuery) -> None:
    uid = callback.from_user.id
    await callback.answer()
    top = get_top_users(10)
    if not top:
        await callback.message.answer(t(uid, "lb_empty"), parse_mode=None)
        return
    lines = [t(uid, "lb_header")]
    for i, row in enumerate(top, 1):
        medal = _MEDALS.get(i, "🏅")
        name = f"@{row['username']}" if row["username"] else f"id:{row['user_id']}"
        lines.append(f"  {medal} {name} — {row['score']} InCoins")
    await callback.message.answer("\n".join(lines), parse_mode=None)


@router.message(F.text.func(lambda text: text in _ALL_LB_BUTTONS))
async def leaderboard_show(message: Message) -> None:
    uid = message.from_user.id
    top = get_top_users(10)

    if not top:
        await message.answer(t(uid, "lb_empty"), parse_mode=None)
        return

    lines = [t(uid, "lb_header")]
    for i, row in enumerate(top, 1):
        medal = _MEDALS.get(i, "🏅")
        name = f"@{row['username']}" if row["username"] else f"id:{row['user_id']}"
        lines.append(f"  {medal} {name} — {row['score']} InCoins")

    await message.answer("\n".join(lines), parse_mode=None)
