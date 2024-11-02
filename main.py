import json
import os

import asyncio

import logging.config

import aiohttp
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.methods.send_chat_action import SendChatAction
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag
)
import logging_cfg
import services

logging.config.dictConfig(logging_cfg.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

load_dotenv()
dp = Dispatcher()
bot = Bot(token=os.getenv('SDP_BOT'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
url_get_dataAPI = os.getenv("ip_addrAPI")


@dp.message(Command("test1"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


@dp.message(F.text.contains(' ?'))
async def cmd_test2(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    msg = message.text.split()
    if msg[0].isdigit() or services.check_valid_ipaddr(msg[0])[0]:
        req = services.RequestToApi()
        res = await req.request_to_api(url_get_dataAPI, msg[0])
    else:
        res = 'dsaasdasdsad'

    logger.debug(res)
    await message.answer(f'```\n{res}\n```', parse_mode='MarkdownV2')

    # await bot.send_message('-1002412371192', f'```\n{res}\n```', parse_mode='MarkdownV2')


# dp.message.register(cmd_test2, F.text)
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
