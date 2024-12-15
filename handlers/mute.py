from filter.filter_group import is_admin
from aiogram.types import Message, ChatPermissions
from aiogram.filters import Command, CommandObject
from aiogram import Bot, Router, F
from aiogram.enums.chat_member_status import ChatMemberStatus
from database import requests as rq
from database.models import User
from utils.error_handling import error_handler
import datetime
import logging
import asyncio

router = Router()
router.message.filter(F.chat.type != "private")


@router.message(Command("mute"))
@error_handler
async def process_command_mute(message: Message, command: CommandObject, bot: Bot):
    """
    Обработка команды /mute
    /mute @username [срок в часах, цифрой] [причина]
    /mute [срок в часах, цифрой] [причина] - если ответным сообщением
    :param message:
    :param command:
    :param bot:
    :return:
    """
    logging.info('process_command_mute')
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
    # ОЖИДАЕМ ОТ ПОЛЬЗОВАТЕЛЬ: /mute [срок в часах, цифрой] [причина] - если ответным сообщением
    if reply_message:
        arguments = command.args
        if not arguments:
            msg = await message.answer(
                'Для применения команды /mute требуется указать срок в часах и по какой причине она применяется')
            await asyncio.sleep(5)
            await msg.delete()
            return
        else:
            list_arguments = arguments.split(' ', 1)
            if len(list_arguments) == 2:
                hour = list_arguments[0]
                if hour.isdigit():
                    hour_mute = int(hour)
                else:
                    msg = await message.answer(
                        text='Количество часов необходимо указать числом')
                    await asyncio.sleep(5)
                    await msg.delete()
                    return

                user_to_action = reply_message.from_user.id
                user: User = await rq.get_user_tg_id(tg_id=user_to_action)
                if user:
                    await mute_info_process(user_to_action=user_to_action,
                                            reason=list_arguments[1],
                                            message=message,
                                            hour_mute=hour_mute,
                                            bot=bot)
            else:
                msg = await message.answer(
                    text='Для применения команды /mute необходимо в параметрах указать срок в часах'
                         ' и причину ее применения, например: /mute 5 Причина')
                await asyncio.sleep(5)
                await msg.delete()
                return
    else:
        # ОЖИДАЕМ ОТ ПОЛЬЗОВАТЕЛЬ: /mute @username [срок в часах, цифрой] [причина]
        arguments = command.args
        if not arguments:
            msg = await message.answer(text='Для применения команды /mute необходимо в параметрах указать срок в часах'
                                            ' и причину ее применения, например: /mute 5 Причина')
            await asyncio.sleep(5)
            await msg.delete()
            return
        list_arguments: list = arguments.split(' ', 2)
        if len(list_arguments) == 3:
            # если указан id пользователя
            if list_arguments[0].isdigit():
                user_to_action = int(list_arguments[0])
                user: User = await rq.get_user_tg_id(tg_id=user_to_action)
                if user:
                    if list_arguments[1].isdigit():
                        hour_mute = int(list_arguments[1])
                        await mute_info_process(user_to_action=user_to_action,
                                                reason=list_arguments[2],
                                                message=message,
                                                hour_mute=hour_mute,
                                                bot=bot)
                    else:
                        msg = await message.answer(
                            text='Количество часов необходимо указать числом')
                        await asyncio.sleep(5)
                        await msg.delete()
                        return
                else:
                    await message.answer(text='Пользователь с таким id не найден')
            else:
                username = list_arguments[0].replace('@', '')
                user: User = await rq.get_user_username(username=username)
                if user:
                    if list_arguments[1].isdigit():
                        hour_mute = int(list_arguments[1])
                        await mute_info_process(user_to_action=user.tg_id,
                                                reason=list_arguments[2],
                                                message=message,
                                                hour_mute=hour_mute,
                                                bot=bot)
                    else:
                        msg = await message.answer(
                            text='Количество часов необходимо указать числом')
                        await asyncio.sleep(5)
                        await msg.delete()
                        return

                else:
                    await message.answer(text='Пользователь с таким username не найден')
        else:
            await message.answer(text='Для применения команды /mute необходимо в параметрах указать срок в часах'
                                      ' и причину ее применения, например: /mute 5 Причина')


async def mute_info_process(user_to_action: int, reason: str, message: Message, hour_mute: int, bot: Bot):
    """
    Процесс информирования пользователя и администратора о применении команды warn
    :param user_to_action:
    :param reason:
    :param message:
    :param hour_mute:
    :param bot:
    :return:
    """
    logging.info('warn_info_process')
    date_chat_action = datetime.datetime.today()
    date_chat_action = date_chat_action.strftime('%d-%m-%Y %H:%M')
    type_chat_action = 'mute'
    reason_chat_action = reason
    data_chat_action = {'tg_id': user_to_action,
                        'type_action': type_chat_action,
                        'data_action': date_chat_action,
                        'reason_action': reason_chat_action}
    await rq.add_chat_action(data=data_chat_action)
    user: User = await rq.get_user_tg_id(tg_id=user_to_action)
    only_read_permissions = ChatPermissions(can_send_messages=False,
                                            can_send_media_messages=False,
                                            can_send_polls=False,
                                            can_send_other_messages=False,
                                            can_add_web_page_previews=False,
                                            can_change_info=False,
                                            can_invite_users=False,
                                            can_pin_messages=False)
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if member in [ChatMemberStatus.CREATOR]:
        until_date = datetime.datetime.now() + datetime.timedelta(minutes=hour_mute)
        await bot.restrict_chat_member(chat_id=message.chat.id,
                                       user_id=user_to_action,
                                       permissions=ChatPermissions(can_send_messages=False),
                                       until_date=until_date)
        await message.answer(f"Администратор <a href='tg://user?id={message.from_user.id}'>"
                             f"{message.from_user.full_name}</a> замутил пользователя "
                             f" <a href='tg://user?id={user_to_action}'>"
                             f"{user.nickname if user.nickname else user.username}</a> на {hour_mute} часов по причине: {reason}")
    else:
        await message.answer(f'🚫 Этому пользователю нельзя ограничить возможность отправки сообщений!')
