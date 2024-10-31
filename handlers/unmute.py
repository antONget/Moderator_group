from filter.filter_group import parse_time, is_admin
from aiogram.types import Message, ChatPermissions
from aiogram.filters import Command, CommandObject
from aiogram import Bot, Router, F


router = Router()
router.message.filter(F.chat.type != "private")


@router.message(Command("unmute"))
async def func_unmute(message: Message, command: CommandObject, bot: Bot):
    reply_message = message.reply_to_message

    if not reply_message:
        return await message.reply('Для применения команды /unmute требуется ответить на сообщение пользователя')
    if not await is_admin(message, bot):
        await message.reply("Для использования команды /unmute бот должен быть администратором в канале,"
                            " а вы администратором или владельцем")
        return

    mention = reply_message.from_user.mention_html(reply_message.from_user.first_name)

    await bot.restrict_chat_member(chat_id=message.chat.id, user_id=reply_message.from_user.id,
                                   permissions=ChatPermissions(can_send_messages=True,
                                                               can_send_other_messages=True))
    await message.answer(f" Все ограничения с пользователя <b>{mention}</b> были сняты!")