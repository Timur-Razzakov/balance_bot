from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from data.config import ADMIN_ID


class AdminOnlyMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = None

        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id

        if user_id not in ADMIN_ID:
            if isinstance(event, Message):
                await event.answer("⛔ У тебя нет доступа к этому боту")
            elif isinstance(event, CallbackQuery):
                await event.answer("⛔ Нет доступа", show_alert=True)
            return

        return await handler(event, data)
