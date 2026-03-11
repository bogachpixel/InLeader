"""
FreeKassa интеграция: генерация ссылки и проверка подписи уведомлений.
"""

import hashlib
import logging
import os
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

FREEKASSA_PAY_URL = "https://pay.fk.money/"


def _get_config() -> tuple[str, str, str]:
    """Merchant ID, Secret1, Secret2 из .env."""
    m = os.getenv("FREEKASSA_MERCHANT_ID", "")
    s1 = os.getenv("FREEKASSA_SECRET1", "")
    s2 = os.getenv("FREEKASSA_SECRET2", "")
    return m, s1, s2


def build_payment_sign(merchant_id: str, amount: float, secret1: str, order_id: str) -> str:
    """Подпись для платёжной ссылки: md5(merchant_id:amount:secret1:order_id)."""
    s = f"{merchant_id}:{amount}:{secret1}:{order_id}"
    return hashlib.md5(s.encode()).hexdigest()


def verify_notification_sign(merchant_id: str, amount: float, secret2: str, order_id: str, sign: str) -> bool:
    """Проверка подписи уведомления: md5(merchant_id:amount:secret2:order_id)."""
    expected = hashlib.md5(f"{merchant_id}:{amount}:{secret2}:{order_id}".encode()).hexdigest()
    return expected.lower() == (sign or "").lower()


def generate_payment_link(order_id: str, amount_rub: float) -> str | None:
    """Генерирует платёжную ссылку FreeKassa (alias для build_payment_url)."""
    return build_payment_url(order_id, amount_rub)


def build_payment_url(order_id: str, amount_rub: float) -> str | None:
    """
    Генерирует платёжную ссылку FreeKassa.
    amount_rub — сумма в рублях.
    """
    m, s1, s2 = _get_config()
    if not m or not s1:
        logger.error("FREEKASSA_MERCHANT_ID или FREEKASSA_SECRET1 не заданы")
        return None

    sign = build_payment_sign(m, amount_rub, s1, order_id)
    params = {
        "m": m,
        "oa": amount_rub,
        "o": order_id,
        "s": sign,
        "currency": "RUB",
        "lang": "ru",
    }
    return f"{FREEKASSA_PAY_URL}?{urlencode(params)}"
