"""
Per-user language preference (in-memory).

Сейчас активен только русский язык.
Остальные языки сохранены в i18n.py как заглушки — будут подключены позже.
"""

from config.i18n import TEXTS

_user_languages: dict[int, str] = {}

DEFAULT_LANG = "ru"


def set_language(user_id: int, lang: str) -> None:
    # Сохраняем выбор, но пока он не влияет на перевод
    _user_languages[user_id] = lang


def get_language(user_id: int) -> str:
    # Языки временно заморожены — всегда русский
    return DEFAULT_LANG


def t(user_id: int, key: str, **kwargs: str) -> str:
    """Возвращает строку на русском языке."""
    text = TEXTS[DEFAULT_LANG].get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text
