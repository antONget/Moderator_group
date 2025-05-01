import logging

from database.models import async_session
from database.models import User, ClanGroup, Chat_reaction, ChatAction, Recruting, RecrutingOpros
from sqlalchemy import select, update
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class UserRole:
    user = "user"
    lider = "lider"
    admin = "admin"
    clan = "clan"


"""USER"""


async def get_user_tg_id(tg_id: int) -> User:
    logging.info('get_user_tg_id')
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def update_username(tg_id: int, username: str) -> None:
    logging.info('update_username')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if username:
            user.username = username
        await session.commit()


async def update_data_registration(tg_id: int) -> None:
    logging.info('update_username')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            date_format = '%d-%m-%Y %H:%M'
            user.data_registration = datetime.now().strftime(date_format)
        await session.commit()


async def update_honor(tg_id: int) -> None:
    logging.info('update_honor')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        honor = user.honor
        user.honor = honor + 1
        user.all_honor += 1
        await session.commit()


async def change_honor(tg_id: int, sign: str, number: int) -> None:
    """
    Изменяем четь у определенного пользователя на число
    :param tg_id:
    :param sign:
    :param number:
    :return:
    """
    logging.info('change_honor')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if sign == "+":
            user.honor += number
            user.all_honor += number
        else:
            user.honor -= number
            user.all_honor -= number
        await session.commit()


async def reset_honor() -> None:
    """сбрасываем честь у всех пользователей до 0"""
    logging.info('reset_honor')
    async with async_session() as session:
        stmt = update(User).values(all_honor=0)
        await session.execute(stmt)
        await session.commit()


async def update_clan_name(tg_id: int, clan_name: str, username: str = 'username') -> None:
    """
    Обновляем имя клана у пользователя
    :param tg_id:
    :param clan_name:
    :param username:
    :return:
    """
    logging.info('update_clan_name')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.clan_name = clan_name
        else:
            data_user = {'tg_id': tg_id, 'clan_name': clan_name, 'username': username}
            session.add(User(**data_user))
        await session.commit()


async def update_invitation(tg_id: int, invitation: str) -> None:
    logging.info('update_invitation')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.invitation = invitation
        await session.commit()


async def update_warn(tg_id: int, warn: str) -> None:
    logging.info('update_clan_name')
    async with async_session() as session:
        user = await session.scalar(select(Chat_reaction).where(Chat_reaction.tg_id == tg_id))
        if not user:
            data = {"tg_id": tg_id, "warn": warn, "sum": 1}
            session.add(Chat_reaction(**data))
        else:
            user.warn += warn
            user.sum += 1
        await session.commit()
        return


async def update_ban(tg_id: int, ban: str) -> None:
    logging.info('update_clan_name')
    async with async_session() as session:
        user = await session.scalar(select(Chat_reaction).where(Chat_reaction.tg_id == tg_id))
        if not user:
            data = {"tg_id":tg_id, "ban":ban, "sum":1}
            session.add(Chat_reaction(**data))
        else:
            user.ban += ban
            user.sum += 1
        await session.commit()
        return


async def update_mute(tg_id: int) -> None:
    logging.info('update_clan_name')
    async with async_session() as session:
        user = await session.scalar(select(Chat_reaction).where(Chat_reaction.tg_id == tg_id))
        if not user:
            data = {"tg_id":tg_id, "mute":f"mute\n", "sum":1}
            session.add(Chat_reaction(**data))
        else:
            user.mute += f"mute\n"
            user.sum += 1
        await session.commit()
        return


async def update_kick(tg_id: int, kick: str) -> None:
    logging.info('update_clan_name')
    async with async_session() as session:
        user = await session.scalar(select(Chat_reaction).where(Chat_reaction.tg_id == tg_id))
        if not user:
            data = {"tg_id":tg_id, "kick":kick, "sum":1, "active_warn":1}
            session.add(Chat_reaction(**data))
        else:
            user.kick += kick
            user.sum +=1
            user.active_warn +=1
        await session.commit()
        return


async  def after_verification_warn(tg_id:int, active_warn:int):
    logging.info('after_verification_warn')
    async with async_session() as session:
        user = await session.scalar(select(Chat_reaction).where(Chat_reaction.tg_id == tg_id))
        user.active_warn = active_warn
        await session.commit()
        return


async  def get_warn_sum(tg_id:int):
    logging.info('get_warn_sum')
    async with async_session() as session:
        return await session.scalar(select(Chat_reaction).where(Chat_reaction.tg_id == tg_id))


