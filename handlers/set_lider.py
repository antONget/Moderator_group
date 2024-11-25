import logging

from aiogram import Router, F, Dispatcher, Bot
from aiogram.types import Message
from aiogram.filters import CommandObject, Command
from datetime import timedelta
from database import requests as rq
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database import requests
from utils.error_handling import error_handler
from aiogram.filters import  Command, StateFilter
from filter.filter_group import is_admin

router = Router()
router.message.filter(F.chat.type != "private")


@router.message(Command('set_lider'))
@error_handler
async def into_command_set_lider(message: Message, command: CommandObject, bot: Bot):
    logging.info('into_command_set_lider')
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if not await is_admin(message, bot):
        await message.reply("Для использования этой команды бот должен быть администратором в канале,"
                            " а вы администратором или владельцем")
        return

    user_identifier = command.args

    if not user_identifier and not message.reply_to_message:
        await message.answer("Кого сделать лидером? Ответьте на сообщение, укажите @username или ID пользователя.")
        return

    try:
        if user_identifier:
            try:
                user_id = int(user_identifier)
            except ValueError:
                user = await rq.get_user_username(username=user_identifier.replace('@', ''))
                if user:
                    user_id = user.tg_id
                else:
                    await message.reply("Пользователь c таким username не найден в БД, попробуйте применить"
                                        " команду использую ID пользователя")
                    return
        else:
            user_id = message.reply_to_message.from_user.id

        if user_id:
            await rq.update_user_role(tg_id=user_id, role='lider')
            await message.answer("Лидер назначен.")
        else:
            await message.reply("Пользователь не найден.")
    except Exception as e:
        await message.reply(f"Не удалось назначить лидера. Ошибка: {e}")