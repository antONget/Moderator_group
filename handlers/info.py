import logging

from aiogram import Router, F, Bot
from aiogram.types import Message
from database import requests as rq
from database.models import User
from utils.error_handling import error_handler
from aiogram.filters import CommandObject, Command

router = Router()
router.message.filter(F.chat.type != "private")


@router.message(Command('info'))
@error_handler
async def into_command_info(message: Message, bot: Bot, command: CommandObject) -> None:
    logging.info('into_command_info')
    user_identifier = command.args
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)  # Удаление сообщения
    if not user_identifier and not message.reply_to_message:
        await message.answer('Для применения команды /info требуется ответить на сообщение'
                             ' пользователя или прислать его username')
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
                    await message.answer("Пользователь c таким username не найден в БД, попробуйте применить"
                                         " команду использую ID пользователя")
                    return
        else:
            user_id = message.reply_to_message.from_user.id
        if user_id:
            user: User = await rq.get_user_tg_id(tg_id=user_id)
            if user:

                await message.answer(text=f'Клан: {user.clan_name}\n\n'  # Вывод названия клана (пока None)
                                          f'Ник: {user.nickname}\n'
                                          f'ID: <code>{user.id_PUBG_MOBILE}</code>\n'
                                          f'Имя: <a href="tg://user?id={user.tg_id}">{user.name}</a>\n'
                                          f'Возраст: {user.age}\n'
                                          f'Честь: {user.honor}\n'
                                          f'В клане с {user.data_registration}')
            else:
                await message.answer("Пользователь не найден.")
    except Exception as e:
        await message.answeer(f"Не удалось получить информацию о пользователе. Ошибка: {e}")
