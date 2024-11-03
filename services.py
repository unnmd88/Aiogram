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
            "hosts": {f"{num_or_ip}": {"host_id": ""}}, "req_from_telegramm": True, "search_in_db": True
        }

        logger.debug(data)
        # timeout = aiohttp.ClientTimeout(timeout)

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=json.dumps(data)) as s:
                res = await s.text()
                return res
# {'hosts': {'1': {'host_id': ''}, 'req_from_telegramm': True, 'search_in_db': True}}