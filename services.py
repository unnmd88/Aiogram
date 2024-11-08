import json
import logging
import asyncio
import os

import aiohttp
import ipaddress

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


class RequestToApi:
    async def request_to_api(self, url, num_or_ip, timeout=5):
        headers = {
            'User-Agent': os.getenv('user_agent'),
            'Authorization': f'Token {os.getenv("TOKEN")}',
            "content-type": "application/json"
        }

        data = {
            "hosts": {f"{num_or_ip}": {"host_id": ""}}, "req_from_telegramm": True, "search_in_db": True,
            'type_request': 'get'
        }

        logger.debug(data)


        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=json.dumps(data)) as s:
                res = await s.text()
                return res

class GetConfig:
    async def request_get_config(self, url, num_or_ip, timeout=20):
        headers = {
            'User-Agent': os.getenv('user_agent'),
            'Authorization': f'Token {os.getenv("TOKEN")}',
            "content-type": "application/json"
        }

        data = {
            "hosts": {f"{num_or_ip}": {"host_id": ""}}, "type_request": "get_config", "search_in_db": True
        }
        timeout = aiohttp.ClientTimeout(timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, headers=headers, data=json.dumps(data)) as s:
                print(s)
                res = await s.read()
                with open('test2', 'w') as f:
                    f.write(res.decode('utf-8'))
                logger.debug(res)
                return

# {'hosts': {'1': {'host_id': ''}, 'req_from_telegramm': True, 'search_in_db': True}}