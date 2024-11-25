import logging

from aiogram import Router, F, Bot
from aiogram.types import Message
from database import requests as rq
from database.models import User
from utils.error_handling import error_handler
from aiogram.filters import  Command
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
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)#Удаление сообщения
    if not await is_admin(message, bot):
        await message.reply("Для использования этой команды бот должен быть администратором в канале,"
                            " а вы администратором или владельцем")
        return
    members = await bot.get_chat_members(chat_id=message.chat.id)#Создание переменной с значениями пользователей в группе
    users = [] #Создание словаря
    for member in members:
        try:
            tg_id = member.user.id
            nickname = await rq.get_user_tg_id(tg_id=tg_id)
            users.append({"tg_id": int(tg_id), "nickname": nickname.nickname})
        except ValueError:
            print("Ошибка: Введите данные в формате '<tg_id> <имя>'")

    message_ = format_users_for_message(users)
    await message.answer(message_)
    return

