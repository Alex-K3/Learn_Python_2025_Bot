from app.database.models import async_session
from app.database.models import User, UserInfo
from sqlalchemy import select


async def set_user(tg_id, username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, username=username))
            await session.commit()


async def update_user(tg_id, name, age, number):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            user_info = await session.scalar(select(UserInfo).where(UserInfo.user == user.id))

            if not user_info:
                session.add(UserInfo(name=name, age=age, phone=number, user=user.id))
                await session.commit()
            else:
                user_info.name = name
                user_info.age = age
                user_info.phone = number
                await session.commit()
        else:
            raise ValueError("User not found")
