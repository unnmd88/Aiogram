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

            for line in content.splitlines():
                if 'input id="csrf_token" name="csrf_token" type="hidden" value=' in line:
                    csrf = line.split('<input id="csrf_token" name="csrf_token" type="hidden" value=')[-1].replace('"', '').replace(">", '')

            session.cookie_jar.update_cookies(s.cookies)
            print(csrf)
            data = FormData()
            data.add_field('csrf_token', f'"{csrf}"')
            data.add_field('login', '')
            data.add_field('password', '')

            payload = {
                # 'csrfmiddlewaretoken': f'"{csrf}"',
                # 'X-CSRFToken': f'"{csrf}"',
                'csrf_token': f'"{csrf}"',
                'login': '',
                'password': '',
            }

            params = {'X-CSRFToken': f'"{csrf}"'}

            headers = {
                'User-Agent': os.getenv('user_agent'),
                # 'Content-type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': f'"{csrf}"'
            }
            session.headers.update(headers)
            async with session.post("https://10.45.154.12/login", data=payload) as ss:
                content = await ss.text()
                print(content)
                session.cookie_jar.update_cookies(s.cookies)
            headers = {
                'User-Agent': os.getenv('user_agent'),
                # 'Content-type': 'application/x-www-form-urlencoded',
                # 'csrf_token': f'"{csrf}"'
            }
            session.headers.update(headers)
            async with session.get("https://10.45.154.12/index") as sss:
                print(session.headers)
                content = await sss.text()
                print(content)

asyncio.run(main())