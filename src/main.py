"""
Основной модуль Telegram-бота «Криптобезопасный помощник».

Команды:
  /start     — приветствие и список команд
  /help      — подробная справка
  /password  — генерация пароля (с параметрами)
  /check     — анализ сообщения на признаки мошенничества
  /schemes   — список известных мошеннических схем
  /stats     — статистика проверок

Запуск:
    python -m src.main
или:
    python src/main.py
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from config import BOT_TOKEN, LOG_FILE, DEFAULT_PASSWORD_LENGTH
from fraud_detector import analyze_message, list_schemes, get_scheme_info
from password_engine import generate_password, assess_strength

# --- Логирование ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# --- Инициализация бота ---
if not BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN не задан! "
                 "Установите переменную окружения или заполните .env файл.")
    sys.exit(1)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
) 
dp = Dispatcher()


# --- Утилиты ---
def _load_log() -> list[dict]:
    """Загружает лог проверок из JSON-файла."""
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def _append_log(entry: dict) -> None:
    """Добавляет запись в лог проверок."""
    log = _load_log()
    log.append(entry)
    Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def _strength_emoji(score: int) -> str:
    """Возвращает эмодзи по баллу стойкости."""
    if score >= 80:
        return "🟢"
    if score >= 50:
        return "🟡"
    if score >= 25:
        return "🟠"
    return "🔴"


def _level_emoji(level: str) -> str:
    """Возвращает эмодзи по уровню опасности."""
    emojis = {
        "Безопасно": "🟢",
        "Подозрительно": "🟡",
        "Опасно": "🟠",
        "Критично": "🔴",
    }
    return emojis.get(level, "⚪")


# --- Команды ---

@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Приветствие и список команд."""
    text = (
        "🔐 <b>Криптобезопасный помощник</b>\n\n"
        "Я помогу защитить вас от двух главных угроз в интернете: "
        "слабых паролей и мошенников.\n\n"
        "<b>Что я умею:</b>\n"
        "🔑 <b>/password</b> — сгенерировать надёжный пароль\n"
        "🔍 <b>/check</b> — проверить сообщение на мошенничество\n"
        "📋 <b>/schemes</b> — список известных схем мошенников\n"
        "📊 <b>/stats</b> — статистика ваших проверок\n"
        "❓ <b>/help</b> — подробная справка\n\n"
        "Отправьте сообщение, чтобы проверить его на признаки мошенничества."
    )

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔑 Сгенерировать пароль"), KeyboardButton(text="🔍 Проверить сообщение")],
            [KeyboardButton(text="📋 Схемы мошенничества"), KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="❓ Помощь")],
        ],
        resize_keyboard=True,
    )
    await message.answer(text, reply_markup=keyboard)


