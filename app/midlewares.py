from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from app.database.requests import get_user
CACHE = {
    'banned': [6837937583],
}


# class ShadowBanMiddleware(BaseMiddleware):

#     async def __call__(
#         self,
#         handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
#         event: TelegramObject,
#         data: Dict[str, Any]
#     ) -> Any:
        
#         user = await get_user("XAKERRAF777")
#         # print(user. in CACHE.get('banned'))
#         # if user is not None:
#         #     if user.tg_id in CACHE.get('banned'):
#         #         return

#         return await handler(event, data)