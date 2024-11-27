import json
import os

import logging.config

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import BaseMiddleware
from aiogram.types import Message

from typing import Callable, Dict, Awaitable, Any
from aiogram import F
from aiogram.methods.send_chat_action import SendChatAction
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag
)

import handlers_private
import logging_cfg
import middlewares

logging.config.dictConfig(logging_cfg.LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logger_msg_writer = logging.getLogger('msg_writer')

load_dotenv()

bot = Bot(token=os.getenv('SDP_BOT'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
admin1 = os.getenv('admin1')


class MessageLogMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        await bot.forward_message(admin1, event.chat.id, event.message_id)
        logger_msg_writer.info(f'< chat_id: {event.chat.id} > '
                               f'< chat.username: {event.chat.username} > '
                               f'< chat.first_name: {event.chat.first_name} > '
                               f'< chat.last_name: {event.chat.last_name} > \n'
                               f'< message: {event.text} > ')

        return await handler(event, data)  # Возвращаем обновление хендлерам


dp = Dispatcher()
dp.message.outer_middleware(MessageLogMiddleware())
dp.include_router(handlers_private.private_router)



@dp.message(Command("test1"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
