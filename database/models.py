from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


# Создаем асинхронный движок
engine = create_async_engine("sqlite+aiosqlite:///database/db.sqlite3", echo=False)
# Настраиваем фабрику сессий
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String())
    nickname: Mapped[str] = mapped_column(String(), default='')
    name: Mapped[str] = mapped_column(String(), default='')
    age: Mapped[int] = mapped_column(Integer(), default=0)
    honor: Mapped[int] = mapped_column(Integer(), default=0)
    data_registration: Mapped[str] = mapped_column(String(), default='date')
    id_PUBG_MOBILE: Mapped[int] = mapped_column(Integer(), default=0)
    role: Mapped[str] = mapped_column(String(), default='user')
    clan_name: Mapped[str] = mapped_column(String(), default='None')
    warn: Mapped[str] = mapped_column(String(), default='None')

class ClanGroup(Base):
    __tablename__ = "clan_groups"

    group_id: Mapped[int] = mapped_column(primary_key=True)
    group_clan: Mapped[str] = mapped_column(String())
    group_link: Mapped[str] = mapped_column(String())

"""class Warn(Base):
    __tablename__ = "warn"

    tg_id: Mapped[int] = mapped_column(primary_key=True)
    warn_1: Mapped[str] = mapped_column(String())
    warn_cause_1: Mapped[str] = mapped_column(String())
    warn_2: Mapped[str] = mapped_column(String())
    warn_cause_2: Mapped[str] = mapped_column(String())
    warn_3: Mapped[str] = mapped_column(String())
    warn_cause_3: Mapped[str] = mapped_column(String())
    warn_4: Mapped[str] = mapped_column(String())
    warn_cause_4: Mapped[str] = mapped_column(String())
    warn_5: Mapped[str] = mapped_column(String())
    warn_cause_5: Mapped[str] = mapped_column(String())
    mute: Mapped[str] = mapped_column(String())
    mute_cause: Mapped[str] = mapped_column(String())
    ban: Mapped[str] = mapped_column(String())
    ban_cause: Mapped[str] = mapped_column(String())"""

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
