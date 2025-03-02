from app.database.models import async_session, User
from sqlalchemy import select
from config import logger


async def set_user(tg_id: int, username: str):
    """Добавляет пользователя в БД при первом запуске бота."""
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, username=username))
            await session.commit()
            logger.info(
                f"Добавлен новый пользователь: tg_id={tg_id}, username={username}")


async def update_user(tg_id: int, first_name: str, last_name: str, birthday: str, city: str, phone: str, email: str):
    """Обновляет данные пользователя после регистрации."""
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            user.first_name = first_name
            user.last_name = last_name
            user.birthday = birthday
            user.city = city
            user.phone = phone
            user.email = email
            await session.commit()
            logger.info(f"Обновлены данные пользователя: tg_id={tg_id}")
