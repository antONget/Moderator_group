import asyncio
import logging

from aiogram import Router, F, Bot
from aiogram.types import Message
from database import requests as rq
from database.models import User, ClanGroup
from utils.error_handling import error_handler
from aiogram.filters import CommandObject, Command

router = Router()
router.message.filter(F.chat.type == "private")


@router.message(Command('member'))
@error_handler
async def into_command_member(message: Message, bot: Bot, command: CommandObject) -> None:
    """
    Обработка команды /member
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
        await info_member_process(user_to_action=user_to_action, message=message, bot=bot)
    else:
        argument = command.args
        if argument:
            if argument.isdigit():
                user_to_action = int(argument)
                await info_member_process(user_to_action=user_to_action, message=message, bot=bot)
            else:
                username: str = argument.replace('@', '')
                user: User = await rq.get_user_username(username=username)
                if user:
                    user_to_action = user.tg_id
                    await info_member_process(user_to_action=user_to_action, message=message, bot=bot)
                else:
                    msg = await message.answer(text=f'Пользователя с username {argument} не найден')
                    await asyncio.sleep(5)
                    await msg.delete()
        else:
            user_to_action = message.from_user.id
            await info_member_process(user_to_action=user_to_action, message=message)


async def info_member_process(user_to_action: int, message: Message, bot: Bot):
    """
    Процесс информирования пользователя и администратора о применении команды info
    :param user_to_action:
    :param message:
    :param bot:
    :return:
    """
    logging.info('info_member_process')
    user: User = await rq.get_user_tg_id(tg_id=user_to_action)
    groups: list[ClanGroup] = await rq.get_groups()
    text = f'<b>Статус пользователя {user.name} {user.clan_name}\n\n'
    for group in groups:
        try:
            member = await bot.get_chat_member(user_id=user.tg_id,
                                               chat_id=message.chat.id)
            text += f'<i>{group.group_title}</i> - {member.status}\n'
        except:
            pass
    if user:
        await message.answer(text=text)
    else:
        msg = await message.answer(text='Пользователь не найден')
        await asyncio.sleep(5)
        await msg.delete()
