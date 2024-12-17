from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from cachetools import TTLCache

CACHE = TTLCache(maxsize=10_000, ttl=1)  # Максимальный размер кэша - 10000 ключей, а время жизни ключа - 5 секунд


class ThrottlingMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user: User = data.get('event_from_user')
        if user.id in [5842594683, 2063026859, 7124671736, 5581601063, 5687278454, 6894696433, 6692981863,
                       1076862578, 6517086173, 6830053157, 7272511490, 6338244821, 5830784729, 1737348162,
                       641098473, 6634983438, 1095124331, 6639612091, 7157160550, 5520806785, 5622640831,
                       5674038978, 6338244821, 5622478844, 1649610927, 6789844460, 6448254413, 7387419272,
                       5950250196, 1372825997]:
            return
        if user.id in CACHE:
            return

        CACHE[user.id] = True

        return await handler(event, data)
