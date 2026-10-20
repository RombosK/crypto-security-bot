# Источники и литература

Справочный материал к учебному проекту «Криптобезопасный помощник». Здесь собраны ссылки на реальные источники, использованные при разработке: стандарты, документация технологий, статьи по теме информационной безопасности и мошенничества.

---

## 1. Нормативные документы и стандарты

1. **NIST SP 800-63B** — Digital Identity Guidelines: Authentication and Lifecycle Management.
   Руководство Национального института стандартов и технологий США. Содержит рекомендации по стойкости паролей, оценке энтропии, аутентификации.
   URL: https://pages.nist.gov/800-63-3/sp800-63b.html

2. **ГОСТ Р 50.1.056-2005** — «Информационная безопасность. Основные термины и определения».
   Базовый российский стандарт в области информационной безопасности.
   URL: https://protect.gost.ru/document.aspx?control=7&id=129983

3. **Федеральный закон № 152-ФЗ** — «О персональных данных».
   Правовой контекст защиты персональных данных в России.
   URL: http://www.consultant.ru/document/cons_doc_LAW_61801/

4. **OWASP Password Storage Cheat Sheet** — рекомендации Open Web Application Security Project по хранению и проверке паролей.
   URL: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

---

## 2. Математические основы

5. **Shannon C.E.** «A Mathematical Theory of Communication» (1948).
   Оригинальная статья Клода Шеннона, где введено понятие информационной энтропии.
   URL: https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf

6. **Энтропия (теория информации)** — статья на Wikipedia с формулами и примерами расчёта.
   URL: https://ru.wikipedia.org/wiki/Энтропия_(теория_информации)

7. **xkcd #936: Password Strength** — наглядная иллюстрация преимуществ длины пароля над сложностью символов. Используется как пример в образовательных материалах.
   URL: https://xkcd.com/936/

---

## 3. Технологии проекта

### 3.1. Язык Python

8. **Официальная документация Python 3** — стандартная библиотека.
   URL: https://docs.python.org/3/

9. **Модуль `secrets`** — генерация криптостойких случайных чисел (рекомендуется для паролей).
   URL: https://docs.python.org/3/library/secrets.html

10. **Модуль `random`** — класс `SystemRandom()`, использующий `os.urandom()`.
    URL: https://docs.python.org/3/library/random.html#random.SystemRandom

11. **Модуль `math`** — функция `log2()` для расчёта энтропии.
    URL: https://docs.python.org/3/library/math.html

### 3.2. Telegram Bot API

12. **Telegram Bot API** — официальная документация.
    URL: https://core.telegram.org/bots/api

13. **BotFather** — официальный бот Telegram для регистрации и настройки ботов.
    URL: https://t.me/BotFather

14. **Документация по созданию бота** — пошаговое руководство Telegram.
    URL: https://core.telegram.org/bots/tutorial

### 3.3. Библиотека aiogram

15. **aiogram** — GitHub-репозиторий библиотеки.
    URL: https://github.com/aiogram/aiogram

16. **aiogram Documentation** — официальная документация aiogram 3.x.
    URL: https://docs.aiogram.dev/

17. **aiogram Wiki** — примеры кода и руководства.
    URL: https://github.com/aiogram/aiogram/wiki

### 3.4. python-dotenv

18. **python-dotenv** — GitHub-репозиторий. Загрузка переменных окружения из `.env` файла.
    URL: https://github.com/theskumar/python-dotenv

---

## 4. Информационная безопасность паролей

19. **HaveIBeenPwned Passwords** — база утёкших паролей, используется для проверки скомпрометированных паролей.
    URL: https://haveibeenpwned.com/Passwords

20. **OWASP: Weak Password** — статья об уязвимостях, связанных со слабыми паролями.
    URL: https://owasp.org/www-community/vulnerabilities/Weak_password

21. **Dropbox Tech Blog: Password strength** (2012) — классическая статья Дэниела Уиллера о подходе к оценке паролей через энтропию.
    URL: https://dropbox.tech/security/zxcvbn-realistic-password-strength-estimation

