from aiogram import Router, Bot, F
from aiogram.types import Message
from filter.filter_group import is_admin
from aiogram.filters import Command, CommandObject
from datetime import timedelta
from database import requests as rq

router = Router()
router.message.filter(F.chat.type != "private")


@router.message(Command('kick'))
async def kick_user(message: Message, command: CommandObject, bot: Bot):
    reply_message = message.reply_to_message

    if not reply_message:
        return await message.reply('Для применения команды /mute требуется ответить на сообщение пользователя')
    if not await is_admin(message, bot):
        await message.reply("Для использования этой команды бот должен быть администратором в канале,"
                            " а вы администратором или владельцем")
        return
    try:
        args: str = command.args
        if args:
            await message.reply("Пожалуйста, укажите причину удаления пользователя")
    except:
        await message.reply("Пожалуйста, укажите причину удаления пользователя")
        return
    admin_id = message.from_user.id
    admin_name = message.from_user.username
    kick_name = message.reply_to_message.from_user.username
    kick_id = message.reply_to_message.from_user.id
    user_admin = rq.get_user(tg_id=admin_id)
    user_kick = rq.get_user(tg_id=kick_id)

    seconds = 60
    await bot.ban_chat_member(chat_id=message.chat.id, user_id=kick_id, until_date=timedelta(seconds=seconds))
    await message.answer(text=f'Администратор <a href="tg://user?id={user_admin[0]}">{user_admin[2]}</a>'
                              f' кикнул <a href="tg://user?id={user_kick[0]}">{user_kick[2]}</a> по причине:'
                              f' {args}')

