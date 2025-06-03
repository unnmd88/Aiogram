import json
import logging
import asyncio
import os
import ipaddress
from collections import deque
from typing import NamedTuple

import aiohttp
from dotenv import load_dotenv

import my_formatters
from constants import KeysAndFlags
from drivers import drivers_storage


logger = logging.getLogger(__name__)
load_dotenv()

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

    def user_data_for_get_state_is_valid(self, data: list) -> bool:


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

    def user_data_for_get_states_is_valid(self, data: list) -> bool:

        if data[-1] != KeysAndFlags.FLAG_GET_STATES.value and data[-1] not in KeysAndFlags.JSON.value:
            return False
        if data[-1] == KeysAndFlags.FLAG_GET_STATES.value:
            min_len, max_len = 1, 3
        elif data[-1] in KeysAndFlags.JSON.value:
            min_len, max_len = 2, 4
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


class Response:
    def __init__(self):
        self._response = None
        self._errors = deque(maxlen=8)

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'errors={self._errors} '
            f'response={self._response}'
        )

    def load_response(self, data):
        self._response = data

    def load_error(self, error: str | Exception):
        self._errors.append(str(error))

    @property
    def errors(self):
        return self._errors

    @property
    def response(self):
        return self._response


class RequestToApi:

    headers = {
        'User-Agent': os.getenv('user_agent'),
        'Authorization': f'Token {os.getenv("TOKEN_API")}',
        "content-type": "application/json"
    }

    FAPI_BASE_URL = os.getenv('FAPI_BASE_URL')
    FAPI_ROUTE_GET_STATE = os.getenv('FAPI_ROUTE_GET_STATE')
    print(f'FAPI_BASE_URL: {FAPI_BASE_URL}')
    print(f'FAPI_ROUTE_GET_STATE: {FAPI_ROUTE_GET_STATE}')

    def __init__(self):
        self._response = Response()

    def get_controller_states_url(self):
        return self.FAPI_BASE_URL + self.FAPI_ROUTE_GET_STATE

    @property
    def response_result(self) -> Response:
        return self._response

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
              "hosts": [
                "11",
                "2390"
              ]
            }




        logger.debug(data)

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=json.dumps(data)) as s:
                # res = await s.text()
                res = await s.json()
                print(f'res: {res}')
                return res

    # async def get_controller_state(self, chat_id, num_or_ip, ):
    #     url = os.getenv('URL_ManageControllerAPI')
    #     request_entity = ['get_state']
    #     return await self.request_to_api(chat_id, url, num_or_ip, request_entity, type_request='get_state', timeout=5)

    # async def get_config(self, chat_id, num_or_ip, ):
    #     url = os.getenv('URL_GetConfigAPI')
    #     request_entity = ['get_config']
    #     return await self.request_to_api(chat_id, url, num_or_ip, request_entity, type_request='get_config', timeout=60)

    async def send_request(self, url: str, payload: str):
        try:
            async with drivers_storage.aiohttp_client_session.post(url, headers=self.headers, data=payload) as r:
                response = await r.json()
                self._response.load_response(response)
                print(f'response: {response}')
                print(f'self._response: {self._response}')
        except asyncio.TimeoutError:
            self._response.load_error('Ошибка соединения')
        except (AssertionError, aiohttp.client_exceptions.ClientConnectorCertificateError):
            logger.critical('Неверный адрес запроса')
            raise
        # except aiohttp.client_exceptions.ClientConnectionError():
        #     self._response.load_error('Превышено время ожидания запроса данных')


class GetControllerState(RequestToApi):

    async def get_controller_state(self, chat_id, num_or_ip, ):
        url = os.getenv('URL_ManageControllerAPI')
        request_entity = ['get_state']
        return await self.request_to_api(chat_id, url, num_or_ip, request_entity, type_request='get_state', timeout=5)


class GetControllerStateFull(RequestToApi):

    async def get_controller_state(self, chat_id, num_or_ip, ):
        url = os.getenv('URL_ManageControllerAPI')
        request_entity = ['get_states']
        return await self.request_to_api(chat_id, url, num_or_ip, request_entity, type_request='get_states', timeout=6)


class UploadConfig(RequestToApi):

    async def get_config(self, chat_id, num_or_ip, ):
        url = os.getenv('URL_GetConfigAPI')
        request_entity = ['get_config']
        return await self.request_to_api(chat_id, url, num_or_ip, request_entity, type_request='get_config', timeout=60)