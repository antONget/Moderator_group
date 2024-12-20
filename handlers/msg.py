import asyncio
import logging

from aiogram import Router, F, Bot
from aiogram.types import Message
from database import requests as rq
from database.models import User, ChatAction
from utils.error_handling import error_handler
from aiogram.filters import CommandObject, Command
from filter.admin_filter import IsSuperAdmin

router = Router()
router.message.filter(F.chat.type == "private")


@router.message(Command('msg'), IsSuperAdmin())
@error_handler
async def into_command_msg(message: Message, bot: Bot, command: CommandObject) -> None:
    """
    Обработка команды /msg
    :param message:
    :param bot:
    :param command:
    :return:
    """
    logging.info('into_command_msg')
    arguments = command.args
    if arguments:
        users: list[User] = await rq.get_users()
        len_users = len(users)
        i = 0
        j = 0
        await message.answer(text=f'Рассылка запущена на {len_users} пользователей')
        for user in users:
            i += 1
            if user.clan_name == 'None' or not user.clan_name:
                await asyncio.sleep(1)
                try:
                    await bot.send_message(chat_id=user.tg_id,
                                           text=arguments)
                except:
                    j += 1
        await message.answer(text=f'Рассылка завершена. Разослано - {len_users}, доставлено - {j}')
    else:
        await message.answer(text='Пришлите текст для рассылки')