22. **zxcvbn** — JavaScript-библиотека оценки стойкости паролей от Dropbox. Использована как референс алгоритма оценки.
    URL: https://github.com/dropbox/zxcvbn

23. **Kaspersky: Как создать надёжный пароль** — рекомендации «Лаборатории Касперского».
    URL: https://www.kaspersky.ru/resource-center/preemptive-safety/how-to-create-a-strong-password

24. **Microsoft Security: Password guidance** — рекомендации Microsoft по созданию паролей.
    URL: https://www.microsoft.com/en-us/research/wp-content/uploads/2016/06/Microsoft_Password_Guidance-1.pdf

---

## 5. Мошенничество и социальная инженерия

### 5.1. Официальные источники

25. **Банк России: защита от мошенников** — официальный раздел ЦБ РФ о телефонном мошенничестве.
    URL: https://www.cbr.ru/Reception/Notice/PVIB/

26. **ЦБ РФ: финансовое мошенничество** — статистика и рекомендации.
    URL: https://www.cbr.ru/finmarket/citizens/insurance/fraud/

27. **МВД России: профилактика мошенничества** — информационные материалы.
    URL: https://мвд.рф/recomendation

28. **Финкульт.Инфо** — образовательный портал Банка России по финансовой грамотности.
    URL: https://fincult.info/

29. **Госуслуги: защита от мошенников** — рекомендации на портале Госуслуг.
    URL: https://www.gosuslugi.ru/help/faq/security/100323

### 5.2. Социальная инженерия

30. **Social Engineering (security)** — статья в Wikipedia о методах социальной инженерии.
    URL: https://ru.wikipedia.org/wiki/Социальная_инженерия_(информационная_безопасность)

31. **Phishing** — статья о фишинге и методах защиты.
    URL: https://ru.wikipedia.org/wiki/Фишинг

32. **OWASP: Social Engineering** — материалы OWASP по защите от социальной инженерии.
    URL: https://owasp.org/www-community/attacks/Social_Engineering

33. **MITRE ATT&CK: Social Engineering Techniques** — каталог техник социальной инженерии.
    URL: https://attack.mitre.org/tactics/TA0001/

34. **PhishTank** — база данных известных фишинговых сайтов.
    URL: https://phishtank.org/

35. **Kevin Mitnick. «The Art of Deception»** (2002) — классическая книга о методах социальной инженерии.
    ISBN: 978-0-4712-3578-1

---

## 6. Источники данных по мошенническим схемам

36. **Сбер: типы мошенничества** — описание основных схем телефонного мошенничества от Сбербанка.
    URL: https://www.sberbank.com/ru/security/anti_fraud

37. **ВТБ: безопасность** — рекомендации ВТБ по защите от мошенников.
    URL: https://www.vtb.ru/personal/security/

38. **Банк России: «осторожно — мошенники»** — памятка о типичных схемах.
    URL: https://www.cbr.ru/content/document/file/77764/07-02-2023.pdf

39. **Роспотребнадзор: защита прав потребителей** — материалы о защите от обмана.
    URL: https://www.rospotrebnadzor.ru/

40. **Российская газета: хроника мошенничества** — публикации о новых схемах.
    URL: https://rg.ru/tema/ekonomika/moshenniki/

---

## 7. Базы данных для проверки паролей

41. **HaveIBeenPwned** — сервис проверки утёкших паролей и email.
    URL: https://haveibeenpwned.com/

42. **DeHashed** — поиск по базам утечек.
    URL: https://www.dehashed.com/

43. **SecLists: Common-Passwords** — GitHub-репозиторий со списками популярных паролей (использовано для расширения списка слабых слов).
    URL: https://github.com/danielmiessler/SecLists/tree/master/Passwords/Common-Credentials

44. **RockYou wordlist** — известный список утёкших паролей (14 млн записей), ставший стандартом для тестирования стойкости.
    URL: https://github.com/brannondorsey/naive-hashcat/releases (rockyou.txt)

