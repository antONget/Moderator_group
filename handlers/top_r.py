import logging
import asyncio

from aiogram import Router, Bot
from aiogram.types import Message
from filter.filter_group import is_admin
from aiogram.filters import Command, CommandObject
from utils.error_handling import error_handler
from database import requests as rq

router = Router()

@router.message(Command("top_r"))
@error_handler
async def process_command_del_r(message: Message, bot: Bot):
    """
    Обработка команды /top_r
    /top_r
    :param message:
    :param bot:
    :return:
    """
    logging.info('process_command_del_r')
    # удаляем сообщение с командой
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    # проверка что команду использует администратор или владелец чата
    if not await is_admin(message, bot):
        msg = await message.answer(text="Для использования этой команды бот должен быть администратором в канале,"
                                        " а вы администратором или владельцем")
        await asyncio.sleep(5)
        await msg.delete()
        return
    num_top = 10
    top_honor = await rq.get_top_honor_users(num_top)
    top_all_honor = await rq.get_top_all_honor_users(num_top)
    top_users_honor = ""
    top_users_all_honor = ""
    for num, user in enumerate(top_honor, start=1):
        top_users_honor += f"{num}. <a href='tg://user?id={int(user.tg_id)}'>{user.nickname}</a> - {user.honor}\n"
    for num, user in enumerate(top_all_honor, start=1):
        top_users_all_honor += f"{num}. <a href='tg://user?id={int(user.tg_id)}'>{user.nickname}</a> - {user.all_honor}\n"
    await message.answer("РЕЙТИНГ\n\n"
                         "ВСЯ ЧЕСТЬ:\n\n"
                         f"{top_users_honor}"
                         "Честь:\n\n"
                         f"{top_users_all_honor}")
