import asyncio
import logging
import sqlite3
from aiogram import Router, Bot, Dispatcher, types, F
from aiogram.filters import CommandObject, Command, StateFilter
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from utils.error_handling import error_handler
from filter.filter_group import is_admin_bot_in_group
from filter.admin_filter import check_super_admin
from database import requests as rq

router = Router()
router.message.filter(F.chat.type != "private")


@router.message(Command('set_group'))
@error_handler
async def process_add_group(message: Message, command: CommandObject, bot: Bot):
    logging.info('process_add_group')
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)  # Удаление сообщения
    group_link = command.args
    chat_id = message.chat.id
    if not await is_admin_bot_in_group(message=message, bot=bot) or not await check_super_admin(telegram_id=message.from_user.id):
        await message.reply("Для использования этой команды бот должен быть администратором в канале,"
                            " а вы администратором проекта")
        return
    if not group_link:
        return await message.reply('Для применения команды /get_group нужно прислать ссылку')
    groups = await rq.get_groups_group_id(group_id=chat_id)
    if not groups:
        data = {"group_id": chat_id, "group_clan": "clan", "group_link": group_link}
        await rq.add_new_group(data=data)
        await message.answer(text='Группа добавлена в проект')
        return
    else:
        await message.answer('Группа уже есть в базе')


@router.message(Command('set_group_general'))
@error_handler
async def process_add_group_general(message: Message, command: CommandObject, bot: Bot):
    logging.info('process_add_group_general')

    group_link = command.args
    chat_id = message.chat.id
    if not await is_admin_bot_in_group(message=message, bot=bot) or not \
            await check_super_admin(telegram_id=message.from_user.id):
        await message.reply("Для использования этой команды бот должен быть администратором в канале,"
                            " а вы администратором проекта")
        return
    if not group_link:
        return await message.reply('Для применения команды /get_group_general нужно прислать ссылку')
    group = await rq.get_groups_group_id(group_id=chat_id)
    if not group:
        data = {"group_id": chat_id, "group_clan": "general", "group_link": group_link}
        await rq.add_new_group(data=data)
        await message.reply(text='Группа добавлена как основная')
        return
    else:
        await rq.update_group_general(group_id=chat_id, group_link=group_link)
        await message.reply(text='Основная группа обновлена')
