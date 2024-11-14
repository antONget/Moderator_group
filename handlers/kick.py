import logging

from aiogram import Router, Bot, F
from aiogram.types import Message
from filter.filter_group import is_admin
from aiogram.filters import Command, CommandObject
from utils.error_handling import error_handler
from database import requests as rq

router = Router()
router.message.filter(F.chat.type != "private")


@router.message(Command('kick'))
@error_handler
async def into_command_kick_user(message: Message, command: CommandObject, bot: Bot):
    logging.info('into_command_kick_user')
    if not await is_admin(message, bot):
        await message.reply("Для использования этой команды бот должен быть администратором в канале,"
                            " а вы администратором или владельцем")
        return
    user_identifier = 0
    if not command.args:
        await message.answer('Для применения команды kick требуется указать к кому и по какой причине она применяется')
        return
    args: list = command.args.split(" ", 1)
    if args:
        user_identifier = args[0]
        if not user_identifier and not message.reply_to_message:
            await message.answer("Кого удалять? Ответьте на сообщение, укажите @username или ID пользователя.")
            return
        reason: str = " ".join(args[1:]) if len(args) > 1 else ""
        if not reason:
            await message.answer("Укажите причину kick")
            return
    try:
        if user_identifier:
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
        else:
            user_id = message.reply_to_message.from_user.id
            user = await rq.get_user_tg_id(tg_id=user_id)
        if user_id:
            groups = await rq.get_groups()
            for group in groups:
                member = await bot.get_chat_member(user_id=message.from_user.id,
                                                   chat_id=group.group_id)
                if member.status != 'left':
                    await bot.ban_chat_member(chat_id=group.group_id, user_id=user_id, until_date=60)
            admin = await rq.get_user_tg_id(tg_id=message.from_user.id)
            await message.answer(f"Администратор <a href='tg://user?id={message.from_user.id}'>"
                                 f"{message.from_user.full_name}</a> кикнул <a href='tg://user?id={user_id}'>"
                                 f"{user.nickname}</a> по причине: {reason}")
                
        else:
            await message.reply("Пользователь не найден.")
    except Exception as e:
        await message.reply(f"Не удалось кикнуть пользователя. Ошибка: {e}")
