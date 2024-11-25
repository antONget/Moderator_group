import logging

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import async_session
from database.models import User, ClanGroup
from sqlalchemy import select


"""USER"""


async def get_user_tg_id(tg_id: int) -> User:
    logging.info('get_user_tg_id')
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def get_user_username(username: str) -> User:
    logging.info('get_user_username')
    async with async_session() as session:
        return await session.scalar(select(User).where(User.username == username))


async def add_new_user(data: dict) -> None:
    logging.info(f'add_new_user')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == int(data["tg_id"])))
        if not user:
            session.add(User(**data))
            await session.commit()


async def update_user_role(tg_id: int, role: str) -> None:
    logging.info(f'update_user_role')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.role = role
        await session.commit()


async def update_user_age(tg_id: int, age: int) -> None:
    logging.info(f'update_user_age')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.age = age
        await session.commit()


async def update_user_name(tg_id: int, name: str) -> None:
    logging.info(f'update_user_name')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.name = name
        await session.commit()


async def update_username(tg_id: int, username: str) -> None:
    logging.info(f'update_user_name')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.username = username
        await session.commit()


async def update_user_id_pubg(tg_id: int, id_pubg: int) -> None:
    logging.info(f'update_user_id_pubg')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.id_PUBG_MOBILE = id_pubg
        await session.commit()


async def update_user_nickname(tg_id: int, nickname: str) -> None:
    logging.info(f'update_user_nickname')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.nickname = nickname
        await session.commit()


"""GROUP"""


async def get_groups() -> list[ClanGroup]:
    logging.info('get_groups')
    async with async_session() as session:
        groups = await session.scalars(select(ClanGroup))
        groups_list = [group for group in groups]
        return groups_list


async def get_groups_group_id(group_id: int) -> ClanGroup:
    logging.info('get_groups_group_id')
    async with async_session() as session:
        return await session.scalar(select(ClanGroup).where(ClanGroup.group_id == group_id))


async def get_groups_general() -> ClanGroup:
    logging.info('get_groups_group_id')
    async with async_session() as session:
        return await session.scalar(select(ClanGroup).where(ClanGroup.group_clan == 'general'))


async def add_new_group(data: dict) -> None:
    logging.info(f'add_new_group')
    async with async_session() as session:
        group = await session.scalar(select(ClanGroup).where(ClanGroup.group_id == int(data["group_id"])))
        if not group:
            session.add(ClanGroup(**data))
            await session.commit()


async def update_group_general(group_id: int, group_link: str) -> None:
    logging.info('update_group_general')
    async with async_session() as session:
        group = await session.scalar(select(ClanGroup).where(ClanGroup.group_clan == "general"))
        if group:
            group.group_id = group_id
            group.group_link = group_link
            await session.commit()

# # Функция для создания строки пользователя в базе
# async def create_str(session: AsyncSession, user_id: int):
#     async with session.update():  # автоматически начинает транзакцию
#         user = await session.scalar(select(UserBase).where(UserBase.tg_id == user_id))
#
#         # если пользователя нет в базе
#         if not user:
#             new_user = UserBase(tg_id=user_id)
#             session.add(new_user)
#             await session.commit()
#
#
#
#
#
# async def parse1(user_identifier, session):
#     async with async_session() as session:
#         result = await session.execute(select(UserBase).where(UserBase.username == user_identifier))
#         user_data = result.fetchone()  # Вернет всю строку как кортеж или None, если не найдено
#         return user_data
#
#
# async def parse_clan(user_identifier, session):
#     async with async_session() as session:
#         result = await session.execute(select(UserBase).where(ClanBase.clan == user_identifier))
#         user_data = result.fetchone()  # Вернет всю строку как кортеж или None, если не найдено
#         return user_data
#
#
# async def username(username, user_id, session):
#     async with async_session() as session:
#         player = User(await parse(user_id, session))
#         player.name = username
#         session.merge(player, session)
#         await session.commit()
#
#
# async def id(message, user_id, session):
#     async with async_session() as session:
#         player = UserBase(await parse(user_id, session))
#         player.number = message
#         session.merge(player, session)
#         await session.commit()
#
#
# async def name(message, user_id, session):
#     async with async_session() as session:
#         player = UserBase(await parse(user_id, session))
#         if player:
#             player.name = message
#             session.merge(player, session)
#             await session.commit()
#
#
# async def year(message, user_id, session):
#     async with async_session() as session:
#         player = UserBase(await parse(user_id, session))
#         player.age = message
#         session.merge(player, session)
#         session.commit()
#
#
# async def nickname(message, user_id, session):
#     async with async_session() as session:
#         player = UserBase(await parse(user_id, session))
#         player.nickname = message
#         player.role = "user"
#         session.merge(player, session)
#         session.commit()
#
#
# async def set_lider(user_id, session):
#     async with async_session() as session:
#         player = UserBase(await parse(user_id, session))
#         player.role = "lider"
#         session.merge(player, session)
#         session.commit()
#
#
# async def clan_name(message, user_id, session):
#     async with async_session() as session:
#         player = ClanBase(await parse_clan(user_id, session))
#         player.name = message
#         session.merge(player, session)
#         session.commit()
#
#
# async def get_rows_with_role_clan() -> list:
#     async with async_session() as session:
#         users = await session.scalars(select(User))
#         list_users = [user for user in users ]
#         return list_users
