import asyncio
from aiogram import Bot, Dispatcher
from config import load_config, logger
from app.handlers import router
from app.database.models import database_init


async def main() -> None:
    logger.info("Инициализация базы данных...")
    await database_init()
    logger.info("База данных успешно инициализирована.")
    bot = Bot(token=load_config().TELEGRAM_API)
    dp = Dispatcher()
    dp.include_router(router)
    logger.info("Бот запущен и ожидает сообщения...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot exit')
