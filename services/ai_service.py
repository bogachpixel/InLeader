import logging
import os
from dataclasses import dataclass
import aiohttp
from dotenv import load_dotenv
from groq import AsyncGroq
from openai import AsyncOpenAI

# Загружаем переменные окружения в самом начале
load_dotenv()

logger = logging.getLogger(__name__)

# Проверка загрузки ключей (выводится в консоль при запуске)
_groq_key = os.getenv("GROQ_API_KEY")
_or_key = os.getenv("OPENROUTER_API_KEY")

print(f"DEBUG: Groq Key loaded: {bool(_groq_key)}")
print(f"DEBUG: OpenRouter Key loaded: {bool(_or_key)}")

if not _groq_key or not _or_key:
    logger.error("КРИТИЧЕСКАЯ ОШИБКА: API-ключи не найдены в .env файле!")

# Клиенты
groq_client = AsyncGroq(api_key=_groq_key)
or_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=_or_key,
)

# Маршрутизация моделей
_DEEPSEEK = {"client": or_client, "model": "deepseek/deepseek-chat"}
_GROQ_LLAMA = {"client": groq_client, "model": "llama-3.1-8b-instant"}
_GEMINI = {"client": or_client, "model": "google/gemini-2.0-flash-001"}
_CLAUDE_HAIKU = {"client": or_client, "model": "anthropic/claude-3.5-haiku"}
_GPT5_NANO = {"client": or_client, "model": "openai/gpt-5-nano"}
_ARCEE_TRINITY = {"client": or_client, "model": "arcee-ai/trinity-large-preview:free"}
_GPT_OSS_120B = {"client": or_client, "model": "openai/gpt-oss-120b"}
_QWEN_FLASH = {"client": or_client, "model": "qwen/qwen3.5-flash-02-23"}

_ROUTES: dict[str, dict] = {
    "objections": _DEEPSEEK,
    "analyzer": _DEEPSEEK,
    "calculator": _DEEPSEEK,
    "simulator": _CLAUDE_HAIKU,
    "copywriter": _GEMINI,
    "onboarding": _GEMINI,
    "onboarding_chat": _ARCEE_TRINITY,
    "onboarding_navigator": _ARCEE_TRINITY,
    "registration": _GROQ_LLAMA,
    "crm": _GROQ_LLAMA,
    "marketing": _GPT5_NANO,
    "general": _GEMINI,
    "parser": _GEMINI,
    "tracker_report": _GROQ_LLAMA,
}

MAX_HISTORY_MESSAGES = 10


@dataclass
class GenResult:
    text: str
    model: str
    cost: float | None


def format_admin_footer(gen: "GenResult", user_id: int) -> str:
    """Возвращает строку с агентом и стоимостью только для админа."""
    admin_id = int(os.getenv("ADMIN_ID", "0"))
    if user_id != admin_id:
        return ""
    cost_str = f"${gen.cost:.6f}" if gen.cost is not None else "—"
    return f"\n\n📊 Агент: {gen.model}\n💰 Стоимость: {cost_str}"


async def generate_text(
    prompt: str,
    system_instruction: str,
    task_type: str = "general",
    history: list[dict[str, str]] | None = None,
    user_id: int | None = None,
) -> GenResult:
    """Маршрутизирует запрос в нужную модель. Возвращает GenResult(text, model, cost)."""
    route = _ROUTES.get(task_type, _ROUTES["general"])
    client = route["client"]
    model = route["model"]

    messages = [{"role": "system", "content": system_instruction}]
    if history:
        messages.extend(history[-MAX_HISTORY_MESSAGES:])
    messages.append({"role": "user", "content": prompt})

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            timeout=60
        )
        text = response.choices[0].message.content
        if not text:
            return GenResult("⚠️ Ошибка: Нейросеть вернула пустой ответ. Попробуйте еще раз.", model, None)
        usage = getattr(response, "usage", None)
        cost = None
        if usage:
            cost = getattr(usage, "total_cost", None) or getattr(usage, "cost", None)
            if cost is not None:
                try:
                    cost = float(cost)
                except (TypeError, ValueError):
                    cost = None
        if user_id is not None:
            try:
                from services.db import log_usage
                log_usage(user_id, task_type, model, cost)
            except Exception as log_err:
                logger.warning("usage log failed: %s", log_err)
        return GenResult(text=text, model=model, cost=cost)
    except Exception as e:
        logger.exception(f"AI error [{model}]: {e}")
        return GenResult(f"⚠️ Ошибка связи с ИИ: {str(e)[:100]}. Проверьте API-ключи.", model, None)


