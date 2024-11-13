from filter.filter_group import parse_time, is_admin
from aiogram.types import Message, ChatPermissions
from aiogram.filters import Command, CommandObject
from aiogram import Bot, Router, F
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from database import requests as rq

router = Router()
router.message.filter(F.chat.type != "private")


@router.message(Command("mute"))
async def func_mute(message: Message, command: CommandObject, bot: Bot):
    reply_message = message.reply_to_message
    mention = reply_message.from_user.mention_html(reply_message.from_user.first_name)

    if not await is_admin(message, bot):
        await message.reply("Для использования этой команды бот должен быть администратором в канале,"
                            " а вы администратором или владельцем")
        return
    args = command.args.split(" ")
    user_identifier = [args[0]] if args else []
    if "@" in user_identifier[0]:
        user_identifier = user_identifier[0].replace("@", "")
    chat_id = message.chat.id
    if not user_identifier and not message.reply_to_message:
        await message.answer("Кого заглушить? Ответьте на сообщение, укажите ник или ID пользователя.")
        return

    try:
        if user_identifier:
            try:
                user_id = int(user_identifier[0])
                mention = "Имени нет"
            except ValueError:
                data = await rq.parse1(user_identifier)
                user_id = data[0] if data else None
                mention = user_identifier
        else:
            user_id = message.reply_to_message.from_user.id
            mention = message.reply_to_message.from_user.mention_html(message.reply_to_message.from_user.first_name)

        if user_id:
            chats =await rq.get_rows_with_role_clan()
            if chats:
                for chat_id in chats:
                    if not user_id:
                        pass
                    else:
                        with suppress(TelegramBadRequest):
                            await bot.restrict_chat_member(chat_id=chat_id, user_id=user_id,
                                       permissions=ChatPermissions(can_send_messages=False))
                            await message.answer(f" Пользователь <b>{mention}</b> был заглушен!")
            else:
                with suppress(TelegramBadRequest):
                    await bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id,
                                       permissions=ChatPermissions(can_send_messages=False))
                    await message.answer(f" Пользователь <b>{mention}</b> был заглушен!")
                
        else:
            await message.reply("Пользователь не найден.")
    except Exception as e:
        await message.reply(f"Не удалось забанить пользователя. Ошибка: {e}")