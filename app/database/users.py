from app.database.models import async_session, User
from sqlalchemy import select
from config import logger


async def set_user(tg_id: int, first_name: str, last_name: str, username: str, birthday: str, city: str, phone: str, email: str, status: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id,
                             username=username,
                             first_name=first_name,
                             last_name=last_name,
                             birthday=birthday,
                             city=city,
                             phone=phone,
                             email=email,
                             status=status,))
            await session.commit()
            logger.info(
                f"Добавлен новый пользователь: tg_id={tg_id}, username={username}")
