from sqlalchemy import String, Integer, BigInteger
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
    all_honor: Mapped[int] = mapped_column(Integer(), default=0)
    data_registration: Mapped[str] = mapped_column(String(), default='date')
    id_PUBG_MOBILE: Mapped[int] = mapped_column(Integer(), default=0)
    role: Mapped[str] = mapped_column(String(), default='user')
    clan_name: Mapped[str] = mapped_column(String(), default='')


class ClanGroup(Base):
    __tablename__ = "clan_groups"

    group_id: Mapped[int] = mapped_column(primary_key=True)
    group_clan: Mapped[str] = mapped_column(String(), default='')
    group_link: Mapped[str] = mapped_column(String(), default='')
    group_title: Mapped[str] = mapped_column(String(), default='')

#добавить новую колонку в которую вводится данные об сообщении


class Chat_reaction(Base):
    __tablename__ = "chat_reaction"

    tg_id: Mapped[int] = mapped_column(primary_key=True)
    warn: Mapped[str] = mapped_column(String(), default='')
    mute: Mapped[str] = mapped_column(String(), default='')
    ban: Mapped[str] = mapped_column(String(), default='')
    kick: Mapped[str] = mapped_column(String(), default='')
    sum: Mapped[int] = mapped_column(Integer(), default=0)
    active_warn: Mapped[int] = mapped_column(Integer(), default=0)


class ChatAction(Base):
    __tablename__ = "chat_action"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger())
    type_action: Mapped[str] = mapped_column(String(), default='')
    data_action: Mapped[str] = mapped_column(String(), default='')
    reason_action: Mapped[str] = mapped_column(String(), default='')


class Recruting(Base):
    __tablename__ = "recruting"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_recruting: Mapped[int] = mapped_column(String())


class RecrutingOpros(Base):
    __tablename__ = "recruting_opros"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger())
    age_opros: Mapped[int] = mapped_column(Integer())
    ID_PUBG_MOBILE: Mapped[int] = mapped_column(Integer())
    kd_Metro_Royale: Mapped[str] = mapped_column(String())
    img_PUBG_MOBILE: Mapped[str] = mapped_column(String())
    img_PUBG_Metro_Royale: Mapped[str] = mapped_column(String())
    about_me: Mapped[str] = mapped_column(String())
    data_opros: Mapped[str] = mapped_column(String())


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