@dp.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Подробная справка."""
    text = (
        "❓ <b>Справка</b>\n\n"
        "<b>🔑 Генерация пароля</b>\n"
        "Команда: <code>/password</code>\n"
        "Параметры (через пробел):\n"
        "  • длина (число от 4 до 64, по умолчанию 16)\n"
        "  • <code>nosym</code> — без спецсимволов\n"
        "  • <code>noupp</code> — без заглавных\n"
        "  • <code>nodig</code> — без цифр\n"
        "  • <code>nosim</code> — исключить похожие (il1Lo0O)\n\n"
        "Примеры:\n"
        "  <code>/password</code> — пароль по умолчанию (16 символов)\n"
        "  <code>/password 20</code> — пароль длиной 20\n"
        "  <code>/password 12 nosym</code> — 12 символов без спецсимволов\n\n"
        "Также можно просто отправить свой пароль, и я оценю его стойкость.\n\n"
        "<b>🔍 Проверка сообщения</b>\n"
        "Команда: <code>/check</code> + текст сообщения\n"
        "Или просто перешлите подозрительное сообщение боту.\n\n"
        "<b>📋 Схемы</b>\n"
        "Команда: <code>/schemes</code> — список известных мошеннических схем.\n\n"
        "<b>📊 Статистика</b>\n"
        "Команда: <code>/stats</code> — сколько сообщений проверено."
    )
    await message.answer(text)


@dp.message(Command("password"))
async def cmd_password(message: Message) -> None:
    """
    Генерация пароля.
    Парсит параметры из текста команды.
    """
    args = message.text.split()[1:]  # убираем саму команду

    length = DEFAULT_PASSWORD_LENGTH
    use_upper = True
    use_digits = True
    use_symbols = True
    exclude_similar = False

    for arg in args:
        if arg.isdigit():
            length = int(arg)
        elif arg == "nosym":
            use_symbols = False
        elif arg == "noupp":
            use_upper = False
        elif arg == "nodig":
            use_digits = False
        elif arg == "nosim":
            exclude_similar = True

    result = generate_password(
        length=length,
        use_upper=use_upper,
        use_digits=use_digits,
        use_symbols=use_symbols,
        exclude_similar=exclude_similar,
    )

    text = (
        f"{_strength_emoji(result.strength_score)} <b>Сгенерирован пароль</b>\n\n"
        f"<code>{result.password}</code>\n\n"
        f"📏 Длина: <b>{result.length}</b> символов\n"
        f"🧮 Энтропия: <b>{result.entropy}</b> бит\n"
        f"⏱ Время взлома: <b>{result.crack_time}</b>\n"
        f"📊 Оценка: <b>{result.strength}</b> ({result.strength_score}/100)"
    )
    await message.answer(text)


@dp.message(Command("check"))
async def cmd_check(message: Message) -> None:
    """Анализ сообщения на мошенничество."""
    # Берём текст после команды
    text_to_check = message.text.partition(" ")[2].strip()

    if not text_to_check:
        await message.answer(
            "🔍 Отправьте сообщение для проверки.\n\n"
            "Пример: <code>/check Здравствуйте, ваш сын попал в больницу, срочно переведите 50000</code>\n\n"
            "Или просто перешлите подозрительное сообщение."
        )
        return

    await _run_analysis(message, text_to_check)


@dp.message(Command("schemes"))
async def cmd_schemes(message: Message) -> None:
    """Список известных мошеннических схем."""
    schemes = list_schemes()
    lines = ["📋 <b>Известные мошеннические схемы</b>\n"]
    for i, scheme in enumerate(schemes, 1):
        lines.append(f"<b>{i}. {scheme['name']}</b>\n{scheme['description']}\n")
    lines.append(
        "Используйте /check &lt;текст&gt; для проверки сообщения "
        "на соответствие этим схемам."
    )
    await message.answer("\n".join(lines))


@dp.message(Command("stats"))
async def cmd_stats(message: Message) -> None:
    """Статистика проверок."""
    log = _load_log()
    total = len(log)

    if total == 0:
        await message.answer("📊 Статистика пуста. Вы ещё не проверяли сообщения.")
        return

    # Считаем распределение по уровням
    levels = {"Безопасно": 0, "Подозрительно": 0, "Опасно": 0, "Критично": 0}
    for entry in log:
        level = entry.get("level", "Безопасно")
        if level in levels:
            levels[level] += 1

    text = (
        f"📊 <b>Статистика проверок</b>\n\n"
        f"Всего проверено: <b>{total}</b>\n"
        f"🟢 Безопасно: <b>{levels['Безопасно']}</b>\n"
        f"🟡 Подозрительно: <b>{levels['Подозрительно']}</b>\n"
        f"🟠 Опасно: <b>{levels['Опасно']}</b>\n"
        f"🔴 Критично: <b>{levels['Критично']}</b>"
    )
    await message.answer(text)


# --- Обработка текстовых сообщений ---

@dp.message(F.text)
async def handle_text(message: Message) -> None:
    """
    Обрабатывает任意 текст:
    - Если есть кнопки клавиатуры — реагирует на них
    - Короткий текст (одно слово) — проверяет как пароль
    - Длинный текст — анализирует на мошенничество
    """
    text = message.text.strip()

    # --- Реакция на кнопки ---
    if text == "🔑 Сгенерировать пароль":
        await cmd_password(message)
        return
    if text == "🔍 Проверить сообщение":
        await message.answer(
            "🔍 Отправьте или перешлите подозрительное сообщение, "
            "и я проверю его на признаки мошенничества."
        )
        return
    if text == "📋 Схемы мошенничества":
        await cmd_schemes(message)
        return
    if text == "📊 Статистика":
        await cmd_stats(message)
        return
    if text == "❓ Помощь":
        await cmd_help(message)
        return

    # --- Логика автоопределения ---
    # Длинный текст (>30 символов) — проверяем как сообщение на мошенничество
    if len(text) > 30:
        await _run_analysis(message, text)
        return

    # Короткий текст без пробелов — проверяем как пароль
    if " " not in text and len(text) >= 3:
        await _assess_password(message, text)
        return

    # Промежуточный случай — спрашиваем
    await message.answer(
        "Я не уверен, что вы хотите сделать.\n"
        "Используйте /password для генерации пароля "
        "или /check для проверки сообщения."
    )


# --- Вспомогательные функции ---

async def _run_analysis(message: Message, text: str) -> None:
    """Анализирует текст на мошенничество и отправляет результат."""
    result = analyze_message(text)

    lines = [
        f"{_level_emoji(result.level)} <b>Анализ сообщения</b>\n",
        f"Уровень риска: <b>{result.level}</b> ({result.score}/100)\n",
    ]

    if result.found_signs:
        lines.append("<b>Найденные признаки:</b>")
        for sign in result.found_signs:
            lines.append(f"  • {sign['description']} (вес: {sign['weight']})")
        lines.append("")

    if result.matched_schemes:
        lines.append("<b>Совпавшие схемы:</b>")
        for scheme in result.matched_schemes:
            lines.append(f"  📌 {scheme['name']}")
            lines.append(f"  {scheme['what_to_do']}")
            lines.append("")

    lines.append(f"💡 <b>Рекомендация:</b>\n{result.recommendation}")

    await message.answer("\n".join(lines))

    # Запись в лог
    _append_log({
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "user_id": message.from_user.id if message.from_user else None,
        "text": text[:500],  # ограничиваем длину для лога
        "score": result.score,
        "level": result.level,
    })


async def _assess_password(message: Message, password: str) -> None:
    """Оценивает стойкость пароля и отправляет результат."""
    result = assess_strength(password)

    lines = [
        f"{_strength_emoji(result.strength_score)} <b>Анализ пароля</b>\n",
        f"🧮 Энтропия: <b>{result.entropy}</b> бит",
        f"⏱ Время взлома: <b>{result.crack_time}</b>",
        f"📊 Оценка: <b>{result.strength}</b> ({result.strength_score}/100)\n",
    ]

    if result.issues:
        lines.append("⚠️ <b>Проблемы:</b>")
        for issue in result.issues:
            lines.append(f"  • {issue}")
        lines.append("")

    if result.tips:
        lines.append("💡 <b>Советы:</b>")
        for tip in result.tips:
            lines.append(f"  • {tip}")

    await message.answer("\n".join(lines))


# --- Запуск ---

async def main() -> None:
    """Точка входа бота."""
    logger.info("Бот запускается...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())