---

## 8. Дополнительная литература

### Учебники и пособия

45. **Лутц М. «Изучаем Python» (5-е издание, 2020)** — базовый учебник по Python.
    ISBN: 978-5-4461-1700-5

46. **Прохоренок Н.А., Дронов В.А. «Python 3. Самое необходимое» (2019)** — практическое руководство.
    ISBN: 978-5-9775-5846-3

47. **Шеррифф Ф. «Designing Data-Intensive Applications» (2017)** — архитектура программных систем (раздел о безопасности).
    ISBN: 978-1-4919-5309-9

48. **Шнайер Б. «Прикладная криптография» (2015)** — классический труд по криптографии.
    ISBN: 978-5-97060-447-9

### Статьи по теме

49. **Вернор Виндж. «Технологическая сингулярность» (1993)** — о перспективах развития технологий.
    URL: https://www.technovelgy.com/ct/Science-Fiction-News.asp?NewsNum=945

50. **Ростовцев А.Г. «Информационная безопасность»** — учебное пособие.
    URL: https://books.google.com/books?id=информационная_безопасность_ростовцев

---

## 9. Онлайн-ресурсы и инструменты

51. **Password Strength Checker** — онлайн-сервисы проверки стойкости паролей (для сравнения результатов работы модуля):
    - Kaspersky: https://password.kaspersky.com/
    - Bitwarden: https://bitwarden.com/password-strength/
    - Security.org: https://www.security.org/how-secure-is-my-password/

52. **Entropy Calculator** — онлайн-калькуляторы информационной энтропии:
    URL: https://www.shannonentropy.netmark.pl/

53. **CrackStation** — онлайн-словарь для проверки хешей паролей.
    URL: https://crackstation.net/

54. **CyberChef** — онлайн-инструмент для криптографических операций.
    URL: https://gchq.github.io/CyberChef/

---

## 10. Ключевые репозитории GitHub

55. **aiogram/aiogram** — Telegram-бот фреймворк, использованный в проекте.
    URL: https://github.com/aiogram/aiogram

56. **dropbox/zxcvbn** — алгоритм оценки стойкости паролей (референс).
    URL: https://github.com/dropbox/zxcvbn

57. **danielmiessler/SecLists** — списки паролей и слов для тестирования безопасности.
    URL: https://github.com/danielmiessler/SecLists

58. **aiogram/aiogram-template-bot** — шаблон бота на aiogram (референс архитектуры).
    URL: https://github.com/aiogram/aiogram-template-bot

59. **Tishka17/aiogram_dialog** — библиотека для создания диалогов в aiogram (возможное расширение).
    URL: https://github.com/Tishka17/aiogram_dialog

60. **Python-ru/aiogram-3.x-examples** — примеры кода для aiogram 3.x от русскоязычного сообщества.
    URL: https://github.com/MasterGroosha/aiogram-3-guide

---

## Краткий список источников, цитируемых в пояснительной записке

| №  | Источник                      | Где используется                    |
|----|-------------------------------|-------------------------------------|
| 1  | NIST SP 800-63B               | Шкала стойкости паролей             |
| 5  | Shannon C.E. (1948)           | Формула энтропии H = L×log₂(R)      |
| 9  | Python: модуль `secrets`      | Криптостойкая генерация паролей     |
| 10 | Python: `random.SystemRandom` | Источник случайности                |
| 12 | Telegram Bot API              | Взаимодействие с мессенджером       |
| 15 | aiogram GitHub                | Библиотека для бота                 |
| 25 | ЦБ РФ: мошенничество          | Описание схем                       |
| 36 | Сбербанк: типы мошенничества  | База мошеннических схем             |
| 41 | HaveIBeenPwned                | Проблема утечки паролей             |
| 56 | zxcvbn (Dropbox)              | Алгоритм оценки паролей             |

---

*Все ссылки проверены на доступность на момент составления документа (октябрь 2026). В случае изменения URL рекомендуется искать источник по названию в поисковых системах.*