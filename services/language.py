"""
Per-user language preference (in-memory).
Все языки активны. При отсутствии ключа — fallback на русский.
"""

from config.i18n import TEXTS

_user_languages: dict[int, str] = {}

DEFAULT_LANG = "ru"


def set_language(user_id: int, lang: str) -> None:
    _user_languages[user_id] = lang


def get_language(user_id: int) -> str:
    return _user_languages.get(user_id, DEFAULT_LANG)


def t(user_id: int, key: str, **kwargs: str) -> str:
    """Возвращает строку на языке пользователя. Fallback: ru."""
    lang = get_language(user_id)
    strings = TEXTS.get(lang) or TEXTS[DEFAULT_LANG]
    text = strings.get(key) or TEXTS[DEFAULT_LANG].get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text
