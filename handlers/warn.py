from database.requests import update_warn
from filter.filter_group import parse_time, is_admin
from aiogram.types import Message, ChatPermissions
from aiogram.filters import Command, CommandObject
from aiogram import Bot, Router, F
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from database import requests as rq
import datetime as DT
import logging
import handlers.verification_ as vr

router = Router()
router.message.filter(F.chat.type != "private")


@router.message(Command("warn"))
async def func_mute(message: Message, command: CommandObject, bot: Bot):
    reply_message = message.reply_to_message
    message_id = message.message_id
    reply_id=message.reply_to_message.from_user.id
    if not await is_admin(message, bot):
        await message.answer("Для использования этой команды бот должен быть администратором в канале,"
                            " а вы администратором или владельцем")
        return
    if not command.args:
        await message.answer('Вы вообще что нибудь написали?')
        return
    args: list = command.args.split(" ", 1)
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)# Удаление сообщения
    if args:
        user_identifier = args[0]
        if not user_identifier and not message.reply_to_message:
            await message.answer("Кому выговор? Ответьте на сообщение, укажите @username или ID пользователя.")
            return
        reason_: str = " ".join(args[0:]) if len(args) > 1 else ""
        reason: str = " ".join(args[1:]) if len(args) > 1 else ""
        if not reason and not message.reply_to_message.from_user.id:
            await message.answer("Укажите причину warn")
            return
        else:
            reason = reason_
    try:
        if reply_id:
            user_id = message.reply_to_message.from_user.id
            mention = message.reply_to_message.from_user.mention_html(message.reply_to_message.from_user.first_name)
        else:
            try:
                user_id = int(user_identifier)
            except ValueError:
                user = await rq.get_user_username(username=user_identifier.replace("@", ""))
                if user:
                    user_id = user.tg_id
                else:
                    await message.reply("Пользователь c таким username не найден в БД, попробуйте применить"
                                        " команду использую ID пользователя")
                    return


        if user_id:
            date = DT.datetime.today()
            date += DT.timedelta(hours=168)
            warn = str(f'warn \n {str(date)}\n {reason}\n')
            await update_warn(tg_id=user_id, warn=warn)
            verification = await vr.pruf_sum_warn(tg_id=user_id)
            if verification == 0:
                groups = await rq.get_groups()
                for group in groups:
                    member = await bot.get_chat_member(user_id=user_id,
                                                       chat_id=group.group_id)
                    if member.status != 'left':
                        await bot.ban_chat_member(chat_id=group.group_id, user_id=user_id)
            user = await rq.get_user_tg_id(tg_id=user_id)
            await message.answer(f"Пользователь {user.username} исключен из клана в связи с достижением 5 выговоров")
            if verification == 1:
                await message.answer(f"Пользователь {user.username} получил выговор")
        else:
            await message.reply("Пользователь не найден.")
    except Exception as e:
        await message.answer(f"Не удалось дать выговор пользователя. Ошибка: {e}")
