import logging

from aiogram import Router, F, Bot
from aiogram.types import Message
from database import requests as rq
from database.models import User
from utils.error_handling import error_handler
from aiogram.filters import Command
from filter.filter_group import is_admin

router = Router()
router.message.filter(F.chat.type != "private")


def format_users_for_message(users):
    """
    Формирует строку для отправки списка пользователей в Telegram.

    :param users: список словарей с ключами "tg_id" и "name"
    :return: строка, готовая для отправки в Telegram
    """
    return '\n'.join([f'<a href="tg://user?id={user["tg_id"]}">{user["nickname"]}</a>' for user in users])


@router.message(Command('list'))
async def into_command_list(message: Message, bot: Bot) -> None:
    logging.info('into_command_list')
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)  # Удаление сообщения
    if not await is_admin(message, bot):
        await message.reply("Для использования этой команды бот должен быть администратором в канале,"
                            " а вы администратором или владельцем")
        return

    users_dictinary = []  # Создание словаря
    users = await rq.get_users()
    for user in users:
        member = await bot.get_chat_member(user_id=message.from_user.id,
                                           chat_id=user.tg_id)
        if member.status != 'left':
            nickname = await rq.get_user_tg_id(tg_id=user.tg_id)
            users_dictinary.append({"tg_id": int(user.tg_id), "nickname": nickname.nickname})
    message = format_users_for_message(users)
    await message.answer(message)
    return

