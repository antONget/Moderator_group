import asyncio
import logging

from aiogram import Router, F, Bot
from aiogram.types import Message
from database import requests as rq
from database.models import User, ChatAction
from utils.error_handling import error_handler
from aiogram.filters import CommandObject, Command

router = Router()
router.message.filter(F.chat.type != "private")


@router.message(Command('info'))
@error_handler
async def into_command_info(message: Message, bot: Bot, command: CommandObject) -> None:
    """
    Обработка команды /info
    :param message:
    :param bot:
    :param command:
    :return:
    """
    logging.info('into_command_info')
    # удаляем команду
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if message.reply_to_message:
        user_to_action = message.reply_to_message.from_user.id
        await info_info_process(user_to_action=user_to_action, message=message)
    else:
        argument = command.args
        if argument:
            if argument.isdigit():
                user_to_action = int(argument)
                await info_info_process(user_to_action=user_to_action, message=message)
            else:
                username: str = argument.replace('@', '')
                user: User = await rq.get_user_username(username=username)
                if user:
                    user_to_action = user.tg_id
                    await info_info_process(user_to_action=user_to_action, message=message)
                else:
                    msg = await message.answer(text=f'Пользователя с username {argument} не найден')
                    await asyncio.sleep(5)
                    await msg.delete()
        else:
            user_to_action = message.from_user.id
            await info_info_process(user_to_action=user_to_action, message=message)


async def info_info_process(user_to_action: int, message: Message):
    """
    Процесс информирования пользователя и администратора о применении команды info
    :param user_to_action:
    :param message:
    :return:
    """
    logging.info('info_info_process')
    user: User = await rq.get_user_tg_id(tg_id=user_to_action)
    if user:
        actions_all: list[ChatAction] = await rq.get_chat_action_tg_id(tg_id=user_to_action,
                                                                       type_action='warn',
                                                                       count_day=-1)
        await message.answer(text=f'Клан: {user.clan_name}\n\n'
                                  f'Ник: {user.nickname}\n'
                                  f'ID: <code>{user.id_PUBG_MOBILE}</code>\n'
                                  f'Имя: <a href="tg://user?id={user.tg_id}">{user.name}</a>\n'
                                  f'Возраст: {user.age}\n'
                                  f'Честь: {user.honor}\n'
                                  f'Количество выговоров: {len(actions_all)}\n'
                                  f'В клане с {user.data_registration}')
    else:
        msg = await message.answer(text='Пользователь не найден')
        await asyncio.sleep(5)
        await msg.delete()
