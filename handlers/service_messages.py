from aiogram.types import ChatMemberUpdated
from aiogram import Router, F, Bot

from database import requests as rq
from database.models import ClanGroup
from config_data.config import Config, load_config
from keyboards.keyboard import main_keyboard_group

import logging
import asyncio

router = Router()
config: Config = load_config()


@router.chat_member(F.new_chat_member)
async def on_user_join(event: ChatMemberUpdated, bot: Bot):
    logging.info(f'on_user_join {event.new_chat_member.status} {event}')
    # print(event.new_chat_member.status, event.from_user.id)
    if event.new_chat_member.status == 'member':
        if event.from_user.id != 6166594444:
            # await bot.delete_message(chat_id=event.chat.id, message_id=event.message_id)
            # если человек зашел в общий чат клана, то бот проверяет, состоит ли данный юзер в чатах клана,
            # если нет, то сразу банит в общем чате
            general_group: ClanGroup = await rq.get_groups_general()
            # print(general_group.group_id, event.chat.id)
            if event.chat.id == general_group.group_id:
                text = f'<a href="tg://user?id={event.from_user.id}">{event.from_user.full_name}</a>,' \
                       f' добро пожаловать в общий чат клана!'
                await event.answer(text=text,
                                   reply_markup=main_keyboard_group())
                groups: list[ClanGroup] = await rq.get_groups()
                is_ban = True
                for group in groups:
                    if group.group_clan == 'general':
                        continue
                    else:
                        try:
                            member = await bot.get_chat_member(user_id=event.from_user.id,
                                                               chat_id=group.group_id)
                            if member.status in ['member', 'administrator']:
                                is_ban = False
                        except:
                            pass
                if is_ban:
                    msg = await event.answer(text=f'Пользователь <a href="tg://user?id={event.from_user.id}">'
                                                  f'{event.from_user.full_name}</a> не состоит в клановских беседах'
                                                  f' и будет забанен на один час')
                    # print(event.from_user.id)
                    await bot.ban_chat_member(chat_id=general_group.group_id, user_id=event.from_user.id)
                    # await asyncio.sleep(1 * 60)
                    # await msg.delete()
                    await asyncio.sleep(60 * 60)
                    await bot.unban_chat_member(chat_id=general_group.group_id, user_id=event.from_user.id)
            else:
                await event.answer(text=f"<a href='tg://user?id={event.from_user.id}'>{event.from_user.full_name}</a>, добро пожаловать в клан!\n\n"
                                        f"Если ты еще не зашел в общий чат клана, то не сможешь писать сообщения,"
                                        f" перейди в бота @clan_by_bot напиши команду /start и команду"
                                        f" /opros для прохождения опроса.",
                                     reply_markup=main_keyboard_group())

