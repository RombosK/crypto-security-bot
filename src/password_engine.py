"""
Модуль генерации и оценки паролей.

Содержит:
- generate_password() — генерация пароля заданной длины с настройками символов
- calculate_entropy() — расчёт энтропии пароля в битах
- estimate_crack_time() — оценка времени взлома перебором
- assess_strength() — комплексная оценка стойкости пароля
"""

import math
import random
import string
from dataclasses import dataclass, field
from typing import List


# Наборы символов
LOWER = string.ascii_lowercase           # a-z
UPPER = string.ascii_uppercase           # A-Z
DIGITS = string.digits                   # 0-9
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?/"     # специальные символы
SIMILAR = "il1Lo0O"                      # похожие символы (можно исключить)

# Базовая скорость перебора (попыток в секунду)
# Для учебного проекта берём 10 млрд/сек — оценка современной атаки по хешу
ATTEMPTS_PER_SECOND = 1e10


@dataclass
class PasswordResult:
    """Результат генерации пароля."""
    password: str
    length: int
    entropy: float                       # в битах
    crack_time: str                      # человекочитаемая строка
    strength: str                        # "Очень слабый" / "Слабый" / "Средний" / "Сильный" / "Очень сильный"
    strength_score: int                  # 0-100


@dataclass
class StrengthAssessment:
    """Результат оценки существующего пароля."""
    entropy: float
    crack_time: str
    strength: str
    strength_score: int
    issues: List[str] = field(default_factory=list)
    tips: List[str] = field(default_factory=list)


def _calculate_charset_size(password: str) -> int:
    """
    Определяет размер алфавита пароля по фактически использованным символам.
    Чем больше разных классов символов — тем выше энтропия.
    """
    size = 0
    if any(c in LOWER for c in password):
        size += len(LOWER)
    if any(c in UPPER for c in password):
        size += len(UPPER)
    if any(c in DIGITS for c in password):
        size += len(DIGITS)
    if any(c in SYMBOLS for c in password):
        size += len(SYMBOLS)
    # Если ни один класс не определился (нестандартные символы)
    if size == 0:
        size = len(set(password))
    return size


def calculate_entropy(password: str) -> float:
    """
    Считает энтропию пароля по формуле Шеннона:
        H = L * log2(R)
    где L — длина пароля, R — размер алфавита.
    """
    if not password:
        return 0.0
    charset_size = _calculate_charset_size(password)
    return len(password) * math.log2(charset_size)


def estimate_crack_time(entropy: float) -> str:
    """
    Оценивает время полного перебора:
        T = 2^H / 2 / attempts_per_second
    (делим на 2 — в среднем ответ находится на половине перебора)
    Возвращает человекочитаемую строку.
    """
    if entropy <= 0:
        return "мгновенно"

    seconds = (2 ** entropy) / 2 / ATTEMPTS_PER_SECOND

    if seconds < 1:
        return "мгновенно"
    if seconds < 60:
        return f"{seconds:.0f} секунд"
    if seconds < 3600:
        return f"{seconds / 60:.0f} минут"
    if seconds < 86400:
        return f"{seconds / 3600:.1f} часов"
    if seconds < 86400 * 365:
        return f"{seconds / 86400:.1f} дней"
    if seconds < 86400 * 365 * 1000:
        return f"{seconds / (86400 * 365):.1f} лет"
    if seconds < 86400 * 365 * 1e6:
        return f"{seconds / (86400 * 365 * 1000):.1f} тысяч лет"
    if seconds < 86400 * 365 * 1e9:
        return f"{seconds / (86400 * 365 * 1e6):.1f} миллионов лет"
    return "миллиарды лет"


def _entropy_to_strength(entropy: float) -> tuple[str, int]:
    """
    Преобразует энтропию в текстовую оценку и балл 0-100.
    Шкала основана на общепринятых рекомендациях:
      < 28 бит  — очень слабый (4-значный PIN)
      < 36 бит  — слабый        (6 букв)
      < 60 бит  — средний        (8 символов смешанных)
      < 80 бит  — сильный        (12+ символов)
      >= 80 бит — очень сильный  (16+ символов)
    """
    if entropy < 28:
        return "Очень слабый", 10
    if entropy < 36:
        return "Слабый", 25
    if entropy < 60:
        return "Средний", 50
    if entropy < 80:
        return "Сильный", 75
    return "Очень сильный", 100


