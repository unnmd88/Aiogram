import asyncio
import json
import os

import aiohttp
from aiohttp import FormData
from dotenv import load_dotenv


load_dotenv()

headers = {
    'User-Agent': os.getenv('user_agent'),
    'Authorization': f'Token {os.getenv("TOKEN")}',
     "content-type": "application/json"
}

data = {
    "data": {"11223344": {"host_id": "TEst"}, "num_hosts_in_request": 1, 'search_in_db': True}
}

async def main():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        payload = {
            'login': 'admin',
            'password': 'zBCTRuV7'
        }
        headers = {
            'User-Agent': os.getenv('user_agent'),
        }
        async with session.get("https://10.45.154.12/",
                                headers=headers) as s:

            content = await s.text()
            print(content)
            for line in content.splitlines():
                if 'input id="csrf_token" name="csrf_token" type="hidden" value=' in line:
                    csrf = line.split('<input id="csrf_token" name="csrf_token" type="hidden" value=')[-1].replace('"', '').replace(">", '')

            session.cookie_jar.update_cookies(s.cookies)
            print(csrf)
            data = FormData()
            data.add_field('csrf_token', csrf)
            data.add_field('login', 'admin')
            data.add_field('password', 'zBCTRuV7')

            payload = {
                'csrf_token': csrf,
                'login': 'admin',
                'password': 'zBCTRuV7',
            }

        headers = {
            'User-Agent': os.getenv('user_agent'),
            'content-type': 'application/x-www-form-urlencoded'
        }

        async with session.post("https://10.45.154.12/login",
                                data=data, headers=headers) as s:
            content = await s.text()

            print(content)

        async with session.get("https://10.45.154.12/",
                                headers=headers) as s:

            content = await s.text()
            print(content)





asyncio.run(main())