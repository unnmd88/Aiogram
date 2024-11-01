import asyncio
import json
import os

import aiohttp
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
    async with aiohttp.ClientSession() as session:
        async with session.post("http://127.0.0.1:8000/api/v1/get-data-from-controller-ax/",
                                data=json.dumps(data), headers=headers) as s:
            content = await s.text()
            print(content)

asyncio.run(main())