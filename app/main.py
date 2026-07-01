import asyncio
import logging
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram.types import Message


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def start_handler(message: "Message") -> None:
    """Відповідь на команду /start."""
    await message.answer(
        "Вітаю! Я інформаційний бот LegalHelp4UA. "
        "Допомагаю українцям за кордоном із нотаріальними документами "
        "та апостилем дистанційно."
    )


async def main() -> int:
    """Завантажує налаштування та запускає бота."""
    try:
        from dotenv import load_dotenv
    except ModuleNotFoundError:
        logger.error("Не встановлено python-dotenv. Виконайте: pip install -r requirements.txt")
        return 1

    # Завантажуємо BOT_TOKEN з .env та змінних середовища.
    load_dotenv()

    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        logger.error(
            "BOT_TOKEN не заданий. Додайте його у файл .env "
            "або встановіть як змінну середовища."
        )
        return 1

    try:
        from aiogram import Bot, Dispatcher
        from aiogram.filters import CommandStart
    except ModuleNotFoundError:
        logger.error("Не встановлено aiogram. Виконайте: pip install -r requirements.txt")
        return 1

    # Реєструємо хендлер і запускаємо polling.
    dp = Dispatcher()
    dp.message.register(start_handler, CommandStart())

    bot = Bot(token=token)
    logger.info("Бот LegalHelp4UA стартував. Запуск polling...")
    await dp.start_polling(bot)
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
