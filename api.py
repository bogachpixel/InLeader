import hashlib
import os
import time
import asyncio
import base64
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

import json
import re

from services import db
from services import ai_service
from services.language import get_language, set_language, t
from config.prompts import get_system_instruction
from config.i18n import LANGUAGES
from config.knowledge_base import (
    INSIDER_DISCOUNT_PCT,
    MAX_RP_COVERAGE_PCT,
    RP_VALUE_USD,
    FREE_MEMBERSHIP_FACTS_FOR_AI,
    get_rank_facts_for_ai,
    get_rewards_file_facts_for_ai,
    REWARDS_FACTS_FOR_AI,
)
from services.db import (
    get_tracker_data,
    get_timezone,
    set_timezone,
    update_daily_progress,
    reset_tracker_sprint,
    close_tracker_day,
    upsert_user,
    add_crm_reminder,
    get_user_crm_reminders,
    create_payment_order,
)
from services.image_gen import (
    generate_tourist_receipt,
    generate_cruise_receipt,
    generate_conversion_receipt,
)

app = FastAPI(title="InLeader API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    section: str
    buttonContext: Optional[str] = None
    user_id: int
    review_request: Optional[bool] = False  # Разбор сессии (objections/trainer)
    marketing_key: Optional[str] = None  # ranks, rewards, free_membership, ask_ai
    mentor_key: Optional[str] = None  # mindset, sales, coaching, management, psychology, mlm
    newbie_key: Optional[str] = None  # tourist, partner, navigator


class LangRequest(BaseModel):
    user_id: int
    lang: str


class CalcTouristRequest(BaseModel):
    user_id: int
    months: int


class CalcCruiseRequest(BaseModel):
    user_id: int
    price: float
    rp: int


class CalcConversionRequest(BaseModel):
    user_id: int
    text: str


class TrackerTimezoneRequest(BaseModel):
    user_id: int
    offset: int


class TrackerTaskReportRequest(BaseModel):
    user_id: int
    task_id: int
    report_text: str


class CrmAddRequest(BaseModel):
    user_id: int
    task_text: str


@app.get("/api/inleader/profile/{user_id}")
async def get_profile(user_id: int):
    try:
        coins = db.get_user_coins(user_id)
        return {
            "user_id": user_id,
            "incoins": coins if coins is not None else 0,
            "status": "active"
        }
    except Exception as e:
        print(f"Ошибка получения профиля {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")


@app.get("/api/inleader/lang/{user_id}")
async def get_lang(user_id: int):
    """
    Возвращает текущий язык пользователя так же, как в боте.
    """
    try:
        lang = get_language(user_id)
        return {
            "user_id": user_id,
            "lang": lang,
            "label": LANGUAGES.get(lang, LANGUAGES.get("ru")),
        }
    except Exception as e:
        print(f"Ошибка получения языка {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Ошибка чтения языка")


@app.get("/api/inleader/generate-payment/{user_id}")
async def generate_payment(user_id: int):
    """
    Генерирует ссылку для оплаты FreeKassa (10 руб = 10 InCoins).
    """
    print(f"DEBUG: Generating payment for {user_id}")
    merchant_id = os.getenv("FREEKASSA_MERCHANT_ID", "")  # TODO: если нет в .env — заглушка
    secret1 = os.getenv("FREEKASSA_SECRET1", "")
    if not merchant_id or not secret1:
        raise HTTPException(status_code=500, detail="FreeKassa не настроен (MERCHANT_ID/SECRET1)")

    amount = 10
    currency = "RUB"
    order_id = f"{user_id}_{int(time.time())}"

    sign_str = f"{merchant_id}:{amount}:{secret1}:{currency}:{order_id}"
    sign = hashlib.md5(sign_str.encode()).hexdigest()

    payment_url = f"https://pay.freekassa.ru/?m={merchant_id}&oa={amount}&o={order_id}&s={sign}&currency={currency}"
    create_payment_order(order_id, user_id, float(amount), amount_coins=10)

    return {"payment_url": payment_url}


@app.post("/api/inleader/lang")
async def set_lang(req: LangRequest):
    """
    Меняет язык пользователя как в боте, без обращения к ИИ.
    """
    if req.lang not in LANGUAGES:
        raise HTTPException(status_code=400, detail="Неподдерживаемый язык")
    try:
        set_language(req.user_id, req.lang)
        return {
            "status": "ok",
            "user_id": req.user_id,
            "lang": req.lang,
            "label": LANGUAGES[req.lang],
        }
    except Exception as e:
        print(f"Ошибка сохранения языка {req.user_id}: {e}")
        raise HTTPException(status_code=500, detail="Ошибка сохранения языка")

# Логика тренажёра — те же персоны, что в handlers/simulator.py
_SOFTENING_BASE = (
    "Ты начинаешь как жесткий скептик (уровень 10/10). "
    "После каждого КАЧЕСТВЕННОГО ответа пользователя ты должен снижать уровень скепсиса на 2-3 пункта. "
    "Твои возражения должны становиться всё менее агрессивными и более уточняющими. "
    "На 4-5 сообщении ты должен признать поражение, согласиться с доводами и попросить ссылку на регистрацию."
)
_PERSONA_SYSTEM: dict[str, str] = {
    "student": "Ты отыгрываешь роль клиента: Студент. Хочет всё и сразу, боится мнения друзей. "
    "Тебе пытаются продать inCruises. Возражай: 'друзья скажут что я в пирамиду влез', "
    "'нет денег на такое', 'мне нужен быстрый результат'. Общайся на русском, кратко. " + _SOFTENING_BASE,
    "pensioner": "Ты отыгрываешь роль клиента: Пенсионер. Хочет путешествовать, боится обмана. "
    "Тебе пытаются продать inCruises. Возражай: 'уже обманывали', 'не разбираюсь в интернете', "
    "'а если деньги пропадут'. Общайся на русском, тепло. " + _SOFTENING_BASE,
    "office": "Ты отыгрываешь роль клиента: Офисный сотрудник. Мечтает об увольнении, боится риска. "
    "Тебе пытаются продать inCruises. Возражай: 'увольняться страшно', 'а если не получится', "
    "'нет времени на подработку'. Общайся на русском. " + _SOFTENING_BASE,
    "blogger": "Ты отыгрываешь роль клиента: Блогер. Нужен контент, не хочет 'впаривать'. "
    "Тебе пытаются продать inCruises. Возражай: 'не хочу спамить подписчикам', "
    "'мне нужен честный контент', 'это же типичный МЛМ'. Общайся на русском. " + _SOFTENING_BASE,
    "entrepreneur": "Ты отыгрываешь роль клиента: Предприниматель. Ищет систему, не верит в сетевой. "
    "Тебе пытаются продать inCruises. Возражай: 'сетевой — это не бизнес', "
    "'где гарантии', 'мне нужна система а не агитация'. Общайся на русском. " + _SOFTENING_BASE,
    "skeptic": "Ты отыгрываешь роль клиента: Скептичный партнер. Просит факты и легальность. "
    "Тебе пытаются продать inCruises. Возражай: 'докажи что легально', "
    "'где лицензии', 'покажи цифры и кейсы'. Общайся на русском. " + _SOFTENING_BASE,
}


def _get_persona_system(persona_key: str, turn_count: int) -> str:
    base = _PERSONA_SYSTEM.get(persona_key, _PERSONA_SYSTEM["student"])
    if turn_count >= 4:
        base += " [СЕЙЧАС ОБЯЗАТЕЛЬНО: признай поражение, согласись с доводами партнёра и попроси ссылку на регистрацию. Игра окончена.]"
    return base


VICTORY_MSG = "🎉 ПОБЕДА! Ты блестяще отработал все возражения и закрыл сделку. Этот клиент твой!"


def _is_concession(reply: str) -> bool:
    """Проверяет, признал ли клиент поражение (попросил ссылку / согласился)."""
    lower = reply.lower()
    return any(k in lower for k in ("ссылка", "ссылку", "зарегистрир", "присылай", "давай", "согласен", "убедил", "записывай"))


_SECTION_TO_TASK = {
    "objections": "objections",
    "analyzer": "analyzer",
    "analytics": "analyzer",
    "mentor": "mentor",
    "newbie": "onboarding_chat",
    "onboarding": "onboarding",
    "calculator": "calculator",
    "simulator": "simulator",
    "trainer": "simulator",
    "copywriter": "copywriter",
    "onboarding": "onboarding",
    "crm": "crm",
    "marketing": "marketing",
    "tracker": "tracker_report",
    "mentor": "general",
    "tariffs": "general",
    "referral": "general",
    "registration": "registration",
    "language": "general",
    "general": "general",
}


@app.post("/api/inleader/chat")
async def chat_endpoint(request: ChatRequest):
    uid = request.user_id

    coins = db.get_user_coins(uid)
    if coins is None or coins < 1:
        raise HTTPException(status_code=402, detail="Недостаточно InCoins. Пополните баланс в боте.")

    async def ai_generator():
        success = False
        try:
            # Запрос на разбор сессии (objections/trainer)
            if request.review_request and request.messages:
                if request.section == "trainer":
                    dialogue_text = "\n".join(
                        f"{'Партнёр' if m.role == 'user' else 'Клиент'}: {m.content}"
                        for m in request.messages
                    )
                    review_prompt = (
                        "Проанализируй этот диалог продажи клуба inCruises.\n"
                        "Укажи сильные стороны партнёра и его ошибки.\n"
                        "Дай конкретные советы по улучшению.\n"
                        "Поставь оценку от 1 до 10. Ответ на русском.\n\nДиалог:\n"
                        + dialogue_text
                    )
                else:
                    dialogue_text = "\n".join(
                        f"{'Партнёр' if m.role == 'user' else 'ИИ'}: {m.content}"
                        for m in request.messages
                    )
                    review_prompt = (
                        "Проанализируй сессию по отработке возражений inCruises.\n"
                        "Партнёр озвучивал возражения, ИИ давал аргументы.\n"
                        "Дай разбор: сильные стороны, что улучшить, оценка 1-10. Ответ на русском.\n\n"
                        f"Сессия:\n{dialogue_text}"
                    )
                system_instruction = get_system_instruction(uid)
                task_type = "general"
                prompt = review_prompt
                history = None
            else:
                user_msg = ""
                if request.messages:
                    user_msg = request.messages[-1].content
                if not user_msg and request.buttonContext and request.section == "objections":
                    user_msg = request.buttonContext

                task_type = _SECTION_TO_TASK.get(request.section, "general")

                # AI-Тренажер — тот же агент и логика, что в handlers/simulator.py
                if task_type == "simulator":
                    persona_key = request.buttonContext if request.buttonContext in _PERSONA_SYSTEM else "student"
                    turn_count = sum(1 for m in (request.messages or []) if m.role == "user")
                    system_instruction = _get_persona_system(persona_key, turn_count)
                    if not request.messages:
                        prompt = "Начни диалог первым. Напиши одно короткое сообщение как клиент, которому только что написали про круизный клуб."
                        history = None
                    else:
                        prompt = request.messages[-1].content
                        history = [{"role": m.role, "content": m.content} for m in request.messages[:-1]]
                # База возражений — та же логика и агент (DeepSeek), что в боте
                elif task_type == "objections":
                    system_instruction = get_system_instruction(uid)
                    prompt = f"Клиент говорит: {user_msg}. Дай 3 убийственных аргумента для отработки этого возражения в inCruises."
                    history = [{"role": m.role, "content": m.content} for m in request.messages[:-1]] if request.messages else None
                # AI-Ментор — 1:1 как в handlers/mentor.py (GEMINI / general)
                elif task_type == "mentor" and request.mentor_key:
                    MENTOR_PROMPTS = {
                        "mindset": "Ты — Эксперт по мышлению миллионеров. Твоя цель: расширять сознание пользователя, снимать ограничивающие убеждения и страхи, заряжать мощной энергией. Общайся вдохновляюще, уверенно, на 'ты'. Используй метафоры.",
                        "sales": "Ты — Гений продаж и жесткий клоузер. Твоя цель: давать конкретные скрипты, техники дожима, работы с возражениями и НЛП в продажах. Никакой воды. Общайся дерзко, четко, как акула бизнеса. На 'ты'.",
                        "coaching": "Ты — Топовый Бизнес-коуч. Твоя цель: не давать готовых ответов, а задавать сильные, глубокие вопросы, которые приведут пользователя к инсайту. Помогай декомпозировать цели и строить пошаговые планы.",
                        "management": "Ты — Эксперт по менеджменту и управлению. Твоя цель: учить строить системы, делегировать, мотивировать команду и разрешать конфликты. Общайся структурно, по делу, оперируй терминами управления и эффективности.",
                        "psychology": "Ты — Глубокий Психолог. Твоя цель: помочь пользователю с эмоциональным выгоранием, стрессом, пониманием мотивов других людей (эмпатией). Общайся мягко, с пониманием, как мудрый наставник.",
                        "mlm": "Ты — Легендарный топ-лидер сетевого бизнеса (MLM). Твоя цель: давать стратегии рекрутинга, удержания команды, дупликации и работы с глубиной. Общайся энергично, как спонсор, который верит в своего партнера."
                    }
                    system_instruction = MENTOR_PROMPTS.get(request.mentor_key, MENTOR_PROMPTS["mindset"])
                    prompt = user_msg
                    task_type = "general"
                    history = None
                # Аналитик встреч — 1:1 как в handlers/analyzer.py (DeepSeek)
                elif task_type == "analyzer":
                    system_instruction = (
                        "Ты — жёсткий, но справедливый топ-лидер inCruises и гений продаж. "
                        "Проанализируй отчёт о встрече. Выдай ответ строго по структуре:\n\n"
                        "1. 🧠 Психология клиента (что он на самом деле имел в виду, когда возражал).\n"
                        "2. ❌ Твои ошибки (где ты недожал, какую выгоду не продал).\n"
                        "3. 💬 Сообщение для дожима (напиши 1 готовый, мощный вариант SMS/сообщения, "
                        "которое партнёр может скопировать и отправить клиенту прямо сейчас, "
                        "чтобы вывести его на следующий шаг).\n\n"
                        "Форматируй ответ красиво, без лишней воды. Ответ на русском."
                    )
                    prompt = user_msg
                    history = None
                # Запуск новичка (tourist/partner) — 1:1 как handlers/onboarding.py, без InCruises
                elif request.section == "newbie" and request.newbie_key in ("tourist", "partner"):
                    from pathlib import Path
                    base_path = Path(__file__).resolve().parent
                    if request.newbie_key == "tourist":
                        file_path = base_path / "documents" / "341RU_NOBODY_CRUISES_BETTER.pdf"
                        content = _read_pdf_content(file_path)
                        content += "\n\n[ОБЯЗАТЕЛЬНЫЙ РАЗДЕЛ] Как перейти в Партнеры и экономить 100%: Партнёрское членство позволяет получать скидки и бонусы. Переход из Туриста в Партнера — бесплатный, требуется только регистрация как партнёр в личном кабинете."
                        system_instruction = (
                            f"Ты — заботливый консультант. Твоя цель — рассказать о выгодах путешествий и экономии. "
                            f"Опирайся СТРОГО на этот документ: {content[:30000]}. "
                            f"Отвечай дружелюбно, не предлагай строить бизнес, если не спросят."
                        )
                    else:
                        file_path = base_path / "marketing" / "маркетинг.pdf"
                        content = _read_pdf_content(file_path)
                        system_instruction = (
                            f"Ты — топ-лидер и бизнес-тренер. Твоя цель — погрузить новичка в бизнес, "
                            f"рассказать про маркетинг-план, лидерство и пассивный доход. "
                            f"Опирайся СТРОГО на этот документ: {content[:30000]}. "
                            f"Мотивируй на действия."
                        )
                    prompt = user_msg
                    task_type = "onboarding_chat"
                    history = [{"role": m.role, "content": m.content} for m in (request.messages or [])[:-1]]
                # Маркетинг-план — 1:1 как в handlers/marketing.py, task_type=marketing (GPT5_NANO)
                elif task_type == "marketing" and request.marketing_key:
                    mkt_key = request.marketing_key
                    task_type = "marketing"
                    if mkt_key == "ranks":
                        system_instruction = get_system_instruction(uid) + "\n\n" + get_rank_facts_for_ai()
                        prompt = t(uid, "mkt_ranks_ai_prompt")
                        history = None
                    elif mkt_key == "rewards":
                        system_instruction = get_system_instruction(uid) + "\n\n" + get_rewards_file_facts_for_ai()
                        prompt = t(uid, "mkt_rewards_ai_prompt")
                        history = None
                    elif mkt_key == "free_membership":
                        system_instruction = get_system_instruction(uid) + "\n\n" + FREE_MEMBERSHIP_FACTS_FOR_AI
                        prompt = t(uid, "mkt_free_ai_prompt")
                        history = None
                    elif mkt_key == "ask_ai":
                        system_instruction = get_system_instruction(uid) + "\n\n" + REWARDS_FACTS_FOR_AI
                        prompt = t(uid, "mkt_ai_prompt", question=user_msg or "")
                        history = None
                    else:
                        system_instruction = f"Ты — эксперт InLeader. Раздел: {request.section}."
                        if request.buttonContext:
                            system_instruction += f" Контекст: {request.buttonContext}."
                        prompt = user_msg
                        history = [{"role": m.role, "content": m.content} for m in request.messages[:-1]]
                else:
                    system_instruction = f"Ты — эксперт InLeader. Раздел: {request.section}."
                    if request.buttonContext:
                        system_instruction += f" Контекст: {request.buttonContext}."
                    prompt = user_msg
                    history = [{"role": m.role, "content": m.content} for m in request.messages[:-1]]

            full_reply = ""
            async for chunk in ai_service.generate_text_stream(
                prompt=prompt,
                system_instruction=system_instruction,
                task_type=task_type,
                history=history if history else None,
            ):
                success = True
                if task_type == "simulator":
                    full_reply += chunk
                yield chunk
                await asyncio.sleep(0.01)
            # AI-Тренажер: сообщение о победе 1:1 как в боте (handlers/simulator.py)
            if task_type == "simulator" and full_reply:
                turn_count = sum(1 for m in (request.messages or []) if m.role == "user")
                if turn_count >= 4 and _is_concession(full_reply):
                    yield f"\n\n{VICTORY_MSG}"

        except Exception as e:
            print(f"Ошибка генерации AI для {uid}: {e}")
            yield f"\n\n⚠️ Произошла ошибка: {str(e)}"
        finally:
            if success:
                try:
                    db.add_user_coins_admin(uid, -1)
                except Exception as ex:
                    print(f"Ошибка списания монет у {uid}: {ex}")

    return StreamingResponse(ai_generator(), media_type="text/plain")


# ── CRM и Напоминания 1:1 как в боте (handlers/crm.py) ─────────────────────

from datetime import datetime, timedelta

PARSER_SYSTEM_PROMPT = (
    "Текущее время сервера: {now}.\n"
    "Пользователь напишет задачу с указанием времени.\n"
    "Извлеки суть задачи и точную дату/время срабатывания.\n"
    'Верни СТРОГО валидный JSON: {{"datetime": "YYYY-MM-DD HH:MM:SS", "task": "суть задачи"}}.\n'
    "Никакого лишнего текста, никакого markdown — только JSON."
)


def _parse_crm_ai_response(raw: str, now: datetime) -> tuple[datetime, str] | None:
    """Тот же парсер, что в handlers/crm.py."""
    if raw.startswith("❌"):
        return None
    cleaned = raw.strip()
    json_match = re.search(r"\{.*}", cleaned, re.DOTALL)
    if not json_match:
        return None
    try:
        data = json.loads(json_match.group())
    except json.JSONDecodeError:
        return None
    dt_str = data.get("datetime")
    task = data.get("task")
    if not dt_str or not task:
        return None
    try:
        parsed_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            parsed_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return None
    return parsed_dt, task


@app.post("/api/inleader/crm/add")
async def crm_add(req: CrmAddRequest):
    """Добавить напоминание — та же логика и агент (GROQ_LLAMA), что в handlers/crm.py."""
    uid = req.user_id
    coins = db.get_user_coins(uid)
    if coins is None or coins < 1:
        raise HTTPException(status_code=402, detail="Недостаточно InCoins. Пополните баланс в боте.")
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    system_prompt = PARSER_SYSTEM_PROMPT.format(now=now_str)
    gen = await ai_service.generate_text(
        prompt=req.task_text,
        system_instruction=system_prompt,
        task_type="crm",
        user_id=uid,
    )
    raw = gen.text
    parsed = _parse_crm_ai_response(raw, now)
    if parsed is None:
        return {"ok": False, "error": "parse", "message": t(uid, "crm_parse_error")}
    run_date, task_text = parsed
    if run_date <= now + timedelta(seconds=10):
        return {"ok": False, "error": "past", "message": t(uid, "crm_past_date")}
    run_at_str = run_date.strftime("%Y-%m-%d %H:%M:%S")
    add_crm_reminder(uid, run_at_str, task_text)
    db.add_user_coins_admin(uid, -1)
    formatted_dt = run_date.strftime("%d.%m.%Y в %H:%M")
    return {
        "ok": True,
        "message": t(uid, "crm_confirmed", task=task_text, dt=formatted_dt),
        "run_at": run_at_str,
    }


@app.get("/api/inleader/crm/list")
async def crm_list(user_id: int):
    """Список активных напоминаний — как в handlers/crm.py."""
    reminders = get_user_crm_reminders(user_id)
    return {"reminders": reminders}


def _read_pdf_content(file_path) -> str:
    """Читает текст из PDF (как в handlers/onboarding.py)."""
    try:
        from pypdf import PdfReader
        if not file_path.exists():
            return ""
        reader = PdfReader(str(file_path))
        return "\n".join((p.extract_text() or "") for p in reader.pages).strip()
    except Exception:
        return ""


@app.get("/api/inleader/onboarding/texts")
async def onboarding_texts(user_id: int):
    """Тексты Запуск новичка — без InCruises (маркетинг InLeader)."""
    base = t(user_id, "ob_welcome")
    ob_welcome = base.replace("InCruises", "InLeader").replace("inCruises", "InLeader")
    return {
        "ob_welcome": ob_welcome,
        "ob_tourist": t(user_id, "ob_tourist"),
        "ob_partner": t(user_id, "ob_partner"),
        "ob_navigator": t(user_id, "ob_navigator"),
        "ob_thinking": t(user_id, "ob_thinking"),
        "ob_tourist_welcome": "🏖️ Отличный выбор! Я помогу разобраться с клубными привилегиями. Задай любой вопрос о членстве или переходе в Партнёры:",
        "ob_partner_welcome": "💼 Приветствую, будущий Лидер! Я помогу тебе освоить бизнес-модель и выйти на доход. Задай любой вопрос про маркетинг-план, ранги или первые шаги:",
        "nav_q1": "1️⃣ Какая твоя главная цель на ближайшие 30 дней?",
        "nav_q2": "2️⃣ Какой у тебя опыт в MLM или прямых продажах?",
        "nav_q3": "3️⃣ Сколько времени в неделю готов уделять развитию?",
        "nav_thinking": "⏳ Составляю твой план на 30 дней...",
    }


class RegistrationInstructionRequest(BaseModel):
    user_id: int


@app.post("/api/inleader/registration/instruction")
async def registration_instruction(req: RegistrationInstructionRequest):
    """Пошаговая инструкция по регистрации — 1:1 как handlers/start.py (GROQ_LLAMA)."""
    uid = req.user_id
    coins = db.get_user_coins(uid)
    if coins is None or coins < 1:
        raise HTTPException(status_code=402, detail="Недостаточно InCoins.")
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
    gen = await ai_service.generate_text(
        prompt="Как зарегистрироваться в inCruises?",
        system_instruction=system_prompt,
        task_type="registration",
        user_id=uid,
    )
    db.add_user_coins_admin(uid, -1)
    return {"text": gen.text, "ok": True}


class OnboardingNavigatorRequest(BaseModel):
    user_id: int
    a1: str
    a2: str
    a3: str


@app.post("/api/inleader/onboarding/navigator")
async def onboarding_navigator(req: OnboardingNavigatorRequest):
    """ИИ-Навигатор: план на 30 дней — 1:1 как в handlers/onboarding.py (ARCEE_TRINITY), без InCruises."""
    uid = req.user_id
    coins = db.get_user_coins(uid)
    if coins is None or coins < 1:
        raise HTTPException(status_code=402, detail="Недостаточно InCoins.")
    system_prompt = "Ты — топ-лидер в сетевом маркетинге. На основе ответов пользователя составь краткий, вдохновляющий план действий на первые 30 дней. Структурируй по неделям, добавь конкретные шаги и мотивацию."
    prompt = f"Ответы пользователя:\n1. Главная цель: {req.a1}\n2. Опыт: {req.a2}\n3. Время в неделю: {req.a3}\n\nСоставь персональный план на 30 дней."
    gen = await ai_service.generate_text(
        prompt=prompt,
        system_instruction=system_prompt,
        task_type="onboarding_navigator",
        user_id=uid,
    )
    db.add_user_coins_admin(uid, -1)
    return {"text": gen.text, "ok": True}


@app.get("/api/inleader/mentor/texts")
async def mentor_texts(user_id: int):
    """Тексты AI-Ментор по языку."""
    return {
        "mentor_title": t(user_id, "mentor_title"),
        "mentor_ask": t(user_id, "mentor_ask"),
        "mentor_mindset": t(user_id, "mentor_mindset"),
        "mentor_sales": t(user_id, "mentor_sales"),
        "mentor_coaching": t(user_id, "mentor_coaching"),
        "mentor_management": t(user_id, "mentor_management"),
        "mentor_psychology": t(user_id, "mentor_psychology"),
        "mentor_mlm": t(user_id, "mentor_mlm"),
    }


@app.get("/api/inleader/analytics/texts")
async def analytics_texts(user_id: int):
    """Тексты Аналитик встреч по языку (analyzer_ask, analyzer_thinking)."""
    return {
        "analyzer_ask": t(user_id, "analyzer_ask"),
        "analyzer_thinking": t(user_id, "analyzer_thinking"),
    }


@app.get("/api/inleader/crm/texts")
async def crm_texts(user_id: int):
    """Тексты CRM по языку."""
    return {
        "crm_title": t(user_id, "crm_title"),
        "crm_add_reminder": t(user_id, "crm_add_reminder"),
        "crm_list_reminders": t(user_id, "crm_list_reminders"),
        "crm_ask_task": t(user_id, "crm_ask_task"),
        "crm_thinking": t(user_id, "crm_thinking"),
        "crm_confirmed": t(user_id, "crm_confirmed"),
        "crm_parse_error": t(user_id, "crm_parse_error"),
        "crm_past_date": t(user_id, "crm_past_date"),
        "crm_no_reminders": t(user_id, "crm_no_reminders"),
        "crm_list_header": t(user_id, "crm_list_header"),
    }


# ── Калькулятор 1:1 как в боте (handlers/calculator.py) ─────────────────────

MONTHLY_CONTRIBUTION = 100
REWARD_POINTS_PER_MONTH = 200
CONVERSION_JSON_PROMPT = (
    "Пользователь описывает стоимость круиза и сборов. "
    "Твоя задача — извлечь цифры. "
    'Верни СТРОГО валидный JSON в формате: {"price": 3500, "fees": 350}. '
    'Если сборы не указаны, передай в "fees" 0. '
    "Никакого текста, только JSON."
)


# ── Трекер действий 1:1 как в боте (handlers/tracker.py) ────────────────────

from datetime import date

TASK_LABELS = ("contacts", "followup", "content", "study")
TIMEZONE_OFFSETS = (2, 3, 4, 5, 6, 7, 8)


@app.get("/api/inleader/tracker/data")
async def tracker_get_data(user_id: int):
    """Данные трекера (streak, progress, last_date)."""
    upsert_user(user_id, None)
    data = get_tracker_data(user_id)
    today = date.today().isoformat()
    last_date = data.get("last_tracker_date")
    progress_str = data.get("daily_progress", "0,0,0,0")
    if last_date is None or today > last_date:
        if progress_str != "0,0,0,0":
            progress_str = "0,0,0,0"
            update_daily_progress(user_id, progress_str)
    return {
        "streak": data.get("streak", 0),
        "last_tracker_date": last_date,
        "daily_progress": progress_str,
        "today": today,
    }


@app.get("/api/inleader/tracker/texts")
async def tracker_texts(user_id: int):
    """Тексты трекера по языку."""
    return {
        "trk_title": t(user_id, "trk_title"),
        "trk_contacts": t(user_id, "trk_contacts"),
        "trk_followup": t(user_id, "trk_followup"),
        "trk_content": t(user_id, "trk_content"),
        "trk_study": t(user_id, "trk_study"),
        "trk_finish": t(user_id, "trk_finish"),
        "trk_restart_sprint": t(user_id, "trk_restart_sprint"),
        "trk_done_today": t(user_id, "trk_done_today", streak="__STREAK__"),
        "trk_choose_tz": t(user_id, "trk_choose_tz"),
        "trk_task_done_already": t(user_id, "trk_task_done_already"),
        "trk_report_prompt": t(user_id, "trk_report_prompt", label=""),
        "trk_report_too_short": t(user_id, "trk_report_too_short"),
        "trk_task_accepted": t(user_id, "trk_task_accepted"),
        "trk_sprint_reset": t(user_id, "trk_sprint_reset"),
        "trk_coins_already": t(user_id, "trk_coins_already"),
    }


@app.get("/api/inleader/tracker/timezone")
async def tracker_get_tz(user_id: int):
    tz = get_timezone(user_id)
    return {"timezone": tz, "offsets": list(TIMEZONE_OFFSETS)}


@app.post("/api/inleader/tracker/timezone")
async def tracker_set_tz(req: TrackerTimezoneRequest):
    set_timezone(req.user_id, req.offset)
    return {"status": "ok"}


class TrackerFinishRequest(BaseModel):
    user_id: int


@app.post("/api/inleader/tracker/finish")
async def tracker_finish(req: TrackerFinishRequest):
    user_id = req.user_id
    data = get_tracker_data(user_id)
    progress_str = data.get("daily_progress", "0,0,0,0")
    if "0" in progress_str:
        raise HTTPException(status_code=400, detail="Выполни все задания!")
    result = close_tracker_day(user_id)
    return {"awarded": result["awarded"], "new_streak": result["new_streak"]}


class TrackerResetRequest(BaseModel):
    user_id: int


@app.post("/api/inleader/tracker/reset")
async def tracker_reset(req: TrackerResetRequest):
    user_id = req.user_id
    reset_tracker_sprint(user_id)
    return {"status": "ok"}


@app.post("/api/inleader/tracker/task_report")
async def tracker_task_report(req: TrackerTaskReportRequest):
    """Валидация отчёта через AI (task_type=tracker_report, GROQ_LLAMA)."""
    uid = req.user_id
    if len(req.report_text.strip()) < 5:
        raise HTTPException(status_code=400, detail=t(uid, "trk_report_too_short"))
    data = get_tracker_data(uid)
    progress = data.get("daily_progress", "0,0,0,0").split(",")
    if progress[req.task_id - 1] == "1":
        raise HTTPException(status_code=400, detail=t(uid, "trk_task_done_already"))
    system = (
        "Ты — куратор курса. Оцени отчет студента. Если это просто набор букв или отписка, "
        'ответь "REJECT: Опиши подробнее!". '
        'Если норм, ответь "ACCEPT: Отлично!"'
    )
    gen = await ai_service.generate_text(
        prompt=req.report_text.strip(),
        system_instruction=system,
        task_type="tracker_report",
        user_id=uid,
    )
    ai_text = gen.text
    if "REJECT:" in ai_text.upper():
        reject = ai_text.split("REJECT:")[-1].strip()
        raise HTTPException(status_code=400, detail=f"❌ {reject}")
    progress[req.task_id - 1] = "1"
    update_daily_progress(uid, ",".join(progress))
    return {"status": "accepted"}


@app.get("/api/inleader/marketing/texts")
async def marketing_texts(user_id: int):
    """Тексты для маркетинг-плана (1:1 с ботом)."""
    return {"mkt_ask_prompt": t(user_id, "mkt_ask_prompt")}


@app.get("/api/inleader/calculator/texts")
async def calc_texts(user_id: int):
    """Тексты для калькулятора по языку пользователя (1:1 с ботом)."""
    return {
        "calc_tourist_ask": t(user_id, "calc_tourist_ask"),
        "calc_cruise_ask_price": t(user_id, "calc_cruise_ask_price"),
        "calc_cruise_ask_rp": t(user_id, "calc_cruise_ask_rp"),
        "calc_conversion_ask": t(user_id, "calc_conversion_ask"),
        "calc_bad_number": t(user_id, "calc_bad_number"),
    }


@app.get("/api/inleader/calculator/free")
async def calc_free(user_id: int):
    """Безоплатное членство — только текст, без AI."""
    text = t(user_id, "calc_free_member_text")
    return {"text": text}


@app.post("/api/inleader/calculator/tourist")
async def calc_tourist(req: CalcTouristRequest):
    """Калькулятор туриста — 1:1 с ботом."""
    months = max(1, min(120, req.months))
    total_paid = months * MONTHLY_CONTRIBUTION
    total_points = months * REWARD_POINTS_PER_MONTH

    lines = [t(req.user_id, "calc_tourist_header"), ""]
    running_paid, running_points = 0, 0
    for m in range(1, months + 1):
        running_paid += MONTHLY_CONTRIBUTION
        running_points += REWARD_POINTS_PER_MONTH
        lines.append(t(req.user_id, "calc_tourist_row", month=str(m), paid=f"${running_paid}", points=str(running_points)))
    lines.append("")
    lines.append(t(req.user_id, "calc_tourist_total", total_paid=f"${total_paid}", total_points=str(total_points)))
    lines.append("")
    lines.append(t(req.user_id, "calc_tourist_tip"))

    img_b64 = None
    try:
        lang = get_language(req.user_id)
        img_bytes = await asyncio.to_thread(generate_tourist_receipt, months, total_paid, total_points, lang)
        img_b64 = base64.b64encode(img_bytes).decode()
    except Exception as e:
        print(f"Tourist receipt image error: {e}")

    return {"text": "\n".join(lines), "image": img_b64, "caption": t(req.user_id, "calc_image_caption")}


@app.post("/api/inleader/calculator/cruise")
async def calc_cruise(req: CalcCruiseRequest):
    """Расчёт круиза ББ — 1:1 с ботом."""
    cruise_price = max(0.01, req.price)
    user_rp = max(0, req.rp)

    insider_price = cruise_price * (1 - INSIDER_DISCOUNT_PCT / 100)
    insider_save = cruise_price - insider_price
    max_rp_cover = cruise_price * (MAX_RP_COVERAGE_PCT / 100)
    rp_usable = min(user_rp * RP_VALUE_USD, max_rp_cover)
    rp_used_points = int(rp_usable / RP_VALUE_USD)
    cash_needed = cruise_price - rp_usable
    total_savings = rp_usable
    covers_full_50 = (user_rp * RP_VALUE_USD) >= max_rp_cover

    def fmt(val: float) -> str:
        return f"{val:,.2f}"

    lines = [t(req.user_id, "calc_cruise_header"), ""]
    lines.append(t(req.user_id, "calc_cruise_listed", price=fmt(cruise_price)))
    lines.append(t(req.user_id, "calc_cruise_insider", price=fmt(insider_price), save=fmt(insider_save)))
    lines.append("")
    lines.append(t(req.user_id, "calc_cruise_rp_avail", rp=str(user_rp), value=fmt(user_rp * RP_VALUE_USD)))
    if covers_full_50:
        lines.append(t(req.user_id, "calc_cruise_rp_usable", rp=str(rp_used_points), value=fmt(rp_usable)))
    else:
        lines.append(t(req.user_id, "calc_cruise_rp_not_enough", rp=str(user_rp)))
    lines.append(t(req.user_id, "calc_cruise_cash", cash=fmt(cash_needed)))
    lines.append(t(req.user_id, "calc_cruise_savings", save=fmt(total_savings)))
    lines.append("")
    lines.append(t(req.user_id, "calc_cruise_booking_tip"))
    lines.append("")
    lines.append(t(req.user_id, "calc_cruise_partner_tip"))

    img_b64 = None
    try:
        lang = get_language(req.user_id)
        img_bytes = await asyncio.to_thread(
            generate_cruise_receipt, cruise_price, rp_used_points, cash_needed, total_savings, lang
        )
        img_b64 = base64.b64encode(img_bytes).decode()
    except Exception as e:
        print(f"Cruise receipt image error: {e}")

    return {"text": "\n".join(lines), "image": img_b64, "caption": t(req.user_id, "calc_image_caption")}


@app.post("/api/inleader/calculator/conversion")
async def calc_conversion(req: CalcConversionRequest):
    """Конвертация ББ — AI извлекает цифры (task_type=general), 1:1 с ботом."""
    uid = req.user_id
    coins = db.get_user_coins(uid)
    if coins is None or coins < 1:
        raise HTTPException(status_code=402, detail="Недостаточно InCoins.")

    gen = await ai_service.generate_text(
        prompt=req.text,
        system_instruction=CONVERSION_JSON_PROMPT,
        task_type="general",
        user_id=uid,
    )
    raw = gen.text

    parsed = None
    if not raw.startswith("❌"):
        match = re.search(r"\{[^{}]*\}", raw)
        if match:
            try:
                parsed = json.loads(match.group())
            except json.JSONDecodeError:
                pass

    if parsed is None:
        raise HTTPException(status_code=400, detail=t(uid, "calc_conversion_parse_error"))

    price = float(parsed.get("price", 0))
    fees = float(parsed.get("fees", 0))
    if fees == 0:
        fees = price * 0.10
    if price <= 0:
        raise HTTPException(status_code=400, detail=t(uid, "calc_bad_number"))

    standard_points = price / 2
    converted_points = standard_points * 2
    subtotal = standard_points + converted_points
    final_total = subtotal + fees

    receipt = t(
        uid, "calc_conversion_receipt",
        price=f"{price:,.0f}",
        standard_points=f"{standard_points:,.0f}",
        converted_points=f"{converted_points:,.0f}",
        subtotal=f"{subtotal:,.0f}",
        fees=f"{fees:,.0f}",
        final_total=f"{final_total:,.0f}",
    )

    img_b64 = None
    try:
        lang = get_language(uid)
        img_bytes = await asyncio.to_thread(
            generate_conversion_receipt, price, standard_points, converted_points, fees, final_total, lang
        )
        img_b64 = base64.b64encode(img_bytes).decode()
    except Exception as e:
        print(f"Conversion receipt image error: {e}")

    try:
        db.add_user_coins_admin(uid, -1)
    except Exception as ex:
        print(f"Coin deduct error: {ex}")

    return {"text": receipt, "image": img_b64, "caption": t(uid, "calc_image_caption")}


if __name__ == "__main__":
    import uvicorn
    # ВНИМАНИЕ: Порт 9000 специально для проекта InLeader!
    uvicorn.run(app, host="127.0.0.1", port=9000)
