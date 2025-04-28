from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile
from database import requests as rq
from database.models import User, ClanGroup
from config_data.config import Config, load_config
import logging
import asyncio
from keyboards.keyboard import main_keyboard_group
from utils.error_handling import error_handler

router = Router()
config: Config = load_config()
router.message.filter(F.chat.type != "private")


@router.callback_query()
async def all_callback(callback: CallbackQuery) -> None:
    logging.info(f'all_callback: {callback.message.chat.id}')
    logging.info(callback.data)


async def greeting_users(message: Message, bot: Bot):
    member = await bot.get_chat_member(user_id=message.from_user.id,
                                       chat_id=message.chat.id)
    print(message.from_user.id, message.new_chat_members, member.status)
    if message.new_chat_members:  # Новый участник
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        # если человек зашел в общий чат клана, то бот проверяет, состоит ли данный юзер в чатах клана,
        # если нет, то сразу банит в общем чате
        general_group: ClanGroup = await rq.get_groups_general()
        print(general_group.group_id, message.chat.id)
        if message.chat.id == general_group.group_id:
            text = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>,' \
                   f' добро пожаловать в общий чат клана!'
            await message.answer(text=text,
                                 reply_markup=main_keyboard_group())
            groups: list[ClanGroup] = await rq.get_groups()
            is_ban = True
            for group in groups:
                if group.group_clan == 'general':
                    continue
                else:
                    try:
                        member = await bot.get_chat_member(user_id=message.from_user.id,
                                                           chat_id=group.group_id)
                        if member.status in ['member', 'administrator']:
                            is_ban = False
                    except:
                        pass
            if is_ban:
                msg = await message.answer(text=f'Пользователь {message.from_user.id} не состоит в клановских беседах'
                                                f' и будет забанен на один час')
                await asyncio.sleep(1 * 60)
                await msg.delete()
                await bot.ban_chat_member(chat_id=general_group.group_id, user_id=message.from_user.id)
                await asyncio.sleep(60 * 60)
                await bot.unban_chat_member(chat_id=general_group.group_id, user_id=message.from_user.id)
        else:
            await message.answer(text=f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>,\n\n"
                                      f"Если ты еще не зашел в общий чат клана, то не сможешь писать сообщения,"
                                      f" перейди в бота @clan_by_bot напиши команду /start и команду"
                                      f" /opros для прохождения опроса.",
                                 reply_markup=main_keyboard_group())

    if message.left_chat_member:  # Ушел участник
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        general_group = await rq.get_groups_general()
        try:
            await bot.ban_chat_member(chat_id=general_group.group_id, user_id=message.from_user.id)
            await asyncio.sleep(5)
            await bot.unban_chat_member(chat_id=general_group.group_id, user_id=message.from_user.id)
        except:
            pass


@router.message()
async def all_message(message: Message, bot: Bot, ) -> None:
    logging.info(f'all_message {message.text}')
    # await greeting_users(message=message, bot=bot)
    # if message.new_chat_member.status == 'kick':  # Кикнули участника
    #     general_group = await rq.get_groups_general()
    #     await bot.ban_chat_member(chat_id=general_group.group_id, user_id=message.from_user.id)
    #     await asyncio.sleep(5)
    #     await bot.unban_chat_member(chat_id=general_group.group_id, user_id=message.from_user.id)

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

    #  ------ реакция на сообщения
    if message.video_chat_started or message.video_chat_ended:
        return
    general_group = await rq.get_groups_general()
    member = await bot.get_chat_member(user_id=message.from_user.id,
                                       chat_id=general_group.group_id)

    logging.info(f'member_status_general_group {member.status}')
    user: User = await rq.get_user_tg_id(tg_id=message.from_user.id)
    if user:
        await rq.update_honor(tg_id=message.from_user.id)

    if message.chat.id != general_group.group_id:
        if message.from_user.username:
            username = message.from_user.username
        else:
            username = 'username'
        await rq.update_clan_name(tg_id=message.from_user.id,
                                  username=username,
                                  clan_name=message.chat.title)

    if member.status in ['left', 'kicked']:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except:
            pass
        msg = await message.answer(
            'К сожалению, вы не состоите в общем чате клана и отправка сообщений вам не доступна.\n\n'
            'Пройдите опрос в боте @clan_by_bot для добавления в общий чат клана.')
        await asyncio.sleep(15)
        await msg.delete()
        return

    user = await rq.get_user_tg_id(tg_id=message.from_user.id)
    if user:
        if user.username != message.from_user.username:  # Проверка актуальности username
            await rq.update_username(tg_id=message.from_user.id, username=message.from_user.username)

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

