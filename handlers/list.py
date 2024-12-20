import logging

from aiogram import Router, F, Bot
from aiogram.types import Message
from database import requests as rq
from database.models import User
from utils.error_handling import error_handler
from aiogram.filters import Command
from filter.filter_group import is_admin
from config_data.config import Config, load_config

router = Router()
config: Config = load_config()
router.message.filter(F.chat.type != "private")


@router.message(Command('list'))
@error_handler
async def into_command_list(message: Message, bot: Bot) -> None:
    logging.info(f'into_command_list {message.chat.id}')
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)  # Удаление сообщения
    if not await is_admin(message, bot):
        await message.answer("Для использования этой команды бот должен быть администратором в канале,"
                             " а вы администратором или владельцем")
        return

    users = await rq.get_users()
    # print(len(users))
    group = await rq.get_groups_group_id(group_id=message.chat.id)
    # groups = await rq.get_groups()
    # text = ''
    # i = 0
    # await bot.send_message(chat_id=config.tg_bot.support_id,
    #                        text='list')
    if group.group_clan == 'general':
        # await bot.send_message(chat_id=config.tg_bot.support_id,
        #                        text='general')
        text = 'УЧАСТНИКИ КЛАНА:\n\n'
        # for group_ in groups:
            # text = f'<b>{group_.group_id}</b>\n\n'
            # text = ''
        i = 0
        for user in users:
            try:
                member = await bot.get_chat_member(user_id=user.tg_id,
                                                   chat_id=message.chat.id)
            except:
                continue
            # print(member.status)
            if member.status not in ['left', 'kicked', 'restricted']:
                if user.nickname:
                    i += 1
                    text += f'{i}. <a href="tg://user?id={user.tg_id}">{user.nickname}</a>\n'
            # await bot.send_message(chat_id=config.tg_bot.support_id,
            #                        text=text)
        # await message.answer(text=text)
        # print('text', text)
    else:
        text = f'{message.chat.title}\n\n'
        member_text = ''
        i = 0
        for user in users:
            member = await bot.get_chat_member(user_id=user.tg_id,
                                               chat_id=message.chat.id)
            member_text += f'{user.tg_id}/{member.status}'
            if member.status not in ['left', 'kicked', 'restricted']:
                if user.nickname:
                    i += 1
                    text += f'{i}. <a href="tg://user?id={user.tg_id}">{user.nickname}</a>\n'
        # await bot.send_message(chat_id=config.tg_bot.support_id,
        #                        text=member_text)
    print('text', text)
    if text != '':
        # await bot.send_message(chat_id=config.tg_bot.support_id,
        #                        text=text)
        await message.answer(text=text)
    else:
        await message.answer(text='Данные об участниках клана отсутствуют')
    return
