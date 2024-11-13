import ast
import asyncio
import json
import os

import aiohttp
from dotenv import load_dotenv
load_dotenv()




ROUTE_LOGIN_ITC3 = '/api/users/?cmd=login_start&user=admin'
ROUTE_API_ITC3 = '/api/itc/?cmd=panel_get_config'
ROUTE_API_ITC3 = '/api/itc/?cmd=map_get_config'

async def login():
     """
     Метод логиниться в веб сесиию
     :param session: session aiohttp.ClientSession
     :param timeout: таймаут на сессию
     :return: обьект сессии для дальнейших запросов
     """
     headers = {
          'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
     }
     payloadITC3_start = {
          'user': 'admin',
          'pwd': 'changeME1',
          'cmd': 'login_start',

     }
     payloadITC3_finish = {
          # 'login': 'admin',
          'pwd': 'changeME1',

     }

     params = {
          'user': 'admin',

     }

     url_login = f'http://10.179.91.25/'
     url_login2 = f'http://10.179.91.25/api/'
     # url = f'http://{self.ip_adress}{self.ROUTE_LOGIN_ITC3}'
     timeout = aiohttp.ClientTimeout(5)
     async with aiohttp.ClientSession(timeout=timeout) as session:
          async with session.post(url_login2, headers=headers, params=params) as s:
               r = await s.text()
               print(r)
               session.cookie_jar.update_cookies(s.cookies)
          # async with session.post(url_login, headers=headers, data=payloadITC3_finish) as s:
          #      r = await s.text()
          #      print(r)
          #      session.cookie_jar.update_cookies(s.cookies)


res = asyncio.run(login())




# t11 = '''{ "CFG": {"isec_name": "413_interface       ", "isec_id": "                    ", "total_plans": 16, "total_sit": 0}, "success": true , DL:{"detector_logics": [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], "dl_activations": [175,177,170,164,92,94,173,92,0,1,0,227,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}, G:{"group":[[4,4,4,4,4,1,4,4]]}
# , SF:{"software_flags": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}, VD:{"virtual_display":{"display1":["*** ITC-2 Linux  ***","13448 12.11-20:21:57","P3РљР°      S1-S8  115","1-1 Р’РљР›_РћРЁ S6/S6 0  "],"display2":["*** ITC-2 Linux  ***","13448 12.11-20:21:57","P3РљР°      S1-S8  115","1-1 Р’РљР›_РћРЁ S6/S6 0  "],"signals":[1,0,0,0,0,0,1,0]}}
# }'''
# print(ast.literal_eval(t11))
#
#
# t2 ='["*** ITC-2 Linux  ***","13448 12.11-19:09:35","P3РљР°      S1-S8  254","1-1 Р’РљР›_РћРЁ S0/S0 0  "],"display2":["*** ITC-2 Linux  ***","13448 12.11-19:09:35","P3РљР°      S1-S8  254","1-1 Р’РљР›_РћРЁ S0/S0 0  "],"signals":[1,0,0,0,0,0,1,0]'
# t3 = '{"virtual_display":{"display1":["*** ITC-2 Linux  ***","13448 12.11-19:09:35","P3РљР°      ' \
#      'S1-S8  254","1-1 Р’РљР›_РћРЁ S0/S0 0  "],"display2":["*** ITC-2 Linux  ***","13448 12.11-19:09:35","P3РљР°      ' \
#      'S1-S8  254","1-1 Р’РљР›_РћРЁ S0/S0 0  "],"signals":[1,0,0,0,0,0,1,0]}}'
#
# t4 = '{"virtual_display":{"line":["*** ITC-2 Linux  ***","13614 12.11-22:28:32","P1Ка      LOCAL   10","1-1 ВКЛ_ОК S1/S2 16 "],"signals":130}}'
# print(t2.encode(encoding='ansi').decode())
# print(ast.literal_eval(t3))
# t3_3 = ast.literal_eval(t3.encode(encoding='ansi').decode())
# print(t3_3)
# t3_4 = t3_3.get('virtual_display').get('display2')
# t3_4.append(" ".join([str(v) for v in t3_3.get('virtual_display').get('signals')]))
# print(" ".join([str(v) for v in t3_3.get('virtual_display').get('signals')]))
# print(t3_4)
