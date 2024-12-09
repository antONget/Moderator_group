import logging

from aiogram import Bot, Router, F
from filter.filter_group import is_admin
from aiogram.types import Message
from utils.error_handling import error_handler
from aiogram.filters import Command

router = Router()
router.message.filter(F.chat.type != "private")


@router.message(Command("del"))
@error_handler
async def __message_delete_(message: Message, bot: Bot):
    logging.info('message_delete')
    await message.delete()
    if not await is_admin(message=message, bot=bot):
        await message.reply("Для использования этой команды бот должен быть администратором в канале,"
                            " а вы администратором или владельцем")
        return

    replied_message_id = message.reply_to_message.message_id
    if replied_message_id:
        await bot.delete_message(chat_id=message.chat.id, message_id=replied_message_id)
    else:
        await message.answer("Вы не ответили ни на какое сообщение.")
