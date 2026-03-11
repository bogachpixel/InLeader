from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import json

# Импортируем ваши существующие сервисы
from services import db
from services.ai_service import generate_text_stream # Предположим, вы добавите стриминг

app = FastAPI()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    section: str
    buttonContext: Optional[str] = None
    user_id: int

@app.get("/api/inleader/profile/{user_id}")
async def get_profile(user_id: int):
    """Возвращает данные пользователя из SQLite."""
    coins = db.get_user_coins(user_id)
    # Можно добавить другие данные: streak, score и т.д.
    return {
        "user_id": user_id,
        "incoins": coins,
        "is_authorized": True # Т.к. зашел через WebApp
    }

@app.post("/api/inleader/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Эндпоинт для чата. 
    1. Проверяет баланс.
    2. Списывает 1 InCoin.
    3. Генерирует ответ через AI.
    """
    uid = request.user_id
    
    # 1. Проверка баланса (как в боте)
    coins = db.get_user_coins(uid)
    if coins < 1:
        raise HTTPException(status_code=402, detail="Недостаточно InCoins")

    # 2. Списание монеты
    db.add_user_coins_admin(uid, -1)

    # 3. Логика генерации (адаптируйте под ваш ai_service)
    # Здесь пример того, как вызвать ваш существующий ИИ-движок
    async def ai_generator():
        prompt = request.messages[-1].content
        system_prompt = f"Раздел: {request.section}. Контекст: {request.buttonContext}"
        
        # Вызываем ваш генератор (нужно будет сделать его асинхронным генератором)
        async for chunk in db_and_ai_stream(prompt, system_prompt, uid, request.section):
            yield chunk

    return StreamingResponse(ai_generator(), media_type="text/plain")

async def db_and_ai_stream(prompt, system_prompt, uid, task_type):
    """
    Вспомогательная функция, которая связывает ваш ai_service 
    со стримингом FastAPI.
    """
    from services.ai_service import model
    
    # Пример вызова Gemini в режиме потока
    response = model.generate_content(
        contents=[{"role": "user", "parts": [{"text": f"{system_prompt}\n\nUser: {prompt}"}]}],
        stream=True
    )
    
    for chunk in response:
        if chunk.text:
            yield chunk.text

# ВАЖНО: Не забудьте настроить CORS, чтобы фронтенд мог слать запросы
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # В продакшене укажите ['https://in-leader.ru']
    allow_methods=["*"],
    allow_headers=["*"],
)