def generate_password(
    length: int = 16,
    use_upper: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
    exclude_similar: bool = False,
) -> PasswordResult:
    """
    Генерирует случайный пароль заданной длины и состава символов.

    Использует random.SystemRandom() — криптостойкий источник случайности
    из ОС (на Linux это /dev/urandom).

    Args:
        length:           длина пароля (4-64)
        use_upper:        включать заглавные буквы
        use_digits:       включать цифры
        use_symbols:      включать спецсимволы
        exclude_similar:  исключить похожие символы (il1Lo0O)

    Returns:
        PasswordResult с паролем и метриками
    """
    length = max(4, min(length, 64))

    # Собираем алфавит
    charset = LOWER
    if use_upper:
        charset += UPPER
    if use_digits:
        charset += DIGITS
    if use_symbols:
        charset += SYMBOLS
    if exclude_similar:
        charset = "".join(c for c in charset if c not in SIMILAR)

    rng = random.SystemRandom()
    password = "".join(rng.choice(charset) for _ in range(length))

    entropy = calculate_entropy(password)
    crack_time = estimate_crack_time(entropy)
    strength, score = _entropy_to_strength(entropy)

    return PasswordResult(
        password=password,
        length=length,
        entropy=round(entropy, 1),
        crack_time=crack_time,
        strength=strength,
        strength_score=score,
    )


def assess_strength(password: str) -> StrengthAssessment:
    """
    Комплексная оценка существующего пароля.

    Проверяет:
    - энтропию и время взлома
    - длину
    - наличие классов символов
    - словарные слова и простые паттерны
    - повторяющиеся и последовательные символы

    Возвращает StrengthAssessment с метриками, проблемами и советами.
    """
    issues: List[str] = []
    tips: List[str] = []

    # --- Проверка длины ---
    if len(password) < 8:
        issues.append("Слишком короткий пароль (меньше 8 символов)")
        tips.append("Увеличьте длину хотя бы до 12 символов")
    elif len(password) < 12:
        tips.append("Хорошо, но 12+ символов надёжнее")

    # --- Проверка классов символов ---
    has_lower = any(c in LOWER for c in password)
    has_upper = any(c in UPPER for c in password)
    has_digit = any(c in DIGITS for c in password)
    has_symbol = any(c in SYMBOLS for c in password)
    classes_count = sum([has_lower, has_upper, has_digit, has_symbol])

    if not has_upper:
        issues.append("Нет заглавных букв")
        tips.append("Добавьте заглавные буквы")
    if not has_digit:
        issues.append("Нет цифр")
        tips.append("Добавьте цифры")
    if not has_symbol:
        issues.append("Нет спецсимволов")
        tips.append("Добавьте спецсимволы (!@#$ и т.д.)")
    if classes_count < 3:
        issues.append(f"Использован только {classes_count} класс символов из 4")

    # --- Простые паттерны ---
    # Одинаковые символы подряд (aaa, 111)
    has_repeats = any(
        password[i] == password[i + 1] == password[i + 2]
        for i in range(len(password) - 2)
    )
    if has_repeats:
        issues.append("Есть повторяющиеся символы (например, «aaa»)")
        tips.append("Избегайте повторений одинаковых символов")

    # Последовательности (abc, 123)
    has_sequence = False
    for i in range(len(password) - 2):
        a, b, c = ord(password[i]), ord(password[i + 1]), ord(password[i + 2])
        if b - a == 1 and c - b == 1:
            has_sequence = True
            break
    if has_sequence:
        issues.append("Есть последовательности (например, «abc» или «123»)")
        tips.append("Избегайте последовательных символов")

    # Словарные слова (упрощённая проверка)
    COMMON_WEAK = [
        "password", "пароль", "qwerty", "admin", "root",
        "123456", "hello", "welcome", "user", "test",
    ]
    lower_pw = password.lower()
    for word in COMMON_WEAK:
        if word in lower_pw:
            issues.append(f"Найдено словарное слово: «{word}»")
            tips.append("Не используйте словарные слова")
            break

    # --- Расчёт метрик ---
    entropy = calculate_entropy(password)
    crack_time = estimate_crack_time(entropy)
    strength, score = _entropy_to_strength(entropy)

    # Штраф за проблемы
    if issues:
        score = max(0, score - len(issues) * 5)

    # Убираем дубликаты из советов, сохраняя порядок
    seen = set()
    unique_tips = []
    for tip in tips:
        if tip not in seen:
            seen.add(tip)
            unique_tips.append(tip)

    return StrengthAssessment(
        entropy=round(entropy, 1),
        crack_time=crack_time,
        strength=strength,
        strength_score=score,
        issues=issues,
        tips=unique_tips,
    )