from aiogram import Dispatcher, Bot
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
from aiogram import BaseMiddleware

from database.models import ClanGroup
from database.requests import get_groups

class ChatRestrictionMiddleware(BaseMiddleware):

    async def __call__(self, handler, event, data):

        if event.new_chat_member.status == 'member' and event.new_chat_member.user.id == bot.id:
            list_group: list[ClanGroup] = await get_groups()
            list_group_peer = [group.group_id for group in list_group]
            if event.chat.id not in list_group_peer:
                await bot.leave_chat(event.chat.id)