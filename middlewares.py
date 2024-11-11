import logging

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram import types, F, Router, flags

from typing import Callable, Dict, Awaitable, Any


logger = logging.getLogger(__name__)
msg_tracker = Router()


# Создаем класс мидлвари, унаследованный от
# aiogram'овского BaseMiddleware
class MessageLogMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        logging.info(event.text) # Выводим текст сообщения
        return await handler(event, data) # Возвращаем обновление хендлерам


