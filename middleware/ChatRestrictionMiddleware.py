from aiogram import Dispatcher, Bot
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
from aiogram import BaseMiddleware

from database.models import ClanGroup
from database.requests import get_groups

class ChatRestrictionMiddleware(BaseMiddleware):

    async def __call__(self, handler, event, data):
        # Пропускаем события ChatMemberUpdated
        if isinstance(event, ChatMemberUpdated):
            return await handler(event, data)

        # Получаем chat_id из события
        chat = None
        if isinstance(event, Message):
            chat = event.chat
        elif isinstance(event, CallbackQuery) and event.message:
            chat = event.message.chat

        # Если чат не определён, пропускаем
        if not chat:
            return await handler(event, data)

        # Разрешаем личные сообщения
        if chat.type == 'private':
            return await handler(event, data)
        list_group: list[ClanGroup] = await get_groups()
        list_group_peer = [group.group_id for group in list_group]
        # Проверяем разрешённые чаты
        if chat.id not in list_group_peer:
            return  # Блокируем обработку

        return await handler(event, data)