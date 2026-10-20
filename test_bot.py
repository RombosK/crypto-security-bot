import sys
sys.path.insert(0, '/home/rombos/Projects/crypto-security-bot/src')

from password_engine import generate_password, assess_strength, calculate_entropy
from fraud_detector import analyze_message, list_schemes

print("=== Тест 1: Импорт модулей — OK ===")

print()
print("=== Тест 2: Генерация паролей ===")
for length in [8, 12, 16, 24]:
    r = generate_password(length=length)
    print(f"  Длина {length}: {r.password}")
    print(f"    Энтропия: {r.entropy} бит, взлом: {r.crack_time}, оценка: {r.strength} ({r.strength_score}/100)")

print()
print("=== Тест 3: Генерация с параметрами ===")
r = generate_password(length=20, use_symbols=False, exclude_similar=True)
print(f"  Без символов, без похожих: {r.password}")
r = generate_password(length=10, use_upper=False, use_digits=False)
print(f"  Только строчные: {r.password}")

print()
print("=== Тест 4: Оценка существующих паролей ===")
test_passwords = [
    "123456",
    "qwerty",
    "password",
    "abc123",
    "MyStr0ng!Pass2024",
    "correcthorsebatterystaple",
]
for pw in test_passwords:
    res = assess_strength(pw)
    print(f"  '{pw}':")
    print(f"    Энтропия: {res.entropy} бит, взлом: {res.crack_time}")
    print(f"    Оценка: {res.strength} ({res.strength_score}/100)")
    if res.issues:
        print(f"    Проблемы: {'; '.join(res.issues)}")
    if res.tips:
        print(f"    Советы: {'; '.join(res.tips)}")

print()
print("=== Тест 5: Анализ сообщений на мошенничество ===")
test_messages = [
    "Здравствуйте, ваш сын попал в больницу, срочно переведите 50000 на этот счёт",
    "Здравствуйте, это служба безопасности Центрального Банка. Ваш счёт взломан, переведите деньги на безопасный счёт ЦБ РФ. Назовите код из СМС.",
    "Привет, идём в кино в субботу?",
    "Вы выиграли в лотерею! Чтобы получить приз, оплатите налог 1000 рублей",
    "Инвестируйте в криптовалюту, гарантированная доходность 200% годовых, заработок без усилий",
    "Добрый день, ваш заказ доставлен. Оставьте отзыв на сайте.",
]
for msg in test_messages:
    result = analyze_message(msg)
    print(f"  Сообщение: '{msg[:60]}...'")
    print(f"    Скор: {result.score}/100, уровень: {result.level}")
    print(f"    Найдено признаков: {len(result.found_signs)}")
    if result.matched_schemes:
        print(f"    Совпавшие схемы: {[s['name'] for s in result.matched_schemes]}")
    print()

print("=== Тест 6: База схем ===")
schemes = list_schemes()
print(f"  Всего схем: {len(schemes)}")
for s in schemes:
    print(f"  - {s['name']}")

print()
print("=== ВСЕ ТЕСТЫ ПРОЙДЕНЫ ===")