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


# @dp.message(F.text.contains('к'))
# async def cmd_test3(message: types.Message):
#     await bot.send_chat_action(message.chat.id, 'typing', request_timeout=60)
#     logger.debug(URL_ManageControllerAPI)
#     msg = message.text.split()
#     req = services.GetConfig()
#     res = await req.request_get_config(
#     'http://127.0.0.1:8000/api/v1/download-config/', msg[:-1])
#     # if msg[0].isdigit() or services.check_valid_ipaddr(msg[0])[0]:
#     #     req = services.RequestToApi()
#     #     res = await req.request_to_api(url_get_dataAPI, msg[0])
#     # else:
#     #     res = 'dsaasdasdsad'
#
#     logger.debug(res)
#     # doc = open('requirements.txt', 'rb')
#     # await message.reply_document('requirements.txt')
#     await message.answer(f'```\n{res}\n```', parse_mode='MarkdownV2')
#     # await message.answer(f'```\n{res}\n```', parse_mode='MarkdownV2')
#     # await bot.send_message('-1002412371192', f'```\n{res}\
#     # n```', parse_mode='MarkdownV2')


# dp.message.register(cmd_test2, F.text)
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
