import logging

from aiogram import Router, F, Dispatcher, Bot
from aiogram.types import Message
from aiogram.filters import CommandObject, Command
from datetime import timedelta
from database import requests as rq
from database.models import User
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database import requests
from utils.error_handling import error_handler
from aiogram.filters import  Command, StateFilter
from filter.filter_group import is_admin
import asyncio
import datetime

router = Router()
router.message.filter(F.chat.type != "private")


@router.message(Command("set_lider"))
@error_handler
async def process_command_kick(message: Message, command: CommandObject, bot: Bot):
    """
    Обработка команды /set_lider
    /set_lider - если ответным сообщением
    /set_lider @username
    :param message:
    :param command:
    :param bot:
    :return:
    """
    logging.info('process_command_set_lider')
    # удаляем сообщение с командой
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    # проверка что команду использует администратор или владелец чата
    if not await is_admin(message, bot):
        msg = await message.answer(text="Для использования этой команды бот должен быть администратором в канале,"
                                        " а вы администратором или владельцем")
        await asyncio.sleep(5)
        await msg.delete()
        return
    # флаг ответного сообщения
    reply_message = message.reply_to_message
    # ОЖИДАЕМ ОТ ПОЛЬЗОВАТЕЛЬ: /set_lider - если ответным сообщением
    if reply_message:
        user_to_action = reply_message.from_user.id
        user: User = await rq.get_user_tg_id(tg_id=user_to_action)
        if user:
            await set_lider_info_process(user_to_action=user_to_action, message=message, bot=bot)
    else:
        arguments = command.args
        if not arguments:
            msg = await message.answer(text='Для применения команды /set_lider необходимо в параметрах указать пользователя'
                                            ' (@username или телеграм id),'
                                            ' к которому применяется эта команда, например: '
                                            '/set_lider @username')
            await asyncio.sleep(5)
            await msg.delete()
            return
        else:
            if arguments.isdigit():
                user_to_action = int(arguments)
                user: User = await rq.get_user_tg_id(tg_id=user_to_action)
                if user:
                    await set_lider_info_process(user_to_action=user_to_action,
                                                 message=message,
                                                 bot=bot)
                else:
                    await message.answer(text='Пользователь с таким id не найден')
            else:
                username = arguments.replace('@', '')
                user: User = await rq.get_user_username(username=username)
                if user:
                    await set_lider_info_process(user_to_action=user.tg_id,
                                                 message=message,
                                                 bot=bot)
                else:
                    await message.answer(text='Пользователь с таким username не найден')


async def set_lider_info_process(user_to_action: int, message: Message, bot: Bot):
    """
    Процесс информирования пользователя и администратора о применении команды set_lider
    :param user_to_action:
    :param message:
    :param bot:
    :return:
    """
    logging.info('set_lider_info_process')
    date_chat_action = datetime.datetime.today()
    date_chat_action = date_chat_action.strftime('%d-%m-%Y %H:%M')
    type_chat_action = 'set_lider'
    reason_chat_action = '---'
    data_chat_action = {'tg_id': user_to_action,
                        'type_action': type_chat_action,
                        'data_action': date_chat_action,
                        'reason_action': reason_chat_action}
    await rq.add_chat_action(data=data_chat_action)
    user: User = await rq.get_user_tg_id(tg_id=user_to_action)
    await rq.update_user_role(tg_id=user.tg_id, role=rq.UserRole.lider)
    await message.answer(f"Администратор <a href='tg://user?id={message.from_user.id}'>"
                         f"{message.from_user.full_name}</a> назначил лидером клана"
                         f" <a href='tg://user?id={user_to_action}'>"
                         f"{user.nickname if user.nickname else user.username}</a>")