async def generate_text_stream(
    prompt: str,
    system_instruction: str,
    task_type: str = "general",
    history: list[dict[str, str]] | None = None,
) -> "AsyncIterator[str]":
    """Стримит ответ чанками. Используется для API чата (сайт)."""
    route = _ROUTES.get(task_type, _ROUTES["general"])
    client = route["client"]
    model = route["model"]

    messages = [{"role": "system", "content": system_instruction}]
    if history:
        messages.extend(history[-MAX_HISTORY_MESSAGES:])
    messages.append({"role": "user", "content": prompt})

    stream = await client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
        timeout=60,
    )
    async for chunk in stream:
        delta = chunk.choices[0].delta if chunk.choices else None
        if delta and getattr(delta, "content", None):
            yield delta.content

IMAGE_FORMAT_REELS = "9:16"
IMAGE_FORMAT_POST = "16:9"

# Модели для админ-генерации картинок (OpenRouter)
IMAGE_MODELS = {
    "nanobanana": {"id": "google/gemini-3.1-flash-image-preview", "modalities": ["image", "text"], "name": "Nano Banana 2 (Gemini 3.1 Flash Image Preview)"},
    "flux": {"id": "black-forest-labs/flux.2-pro", "modalities": ["image"], "name": "Flux.1 (Pro/Dev)"},
    "gemini25flash": {"id": "google/gemini-2.5-flash-image", "modalities": ["image", "text"], "name": "Gemini 2.5 Flash Image"},
    "riverflow_fast": {"id": "sourceful/riverflow-v2-fast", "modalities": ["image"], "name": "Riverflow V2 Fast"},
    "riverflow_std": {"id": "sourceful/riverflow-v2-standard-preview", "modalities": ["image"], "name": "Riverflow V2 Standard Preview"},
    "flux2pro": {"id": "black-forest-labs/flux.2-pro", "modalities": ["image"], "name": "Flux 2 Pro"},
}

async def generate_image_ai(prompt: str, aspect_ratio: str = "1:1", model_key: str = "nanobanana") -> tuple[bytes | None, float | None]:
    """Генерирует картинку по текстовому запросу через выбранную модель (OpenRouter).
    Возвращает (bytes, cost) или (None, None) при ошибке.
    """
    import base64
    if not _or_key:
        logger.error("OPENROUTER_API_KEY не задан для генерации картинок")
        return (None, None)
    cfg = IMAGE_MODELS.get(model_key, IMAGE_MODELS["nanobanana"])
    model_id = cfg["id"]
    modalities = cfg.get("modalities", ["image", "text"])
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {_or_key}",
        "Content-Type": "application/json",
    }
    format_hint = " (строго вертикальная композиция 9:16, как для Reels)" if aspect_ratio == "9:16" else " (строго горизонтальная композиция 16:9, как для поста)" if aspect_ratio == "16:9" else ""
    enhanced_prompt = prompt + format_hint
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": enhanced_prompt}],
        "modalities": modalities,
        "image_config": {"aspect_ratio": aspect_ratio},
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=90)) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    logger.error(f"OpenRouter image gen error {resp.status}: {text[:300]}")
                    return (None, None)
                data = await resp.json()
        choices = data.get("choices") or []
        if not choices:
            return (None, None)
        msg = choices[0].get("message") or {}
        images = msg.get("images") or []
        if not images:
            return (None, None)
        img_obj = images[0]
        url_field = img_obj.get("image_url") or img_obj.get("imageUrl") or {}
        data_url = url_field.get("url", "")
        if not data_url:
            return (None, None)
        if "," in data_url:
            b64 = data_url.split(",", 1)[1]
        else:
            b64 = data_url
        img_bytes = base64.b64decode(b64)
        usage = data.get("usage") or {}
        cost = usage.get("cost")
        if cost is not None:
            try:
                cost = float(cost)
            except (TypeError, ValueError):
                cost = None
        return (img_bytes, cost)
    except Exception as e:
        logger.exception(f"Image gen error: {e}")
        return (None, None)


async def generate_image(prompt: str) -> str | None:
    """Генерирует визуальный креатив через Unsplash (стабильно) на основе темы."""
    try:
        import urllib.parse
        keywords = prompt[:50].replace(" ", ",")
        # Возвращаем качественное фото по ключевым словам из промпта
        return f"https://source.unsplash.com/1200x800/?cruise,travel,luxury,{urllib.parse.quote(keywords)}"
    except Exception as e:
        logger.error(f"Image generation fallback failed: {e}")
        return None


async def download_image_bytes(url: str) -> bytes | None:
    """Скачивает изображение по URL и возвращает байты. Возвращает None при ошибке."""
    if not url or not url.startswith("http"):
        return None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status == 200:
                    return await resp.read()
                print(f"Ошибка скачивания фото: статус {resp.status}")
    except Exception as e:
        print(f"Не удалось скачать фото: {e}")
    return None
