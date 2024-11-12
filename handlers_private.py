import asyncio
import logging
import os

from aiogram import types, F, Router, flags
from aiogram.enums import ChatAction
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionMiddleware
from dotenv import load_dotenv

import my_formatters
import services
from constants import KeysAndFlags

logger = logging.getLogger(__name__)

load_dotenv()

ALLOWED_MEMBERS = {int(chat_id) for chat_id in os.getenv('allowed_members').split()}

private_router = Router()
private_router.message.middleware(ChatActionMiddleware())


# @private_router.message(Command("start"))
# async def start_handler(msg: Message):
#     await msg.answer("Привет! Я помогу тебе узнать твой ID, просто отправь мне любое сообщение")


@private_router.message((F.from_user.id.in_(ALLOWED_MEMBERS)) & (F.text.contains('test')))
@flags.chat_action(ChatAction.TYPING)
async def message_handler(message: Message):
    await asyncio.sleep(4)
    await message.answer(f"Твой ID: {message.from_user.id}")


@private_router.message(
    (F.from_user.id.in_(ALLOWED_MEMBERS)) & (F.text.contains(f' {KeysAndFlags.FLAG_GET_STATE.value}'))
)
@flags.chat_action(ChatAction.TYPING)
async def get_controller_state(message: types.Message):
    checker = services.Checker()
    responce_formatter = my_formatters.BaseFormatter()
    msg = message.text.split()

    if not checker.user_data_for_get_state_isValid(msg):
        return await asyncio.sleep(0.1)

    responce_formatter.responce_format = responce_formatter.define_format_responce(msg)

    chat_id = message.chat.id
    req = services.GetControllerState()

    data_request = msg[:-1] if msg[-1] == KeysAndFlags.FLAG_GET_STATE.value else msg[:-2]
    res = await req.get_controller_state(chat_id, data_request)

    # content, p_mode = my_formatters.current_state_formatter(req.responce_parser(res), KeysAndFlags.TEXT.value)
    # return await message.answer(**content.as_kwargs())

    if responce_formatter.responce_format == services.KeysAndFlags.TEXT:
        content = responce_formatter.text_format_current_state(res)
        await message.answer(**content.as_kwargs())
    elif responce_formatter.responce_format == services.KeysAndFlags.JSON:
        await message.answer(f'```\n{res}\n```', parse_mode='MarkdownV2')



# @private_router.message(F.text.contains(' ?'))
# @flags.chat_action(ChatAction.TYPING)
# async def cmd_test2(message: types.Message):
#     logger.debug(URL_ManageControllerAPI)
#     msg = message.text.split()
#     req = services.RequestToApi()
#     res = await req.request_to_api(URL_ManageControllerAPI, msg[:-1])
#     # if msg[0].isdigit() or services.check_valid_ipaddr(msg[0])[0]:
#     #     req = services.RequestToApi()
#     #     res = await req.request_to_api(url_get_dataAPI, msg[0])
#     # else:
#     #     res = 'dsaasdasdsad'
#
#     logger.debug(res)
#     await message.answer(f'```\n{res}\n```', parse_mode='MarkdownV2')


@private_router.message(F.text.contains('к'))
@flags.chat_action(ChatAction.UPLOAD_DOCUMENT)
async def cmd_test3(message: types.Message):
    # logger.debug(URL_ManageControllerAPI)
    msg = message.text.split()
    # req = services.GetConfig()
    chat_id = message.chat.id
    req = services.RequestToApi()
    res = await req.get_config(chat_id, msg[:-1])

    # if msg[0].isdigit() or services.check_valid_ipaddr(msg[0])[0]:
    #     req = services.RequestToApi()
    #     res = await req.request_to_api(url_get_dataAPI, msg[0])
    # else:
    #     res = 'dsaasdasdsad'

    logger.debug(res)
    # doc = open('requirements.txt', 'rb')
    # await message.reply_document('requirements.txt')
    await message.answer(f'```\n{res}\n```', parse_mode='MarkdownV2')
    # await message.answer(f'```\n{res}\n```', parse_mode='MarkdownV2')
    # await bot.send_message('-1002412371192', f'```\n{res}\
    # n```', parse_mode='MarkdownV2')