async  def get_warn_user() -> list[Chat_reaction]:
    logging.info('get_users')
    async with async_session() as session:
        users = await session.scalars(select(Chat_reaction))
        users_list = [user for user in users]
        return users_list


async def get_user_username(username: str) -> User:
    """
    Получение информации о пользователе по его username
    :param username:
    :return:
    """
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


async def get_users() -> list[User]:
    logging.info('get_users')
    async with async_session() as session:
        users = await session.scalars(select(User))
        users_list = [user for user in users]
        return users_list


"""GROUP"""


async def get_groups() -> list[ClanGroup]:
    logging.info('get_groups')
    async with async_session() as session:
        groups = await session.scalars(select(ClanGroup))
        groups_list = [group for group in groups]
        return groups_list


async def get_groups_group_id(group_id: int) -> ClanGroup:
    """
    Получаем группу по ее peer_id
    :param group_id:
    :return:
    """
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


""" CHAT_ACTION """


async def add_chat_action(data: dict) -> None:
    """
    Добавление действия из чата
    :param data:
    :return:
    """
    logging.info(f'add_chat_action')
    async with async_session() as session:
        session.add(ChatAction(**data))
        await session.commit()


async def get_chat_action_tg_id(tg_id: int, type_action: str, count_day: int = 7) -> list[ChatAction]:
    """
    Получаем список выбранных действий в отношении пользователя за последние дни
    :param tg_id:
    :param type_action:
    :param count_day:
    :return:
    """
    logging.info(f'add_chat_action')
    async with async_session() as session:
        actions = await session.scalars(select(ChatAction).filter(ChatAction.tg_id == tg_id,
                                                                  ChatAction.type_action == type_action))
        list_actions = []
        if actions:
            date_format = '%d-%m-%Y %H:%M'
            current_date = datetime.now().strftime('%d-%m-%Y %H:%M')
            for action in actions:
                delta_time = (datetime.strptime(current_date, date_format) - datetime.strptime(action.data_action,
                                                                                               date_format))
                if count_day > 0:
                    if delta_time.days < count_day:
                        list_actions.append(action)
                else:
                    list_actions.append(action)
            return list_actions

        else:
            return list_actions


""" RECRUTING """


async def add_recruting(data: dict) -> None:
    """
    Добавление строки рекрутинга
    :param data:
    :return:
    """
    logging.info(f'add_chat_action')
    async with async_session() as session:
        recruting = await session.scalar(select(Recruting).where(Recruting.id == 1))
        if recruting:
            recruting.is_recruting = data['is_recruting']
        else:
            session.add(Recruting(**data))
        await session.commit()


async def get_recruting() -> Recruting:
    """
    Получение строки рекрутинга
    :return:
    """
    logging.info(f'get_recruting')
    async with async_session() as session:
        return await session.scalar(select(Recruting).where(Recruting.id == 1))


""" RECRUTING_OPROS """


async def add_recruting_opros(data: dict) -> None:
    """
    Добавление строки рекрутинга опроса
    :param data:
    :return:
    """
    logging.info(f'add_recruting_opros')
    async with async_session() as session:
        session.add(RecrutingOpros(**data))
        await session.commit()


async def get_recruting_opros() -> RecrutingOpros:
    """
    Получение строки рекрутинга
    :return:
    """
    logging.info(f'get_recruting')
    async with async_session() as session:
        recruting_opros = await session.scalars(select(RecrutingOpros))
        list_recruting_opros = [opros for opros in recruting_opros]
        return list_recruting_opros[-1]


async def get_recruting_opros_id(recruting_id: int) -> RecrutingOpros:
    """
    Получение строки рекрутинга
    :return:
    """
    logging.info(f'get_recruting')
    async with async_session() as session:
        return await session.scalar(select(RecrutingOpros).where(RecrutingOpros.id == recruting_id))


async def get_recruting_opros_tg_id(tg_id: int) -> RecrutingOpros:
    """
    Получение строки рекрутинга
    :return:
    """
    logging.info(f'get_recruting {tg_id}')
    async with async_session() as session:
        recruting_opros = await session.scalars(select(RecrutingOpros).where(RecrutingOpros.tg_id == tg_id))
        if recruting_opros:
            list_recruting_opros = [opros for opros in recruting_opros.all()]
            if len(list_recruting_opros) > 0:
                return list_recruting_opros[-1]
            else:
                return []