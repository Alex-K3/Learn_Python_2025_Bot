from datetime import datetime
from typing import Annotated
from sqlalchemy import BigInteger, Integer, String, func, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from config import load_config
from config import logger


engine = create_async_engine(url=load_config().POSTGRE_SQL)
async_session = async_sessionmaker(engine)

uniq_str = Annotated[str, mapped_column(String(255), unique=True)]
normal_str = Annotated[str, mapped_column(String(100))]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'


class User(Base):
    tg_id = mapped_column(BigInteger, unique=True)
    first_name: Mapped[normal_str]
    last_name: Mapped[normal_str]
    username: Mapped[uniq_str]
    birthday: Mapped[datetime] = mapped_column(Date)
    city: Mapped[normal_str]
    phone: Mapped[uniq_str]
    email: Mapped[uniq_str]
    status: Mapped[str] = mapped_column(String(15))


async def database_init():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Таблицы успешно созданы в базе данных.")
        except Exception as e:
            logger.error(f"Ошибка при создании таблиц: {e}", exc_info=True)
