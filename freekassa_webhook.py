"""
HTTP-сервер для приёма уведомлений FreeKassa и CryptoPay.
Запускается параллельно с ботом. Используй ngrok для туннеля.
"""

import hashlib
import hmac
import json
import logging
import os
from aiohttp import web

from services.db import get_payment_order, mark_payment_paid, add_user_coins_admin, upsert_user
from services.freekassa import _get_config, verify_notification_sign

logger = logging.getLogger(__name__)

ROUTER = web.RouteTableDef()


@ROUTER.get("/freekassa/notification")
async def freekassa_notification_get(_request: web.Request) -> web.Response:
    """Проверка доступности: FreeKassa может слать GET. Возвращаем 200 YES."""
    return web.Response(text="YES", status=200)


@ROUTER.post("/freekassa/notification")
async def freekassa_notification(request: web.Request) -> web.Response:
    """
    Обработчик уведомлений FreeKassa.
    FreeKassa шлёт: MERCHANT_ID, AMOUNT, MERCHANT_ORDER_ID, SIGN (и др.).
    """
    try:
        # FreeKassa шлёт form-urlencoded или JSON
        if request.content_type and "application/json" in request.content_type:
            data = await request.json()
        else:
            data = await request.post()
            data = dict(data)

        merchant_id = str(data.get("MERCHANT_ID", data.get("merchant_id", "")))
        amount = float(data.get("AMOUNT", data.get("amount", 0)))
        order_id = str(data.get("MERCHANT_ORDER_ID") or data.get("o") or "")
        sign = str(data.get("SIGN", data.get("sign", "")))

        if not order_id or not sign:
            logger.warning("FreeKassa: нет order_id или sign")
            return web.Response(text="NO ORDER_ID OR SIGN", status=400)

        m, _, s2 = _get_config()
        if not m or not s2:
            logger.error("FreeKassa: не заданы MERCHANT_ID или SECRET2")
            return web.Response(text="BAD CONFIG", status=500)

        if merchant_id != m:
            logger.warning("FreeKassa: неверный MERCHANT_ID")
            return web.Response(text="BAD MERCHANT", status=400)

        if not verify_notification_sign(m, amount, s2, order_id, sign):
            logger.warning("FreeKassa: неверная подпись")
            return web.Response(text="BAD SIGN", status=400)

        order = get_payment_order(order_id)
        if not order:
            logger.warning("FreeKassa: заказ не найден: %s", order_id)
            return web.Response(text="ORDER NOT FOUND", status=404)

        if order["status"] == "paid":
            logger.info("FreeKassa: заказ %s уже оплачен", order_id)
            return web.Response(text="YES")  # FreeKassa ждёт YES при дубликате

        # Для теста: начисление только при сумме 10 руб
        if amount != 10:
            logger.warning("FreeKassa: сумма %s != 10, начисление не производим", amount)
            return web.Response(text="YES")

        if not mark_payment_paid(order_id):
            return web.Response(text="ALREADY PAID", status=200)

        user_id = order["user_id"]
        # Тарифы: amount_coins задан. Иначе 1₽ = 1 InCoin.
        amount_coins_val = order.get("amount_coins") or 0
        coins = int(amount_coins_val) if amount_coins_val else int(amount)
        if coins < 1:
            coins = 1

        add_user_coins_admin(user_id, coins)

        bot = request.app.get("bot")
        if bot:
            try:
                from services.language import t
                msg = t(user_id, "payment_success", coins=coins, amount=amount)
                await bot.send_message(user_id, msg, parse_mode="HTML")
            except Exception as e:
                logger.warning("FreeKassa: не удалось отправить уведомление user %s: %s", user_id, e)

        logger.info("FreeKassa: заказ %s оплачен, user %s +%d coins", order_id, user_id, coins)
        return web.Response(text="YES")

    except Exception as e:
        logger.exception("FreeKassa notification error: %s", e)
        return web.Response(text="ERROR", status=500)


