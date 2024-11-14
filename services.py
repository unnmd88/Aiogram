import json
import logging
import asyncio
import os


import aiohttp
import ipaddress

import my_formatters
from constants import KeysAndFlags

logger = logging.getLogger(__name__)




def check_valid_ipaddr(ip_addr: str) -> tuple:
    res = False, 'undefind'
    try:
        ipaddress.ip_address(ip_addr)
        res = (True, None)
    except ValueError as err:
        res = False, err.__str__()
    except Exception as err:
        logger.warning(err)
    finally:
        return res


class Common:

    @staticmethod
    def define_resonse_format(flag):
        return 'json' if flag in {'-j', '-json', 'j', '-j'} else 'text'


class Checker:

    def user_data_for_get_state_isValid(self, data: list) -> bool:


        if data[-1] != KeysAndFlags.FLAG_GET_STATE.value and data[-1] not in KeysAndFlags.JSON.value:
            return False

        if data[-1] == KeysAndFlags.FLAG_GET_STATE.value:
            min_len, max_len = 1, 10
        elif data[-1] in KeysAndFlags.JSON.value:
            min_len, max_len = 2, 11
        else:
            return False

        if not (max_len > len(data) > min_len):
            return False

        return True

    def user_data_for_get_config_isValid(self, data: list) -> bool:


        if data[-1] != KeysAndFlags.FLAG_GET_CONFIG.value and data[-1] not in KeysAndFlags.JSON.value:
            return False

        if data[-1] == KeysAndFlags.FLAG_GET_CONFIG.value:
            min_len, max_len = 1, 10
        elif data[-1] in KeysAndFlags.JSON.value:
            min_len, max_len = 2, 11
        else:
            return False

        if not (max_len > len(data) > min_len):
            return False

        return True






class RequestToApi:

    async def request_to_api(self, chat_id, url, num_or_ip, request_entity, type_request, timeout=60):
        headers = {
            'User-Agent': os.getenv('user_agent'),
            'Authorization': f'Token {os.getenv("TOKEN_API")}',
            "content-type": "application/json"
        }

        hosts = {
            f'{num_ip}': {"host_id": "", 'request_entity': request_entity} for num_ip in num_or_ip
        }

        data = {
            "hosts": hosts, "req_from_telegramm": True, "search_in_db": True, 'chat_id': chat_id,
            'type_request': type_request
        }

        logger.debug(data)

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=json.dumps(data)) as s:
                res = await s.text()
                return res

    # async def get_controller_state(self, chat_id, num_or_ip, ):
    #     url = os.getenv('URL_ManageControllerAPI')
    #     request_entity = ['get_state']
    #     return await self.request_to_api(chat_id, url, num_or_ip, request_entity, type_request='get_state', timeout=5)

    # async def get_config(self, chat_id, num_or_ip, ):
    #     url = os.getenv('URL_GetConfigAPI')
    #     request_entity = ['get_config']
    #     return await self.request_to_api(chat_id, url, num_or_ip, request_entity, type_request='get_config', timeout=60)


class GetControllerState(RequestToApi):

    async def get_controller_state(self, chat_id, num_or_ip, ):
        url = os.getenv('URL_ManageControllerAPI')
        request_entity = ['get_state']
        return await self.request_to_api(chat_id, url, num_or_ip, request_entity, type_request='get_state', timeout=5)

class UploadConfig(RequestToApi):

    async def get_config(self, chat_id, num_or_ip, ):
        url = os.getenv('URL_GetConfigAPI')
        request_entity = ['get_config']
        return await self.request_to_api(chat_id, url, num_or_ip, request_entity, type_request='get_config', timeout=60)