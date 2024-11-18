from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile
from database import requests as rq
import logging

router = Router()


@router.callback_query()
async def all_callback(callback: CallbackQuery) -> None:
    logging.info(f'all_callback: {callback.message.chat.id}')
    logging.info(callback.data)


@router.message()
async def all_message(message: Message, bot: Bot) -> None:
    logging.info(f'all_message {message.text}')
    if message.new_chat_members:  # Новый участник
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    if message.left_chat_member:  # Ушел участник
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        general_group = await rq.get_groups_general()
        await bot.ban_chat_member(chat_id=general_group.group_id, user_id=message.from_user.id)
        await bot.unban_chat_member(chat_id=general_group.group_id, user_id=message.from_user.id)

    if message.new_chat_title:  # Новое название чата
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    if message.new_chat_photo:  # Новое фото чата
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    if message.delete_chat_photo:  # Удалено фото чата
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    if message.group_chat_created:  # Группа была создана
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    if message.supergroup_chat_created:  # Супергруппа была создана
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    if message.channel_chat_created:  # Канал был создан
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    if message.migrate_to_chat_id:  # Группа преобразована в супергруппу
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    if message.migrate_from_chat_id:  # Супергруппа преобразована в группу
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    if message.pinned_message:  # Закрепленное сообщение
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    general_group = await rq.get_groups_general()
    member = await bot.get_chat_member(user_id=message.from_user.id,
                                       chat_id=general_group.group_id)
    if member.status == 'left':
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await message.answer('К сожалению, вы не состоите в общем чате клана и отправка сообщений вам не доступна.\n\n'
                             'Пройдите опрос в боте @clan_by_bot для добавления в общий чат клана.')
        return

    if message.photo:
        logging.info(f'all_message message.photo')
        logging.info(message.photo[-1].file_id)

    if message.sticker:
        logging.info(f'all_message message.sticker')
        logging.info(message.sticker.file_id)

    if message.text == '/get_logfile':
        file_path = "py_log.log"
        await message.answer_document(FSInputFile(file_path))

    if message.text == '/get_DB':
        file_path = "database/db.sqlite3"
        await message.answer_document(FSInputFile(file_path))

