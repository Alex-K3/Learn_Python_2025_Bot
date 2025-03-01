import asyncio
from aiogram import Bot, Dispatcher
from config import load_config
from app.handlers import router
from app.database.models import async_main


async def main() -> None:
    await async_main()
    bot = Bot(token=load_config().TELEGRAM_API)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot exit')
