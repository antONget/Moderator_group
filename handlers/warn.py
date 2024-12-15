import asyncio

from filter.filter_group import is_admin
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram import Bot, Router, F
from database import requests as rq
from database.models import User, ChatAction
import datetime
import logging

router = Router()
router.message.filter(F.chat.type != "private")


@router.message(Command("warn"))
async def process_command_warn(message: Message, command: CommandObject, bot: Bot):
    """
    Обработка команды /warn
    /warn [причина] - если ответным сообщением
    /warn @username [причина]
    :param message:
    :param command:
    :param bot:
    :return:
    """
    logging.info('process_command_warn')
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
    # ОЖИДАЕМ ОТ ПОЛЬЗОВАТЕЛЬ: /warn [причина] - если ответным сообщением
    if reply_message:
        reason = command.args
        if not reason:
            msg = await message.answer(
                'Для применения команды /warn требуется указать по какой причине она применяется')
            await asyncio.sleep(5)
            await msg.delete()
            return
        else:
            user_to_action = reply_message.from_user.id
            user: User = await rq.get_user_tg_id(tg_id=user_to_action)
            if user:
                await warn_info_process(user_to_action=user_to_action, reason=reason, message=message, bot=bot)
    else:
        arguments = command.args
        if not arguments:
            msg = await message.answer(text='Для применения команды /warn необходимо в параметрах указать пользователя'
                                            ' (@username или телеграм id),'
                                            ' к которому применяется эта команда и причину ее применения, например: '
                                            '/warn @username Причина предупреждения')
            await asyncio.sleep(5)
            await msg.delete()
            return
        list_arguments: list = arguments.split(' ', 1)
        if len(list_arguments) == 2:
            if list_arguments[0].isdigit():
                user_to_action = int(list_arguments[0])
                user: User = await rq.get_user_tg_id(tg_id=user_to_action)
                if user:
                    await warn_info_process(user_to_action=user_to_action, reason=list_arguments[1], message=message,
                                            bot=bot)
                else:
                    await message.answer(text='Пользователь с таким id не найден')
            else:
                username = list_arguments[0].replace('@', '')
                user: User = await rq.get_user_username(username=username)
                if user:
                    await warn_info_process(user_to_action=user.tg_id,
                                            reason=list_arguments[1],
                                            message=message,
                                            bot=bot)
                else:
                    await message.answer(text='Пользователь с таким username не найден')
        else:
            await message.answer(text='Для применения команды /warn необходимо в параметрах указать пользователя'
                                      ' (@username или телеграм id),'
                                      ' к которому применяется эта команда и причину ее применения, например: '
                                      '/warn @username Причина предупреждения')


async def warn_info_process(user_to_action: int, reason: str, message: Message, bot: Bot):
    """
    Процесс информирования пользователя и администратора о применении команды warn
    :param user_to_action:
    :param reason:
    :param message:
    :param bot:
    :return:
    """
    logging.info('warn_info_process')
    date_chat_action = datetime.datetime.today()
    date_chat_action = date_chat_action.strftime('%d-%m-%Y %H:%M')
    type_chat_action = 'warn'
    reason_chat_action = reason
    data_chat_action = {'tg_id': user_to_action,
                        'type_action': type_chat_action,
                        'data_action': date_chat_action,
                        'reason_action': reason_chat_action}
    await rq.add_chat_action(data=data_chat_action)
    user: User = await rq.get_user_tg_id(tg_id=user_to_action)
    actions_7: list[ChatAction] = await rq.get_chat_action_tg_id(tg_id=user_to_action,
                                                                 type_action='warn',
                                                                 count_day=7)
    if len(actions_7) == 5:
        await bot.ban_chat_member(chat_id=message.chat.id, user_id=user_to_action)
        await message.answer(text=f"Пользователь <a href='tg://user?id={user_to_action}'>"
                                  f"{user.nickname if user.nickname else user.username}</a> "
                                  f"исключен из клана в связи с достижением 5 выговоров")
    actions_all: list[ChatAction] = await rq.get_chat_action_tg_id(tg_id=user_to_action,
                                                                   type_action='warn',
                                                                   count_day=-1)
    await message.answer(f"Администратор <a href='tg://user?id={message.from_user.id}'>"
                         f"{message.from_user.full_name}</a> объявил предупреждение"
                         f" <a href='tg://user?id={user_to_action}'>"
                         f"{user.nickname if user.nickname else user.username}</a>"
                         f" ({len(actions_7)}/{len(actions_all)})"
                         f" по причине: {reason}")
