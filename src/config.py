"""
Конфигурация бота.

Токен загружается из переменной окружения TELEGRAM_BOT_TOKEN
или из файла .env (через python-dotenv).
"""

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv не обязателен, если токен в переменной окружения


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Настройки по умолчанию
DEFAULT_PASSWORD_LENGTH = 16
MAX_PASSWORD_LENGTH = 64
MIN_PASSWORD_LENGTH = 4

# Путь к файлу логов проверенных сообщений
LOG_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "check_log.json",
)