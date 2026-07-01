# LegalHelp4UA

LegalHelp4UA — інформаційний Telegram-бот для українців, яким потрібні підказки щодо юридичних документів, нотаріальних дій та апостиля.

У репозиторії створено мінімальний каркас бота на Python з aiogram 3.x. Код самого бота буде додано наступним кроком.

## Запуск

1. Створіть файл `.env` на основі `.env.example` і додайте свій Telegram Bot Token:

```env
BOT_TOKEN=your_bot_token_here
```

2. Запустіть через Docker Compose:

```bash
docker compose up --build
```

Або локально:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
```