@ROUTER.post("/cryptopay/webhook")
async def cryptopay_webhook(request: web.Request) -> web.Response:
    """
    Обработчик вебхуков CryptoPay (@CryptoBot).
    Проверка подписи crypto-pay-api-signature (HMAC-SHA256).
    При status=paid: начисление InCoins, уведомление пользователя.
    Всегда возвращаем HTTP 200.
    """
    raw_body = await request.read()
    token = os.getenv("CRYPTOPAY_TOKEN", "").strip()
    if not token:
        logger.warning("CryptoPay: CRYPTOPAY_TOKEN не задан")
        return web.Response(status=200)

    signature = request.headers.get("crypto-pay-api-signature", "")
    if not signature:
        logger.warning("CryptoPay: нет заголовка crypto-pay-api-signature")
        return web.Response(status=200)

    # Проверка подписи: secret = SHA256(token), HMAC-SHA256(body, secret)
    try:
        secret = hashlib.sha256(token.encode()).digest()
        expected = hmac.new(secret, raw_body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            logger.warning("CryptoPay: неверная подпись")
            return web.Response(status=200)
    except Exception as e:
        logger.warning("CryptoPay: ошибка проверки подписи: %s", e)
        return web.Response(status=200)

    try:
        data = json.loads(raw_body.decode())
    except json.JSONDecodeError as e:
        logger.warning("CryptoPay: невалидный JSON: %s", e)
        return web.Response(status=200)

    update_type = data.get("update_type", "")
    payload_obj = data.get("payload") or {}

    if update_type != "invoice_paid" or payload_obj.get("status") != "paid":
        return web.Response(status=200)

    # Извлекаем user_id из payload (наши данные при создании инвойса)
    payload_str = payload_obj.get("payload", "")
    user_id = None
    if payload_str:
        try:
            custom = json.loads(payload_str) if isinstance(payload_str, str) and payload_str.startswith("{") else {}
            user_id = custom.get("user_id")
            if user_id is None and payload_str.isdigit():
                user_id = int(payload_str)
        except (json.JSONDecodeError, ValueError):
            if str(payload_str).isdigit():
                user_id = int(payload_str)

    if not user_id:
        logger.warning("CryptoPay: не найден user_id в payload")
        return web.Response(status=200)

    # Расчёт монет: paid_amount (в крипте) * paid_usd_rate (USD за единицу) * coins_per_usd
    paid_amount = float(payload_obj.get("paid_amount") or payload_obj.get("amount") or 0)
    paid_usd_rate = float(payload_obj.get("paid_usd_rate") or 0)
    coins_per_usd = float(os.getenv("CRYPTOPAY_COINS_PER_USD", "100"))

    if paid_usd_rate > 0:
        amount_usd = paid_amount * paid_usd_rate
        coins = max(1, int(amount_usd * coins_per_usd))
    else:
        # Fallback: USDT≈1, TON≈500 USD
        asset = (payload_obj.get("paid_asset") or payload_obj.get("asset") or "USDT").upper()
        rates = {"USDT": 1, "USDC": 1, "TON": 500, "BTC": 100000, "ETH": 4000, "LTC": 100, "BNB": 600, "TRX": 0.2}
        usd_per_unit = rates.get(asset, 1)
        coins = max(1, int(paid_amount * usd_per_unit * coins_per_usd))

    upsert_user(int(user_id), None)
    add_user_coins_admin(int(user_id), coins)

    bot = request.app.get("bot")
    if bot:
        try:
            from services.language import t
            msg = t(int(user_id), "payment_success_cryptopay")
            await bot.send_message(int(user_id), msg)
        except Exception as e:
            logger.warning("CryptoPay: не удалось отправить уведомление user %s: %s", user_id, e)

    logger.info("CryptoPay: оплата user %s +%d coins", user_id, coins)
    return web.Response(status=200)


def create_app(bot=None) -> web.Application:
    app = web.Application()
    app["bot"] = bot
    app.router.add_routes(ROUTER)
    return app


async def run_webhook_server(bot, host: str = "0.0.0.0", port: int = 8080) -> None:
    """Запускает HTTP-сервер для FreeKassa."""
    app = create_app(bot)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    logger.info("FreeKassa webhook server listening on %s:%d", host, port)
