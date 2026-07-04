# DEBUG.md - журнал помилок і виправлень

Записуємо реальні помилки, які виникали під час розробки бота, щоб навчитися читати traceback знизу вгору.

---

## Помилка 1 - BOT_TOKEN не заданий

- **Назва помилки:** конфігураційна помилка
- **Що запускав:** `python -m app.main`
- **Що зробив:** закоментував `BOT_TOKEN` у `.env`

```text
2026-07-04 11:20:22,795 ERROR __main__: BOT_TOKEN не заданий. Додайте його у файл .env або встановіть як змінну середовища.
```

- **Головний рядок:** `BOT_TOKEN не заданий`
- **Причина:** бот не бачить токен, бо рядок у `.env` був закоментований.
- **Як виправив:** прибрав `#` перед `BOT_TOKEN` і зберіг `.env`.
- **Який prompt дав AI:** "Поясни цей лог простими словами: тип помилки, причина і мінімальний фікс. Не переписуй проєкт."
- **Як перевірив, що працює:** повернув `BOT_TOKEN` у `.env`, запустив `python -m app.main` і побачив старт polling без помилки токена.

---

## Помилка 2 - ModuleNotFoundError

- **Назва помилки:** `ModuleNotFoundError`
- **Що запускав:** `python -m app.main`
- **Що зробив:** навмисно додав `import nonexistent_module`

```text
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\dev\vibe-coding-hw\app\main.py", line 4, in <module>
    import nonexistent_module
ModuleNotFoundError: No module named 'nonexistent_module'
```

- **Головний рядок:** `ModuleNotFoundError: No module named 'nonexistent_module'`
- **Причина:** Python намагається імпортувати модуль, якого не існує.
- **Як виправив:** прибрав рядок `import nonexistent_module`.
- **Який prompt дав AI:** "Ось traceback з ModuleNotFoundError. Поясни тип помилки, файл і рядок, причину та мінімальний фікс."
- **Як перевірив, що працює:** прибрав навмисний імпорт і повторно запустив `python -m app.main`; ця помилка більше не з'явилась.

---

## Помилка 3 - ImportError

- **Назва помилки:** `ImportError`
- **Що запускав:** `python -m app.main`
- **Що зробив:** навмисно додав неіснуючий `CommandFake`

```text
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\dev\vibe-coding-hw\app\main.py", line 125, in <module>
    exit_code = asyncio.run(main())
  File "C:\dev\vibe-coding-hw\app\main.py", line 104, in main
    from aiogram.filters import Command, CommandStart, CommandFake
ImportError: cannot import name 'CommandFake' from 'aiogram.filters'
```

- **Головний рядок:** `ImportError: cannot import name 'CommandFake' from 'aiogram.filters'`
- **Причина:** у бібліотеці `aiogram.filters` немає назви `CommandFake`.
- **Як виправив:** прибрав `CommandFake`, залишив `Command` і `CommandStart`.
- **Який prompt дав AI:** "Traceback показує ImportError. Це справжня назва aiogram чи вигадана? Дай мінімальний фікс імпорту."
- **Як перевірив, що працює:** прибрав `CommandFake`, запустив `python -m app.main` і перевірив, що бот стартує та команди обробляються.
