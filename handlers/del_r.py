import logging
import asyncio

from aiogram import Router, Bot, F
from aiogram.types import Message
from filter.filter_group import is_admin
from filter.admin_filter import check_super_admin
from aiogram.filters import Command, CommandObject
from utils.error_handling import error_handler
from database import requests as rq
from database.models import User

router = Router()


@router.message(Command("del_r"))
@error_handler
async def process_command_del_r(message: Message, command: CommandObject, bot: Bot):
    """
    Обработка команды /del_r
    /del_r @username [знак с числом]
    :param message:
    :param command:
    :param bot:
    :return:
    """
    logging.info('process_command_del_r')
    # удаляем сообщение с командой
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    # print(not await check_super_admin(telegram_id=message.from_user.id))
    if not await check_super_admin(telegram_id=message.from_user.id):
        await message.answer(text='Команда не доступна')
        return
    # проверка что команду использует администратор или владелец чата
    if not await is_admin(message, bot):
        msg = await message.answer(text="Для использования этой команды бот должен быть администратором в канале,"
                                        " а вы администратором или владельцем")
        await asyncio.sleep(5)
        await msg.delete()
        return
    arguments = command.args
    if not arguments:
        await rq.reset_honor()
        await message.answer("Честь сброшена")
        return
    list_arguments: list = arguments.split(' ', 1)
    if len(list_arguments) != 2:
        await message.answer(text="Для применения этой команды нужно указать пользователя любым способом "
                             "и указать как изменить его честь. например /del_r user -100")
        return
    else:
        sign = str(list_arguments[1])
        if '-' in sign or '+' in sign:
            numbers=''
            for num in sign:
                if num.isdigit():
                    numbers+=num
            if '-' in sign: sign = '-'
            else: sign = '+'
            if list_arguments[0].isdigit():
                user_to_action = int(list_arguments[0])
                user: User = await rq.get_user_tg_id(tg_id=user_to_action)
                if user:
                    await rq.change_honor(tg_id=user_to_action, sign=sign, number=int(numbers))
                    await message.answer(f"Честь у пользователя {user.nickname} изменилась "
                                         f"на {list_arguments[1]}")
                else:
                    await message.answer(text='Пользователь с таким id не найден')
            else:
                username = list_arguments[0].replace('@', '')
                user: User = await rq.get_user_username(username=username)
                if user:
                    await rq.change_honor(tg_id=user.tg_id, sign=sign, number=int(numbers))
                    await message.answer(f"Честь у пользователя {user.nickname} изменилась "
                                         f"на {list_arguments[1]}")
                else:
                    await message.answer(text='Пользователь с таким username не найден')
        else:
            await message.answer("Вы указали неправильный знак, можно использовать + или -")
