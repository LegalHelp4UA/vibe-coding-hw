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
    logger.info("Команда /start від user_id=%s", message.from_user.id)
    await message.answer(
        "Вітаю! Я інформаційний бот LegalHelp4UA. "
        "Допомагаю українцям за кордоном із нотаріальними документами "
        "та апостилем дистанційно. 🇺🇦"
    )


async def help_handler(message: "Message") -> None:
    """Відповідь на команду /help."""
    logger.info("Команда /help від user_id=%s", message.from_user.id)
    await message.answer(
        "Я інформаційний бот LegalHelp4UA. Ось що я вмію:\n\n"
        "/start — привітання\n"
        "/services — які документи оформлюємо\n"
        "/process — як відбувається оформлення\n"
        "/contacts — як з нами зв'язатися\n"
        "/help — це повідомлення"
    )


async def services_handler(message: "Message") -> None:
    """Відповідь на команду /services."""
    logger.info("Команда /services від user_id=%s", message.from_user.id)
    await message.answer(
        "📄 LegalHelp4UA — дистанційне нотаріальне оформлення документів\n\n"
        "Допомагаємо українцям за кордоном оформити:\n"
        "• Довіреності — на нерухомість, авто, представництво в судах/органах влади, ведення бізнесу\n"
        "• Заяви та згоди — на виїзд дитини за кордон, згода подружжя на продаж/купівлю нерухомості, інші заяви для нотаріуса, податкової, суду\n"
        "• Спадкові документи — заяви про прийняття/відмову від спадщини, довіреність на оформлення спадщини\n"
        "• Договори — шлюбний договір, договір про аліменти, місце проживання дитини та інші\n"
        "• Переклади з апостилем та інші документи — affidavits, KYC/AML пакети, сертифікати резиденції\n\n"
        "Усе — дистанційно, з посвідченням під відеозв'язок із нотаріусом та апостилем."
    )


async def process_handler(message: "Message") -> None:
    """Відповідь на команду /process."""
    logger.info("Команда /process від user_id=%s", message.from_user.id)
    await message.answer(
        "🔄 Як ми працюємо\n\n"
        "1. Заявка — залишаєте заявку на сайті чи в чаті\n"
        "2. Безкоштовна консультація юриста — уточнюємо, який документ потрібен, і готуємо проєкт\n"
        "3. Погоджуємо текст документа з вами\n"
        "4. Підписання під відеозв'язком із нотаріусом\n"
        "5. Нотаріальне посвідчення та апостиль (від 24 годин)\n"
        "6. Доставка готового документа кур'єром\n\n"
        "Особиста присутність не потрібна — усе дистанційно."
    )


async def contacts_handler(message: "Message") -> None:
    """Відповідь на команду /contacts."""
    logger.info("Команда /contacts від user_id=%s", message.from_user.id)
    await message.answer(
        "📞 Як з нами зв'язатися\n\n"
        "Сайт: legalhelp4ua.com\n"
        "Email: support@legalhelp4ua.com\n"
        "Телефон (Велика Британія): +44 7418 376606\n"
        "Телефон (Україна): +380 63 837 6606\n"
        "Telegram: t.me/legalhelp4ukraine\n"
        "WhatsApp: wa.me/message/ATIHVIHXWOHVF1\n"
        "Viber: за номером +44 7518 275176\n"
        "Графік: Пн–Пт, 9:00–21:00 (за Києвом)\n\n"
        "Напишіть зручним каналом — ми відповімо і допоможемо.\n"
        "Інформація має довідковий характер і не є юридичною консультацією."
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
        from aiogram.filters import Command, CommandStart
    except ModuleNotFoundError:
        logger.error("Не встановлено aiogram. Виконайте: pip install -r requirements.txt")
        return 1

    # Реєструємо хендлери і запускаємо polling.
    dp = Dispatcher()
    dp.message.register(start_handler, CommandStart())
    dp.message.register(services_handler, Command("services"))
    dp.message.register(process_handler, Command("process"))
    dp.message.register(contacts_handler, Command("contacts"))
    dp.message.register(help_handler, Command("help"))

    bot = Bot(token=token)
    logger.info("Бот LegalHelp4UA стартував. Запуск polling...")
    await dp.start_polling(bot)
    return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Бот зупинено.")
        raise SystemExit(0) from None
    except SystemExit as exc:
        if exc.code not in (None, 0, 130):
            raise
        logger.info("Бот зупинено.")
        raise SystemExit(0) from None

    raise SystemExit(exit_code)
