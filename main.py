import json
import os

import asyncio
import logging

import aiohttp
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
dp = Dispatcher()
bot = Bot(token=os.getenv('SDP_BOT'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))






@dp.message(Command("test1"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


async def request_to_api():
    data = {
        "data": {"11223344": {"host_id": "TEst"}, "num_hosts_in_request": 1, "search_in_db": True}
    }

    data = json.dumps(data)

    headers = {
        'User-Agent': os.getenv('user_agent'),
        'Authorization': f'Token {os.getenv("TOKEN")}',
        'Сontent-type': 'application/json'
    }

    logger.info(data)
    async with aiohttp.ClientSession() as session:
        async with session.post("http://127.0.0.1:8000/api/v1/get-data-from-controller-ax/",
                                headers=headers, data=data) as s:
            res = await s.text()
            return res



@dp.message(Command("test2"))
async def cmd_test2(message: types.Message):
    data = {
        "data": {"11223344": {"host_id": "TEst"}, "num_hosts_in_request": 1, "search_in_db": True}
    }

    data = json.dumps(data)

    headers = {
        'User-Agent': os.getenv('user_agent'),
        'Authorization': f'Token {os.getenv("TOKEN")}',
        "content-type": "application/json"
    }

    logger.info(data)
    async with aiohttp.ClientSession() as session:
        async with session.post("http://127.0.0.1:8000/api/v1/get-data-from-controller-ax/",
                                headers=headers, data=data) as s:
            res = await s.text()
    await bot.send_message('-1002412371192', f'```\n{res}\n```', parse_mode='MarkdownV2')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
