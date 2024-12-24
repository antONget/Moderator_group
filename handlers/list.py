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
    group = await rq.get_groups_group_id(group_id=message.chat.id)
    if group.group_clan == 'general':
        text = 'УЧАСТНИКИ КЛАНА:\n\n'
        i = 0
        for user in users:
            try:
                member = await bot.get_chat_member(user_id=user.tg_id,
                                                   chat_id=message.chat.id)
            except:
                continue
            if member.status not in ['left', 'kicked', 'restricted']:
                if user.nickname:
                    i += 1
                    text += f'{i}. <a href="tg://user?id={user.tg_id}">{user.nickname}</a>\n'
            if i % 100 == 0:
                if text:
                    await message.answer(text=text)
                    text = ''

    else:
        text = f'{message.chat.title}\n\n'
        i = 0
        for user in users:
            member = await bot.get_chat_member(user_id=user.tg_id,
                                               chat_id=message.chat.id)
            if member.status not in ['left', 'kicked', 'restricted']:
                if user.nickname:
                    i += 1
                    text += f'{i}. <a href="tg://user?id={user.tg_id}">{user.nickname}</a>\n'
            if i % 100 == 0:
                if text:
                    await message.answer(text=text)
                    text = ''
    if text != '':
        await message.answer(text=text)

