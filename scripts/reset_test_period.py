"""
Однократный сброс тестового периода для всех пользователей.
Устанавливает incoins = 5 (как при первом входе) для всех, кроме администратора.

Запуск: python scripts/reset_test_period.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv

load_dotenv()

from services.db import init_db, reset_test_period_for_all

if __name__ == "__main__":
    init_db()
    admin_id = int(os.getenv("ADMIN_ID", "5925660014"))
    n = reset_test_period_for_all(admin_id)
    print(f"Тестовый период сброшен. Обновлено пользователей: {n}")
