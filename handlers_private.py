import asyncio
import logging
import os

from aiogram import types, F, Router, flags
from aiogram.enums import ChatAction
from aiogram.filters import Command, CommandStart, and_f
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionMiddleware
from dotenv import load_dotenv

import my_formatters
import services
from constants import KeysAndFlags
from text_messages import available_options, start_command_text, get_text
from keyboards.main_keyboard import main_menu, text_on_buttons_main


logger = logging.getLogger(__name__)

load_dotenv()

ALLOWED_MEMBERS = {int(chat_id) for chat_id in os.getenv('allowed_members').split()}

private_router = Router()
private_router.message.middleware(ChatActionMiddleware())


@private_router.message(and_f(CommandStart(), F.from_user.id.in_(ALLOWED_MEMBERS)))
async def start_handler(msg: Message):
    await msg.answer(get_text(msg.text), reply_markup=main_menu.as_markup(resize_keyboard=True))


@private_router.message((F.from_user.id.in_(ALLOWED_MEMBERS)) & (F.text.lower().in_(text_on_buttons_main)))
async def message_handler(msg: Message):
    message = get_text(msg.text)
    if isinstance(message, str):
        return await msg.answer(message)
    return await msg.answer(**message.as_kwargs())


@private_router.message(
    (F.from_user.id.in_(ALLOWED_MEMBERS)) & (F.text.contains(f' {KeysAndFlags.FLAG_GET_STATES.value}')) &
    (F.text.func(lambda cnt: cnt.count('?') == 2))
)
@flags.chat_action(ChatAction.TYPING)
async def get_controller_states(message: types.Message):
    print('----------get_controller_states--------------')
    checker = services.Checker()
    responce_formatter = my_formatters.BaseFormatter()
    msg = message.text.split()

    if not checker.user_data_for_get_states_is_valid(msg):
        return await asyncio.sleep(0.1)

    responce_formatter.responce_format = responce_formatter.define_format_responce(msg)

    chat_id = message.chat.id
    req = services.GetControllerStateFull()

    data_request = msg[:-1] if msg[-1] == KeysAndFlags.FLAG_GET_STATES.value else msg[:-2]
    res = await req.get_controller_state(chat_id, data_request)
    logger.debug(res)

    # content, p_mode = my_formatters.current_state_formatter(req.responce_parser(res), KeysAndFlags.TEXT.value)
    # return await message.answer(**content.as_kwargs())

    if responce_formatter.responce_format == services.KeysAndFlags.TEXT:
        content = responce_formatter.text_format_current_state(res, data_request)
        logger.debug(content)
        await message.answer(**content.as_kwargs())
    elif responce_formatter.responce_format == services.KeysAndFlags.JSON:
        await message.answer(f'```\n{res}\n```', parse_mode='MarkdownV2')


@private_router.message(
    (F.from_user.id.in_(ALLOWED_MEMBERS)) & (F.text.contains(f' {KeysAndFlags.FLAG_GET_STATE.value}'))
)
@flags.chat_action(ChatAction.TYPING)
async def get_controller_state(message: types.Message):
    checker = services.Checker()
    responce_formatter = my_formatters.BaseFormatter()
    msg = message.text.split()

    if not checker.user_data_for_get_state_is_valid(msg):
        return await asyncio.sleep(0.1)

    responce_formatter.responce_format = responce_formatter.define_format_responce(msg)

    chat_id = message.chat.id
    req = services.GetControllerState()

    data_request = msg[:-1] if msg[-1] == KeysAndFlags.FLAG_GET_STATE.value else msg[:-2]
    res = await req.get_controller_state(chat_id, data_request)
    logger.debug(res)

    # content, p_mode = my_formatters.current_state_formatter(req.responce_parser(res), KeysAndFlags.TEXT.value)
    # return await message.answer(**content.as_kwargs())

    if responce_formatter.responce_format == services.KeysAndFlags.TEXT:
        content = responce_formatter.text_format_current_state(res, data_request)
        logger.debug(content)
        await message.answer(**content.as_kwargs())
    elif responce_formatter.responce_format == services.KeysAndFlags.JSON:
        await message.answer(f'```\n{res}\n```', parse_mode='MarkdownV2')


@private_router.message(
    (F.from_user.id.in_(ALLOWED_MEMBERS)) & (F.text.lower().contains(f' {KeysAndFlags.FLAG_GET_CONFIG.value}'))
)
@flags.chat_action(ChatAction.UPLOAD_DOCUMENT)
async def get_config(message: types.Message):
    checker = services.Checker()
    responce_formatter = my_formatters.BaseFormatter()
    msg = message.text.split()

    if not checker.user_data_for_get_config_isValid(msg):
        return await asyncio.sleep(0.1)

    responce_formatter.responce_format = responce_formatter.define_format_responce(msg)

    chat_id = message.chat.id
    req = services.UploadConfig()

    data_request = msg[:-1] if msg[-1] == KeysAndFlags.FLAG_GET_CONFIG.value else msg[:-2]
    res = await req.get_config(chat_id, data_request)
    logger.debug(res)

    if responce_formatter.responce_format == services.KeysAndFlags.TEXT:
        content = responce_formatter.text_format_upload_config(res, data_request)
        logger.debug(content)
        await message.answer(**content.as_kwargs())
    elif responce_formatter.responce_format == services.KeysAndFlags.JSON:
        await message.answer(f'```\n{res}\n```', parse_mode='MarkdownV2')
