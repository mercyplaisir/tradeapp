import asyncio
import json
# import requests
import time

import aiohttp

# from src.api.virtualbinance import VirtualClient
# from src.api.sensitive import BINANCE_PRIVATE_KEY, BINANCE_PUBLIC_KEY
# import datetime

# init client
# client = VirtualClient(publickey=BINANCE_PUBLIC_KEY,
#                         secretkey=BINANCE_PRIVATE_KEY)

# #coin in possession
# client.coin = 'BTC'


# asyncio.run(client.studycryptos())
import requests

cryptos = ['BNBBTC', 'ETHUSDT', 'BTCUSDT', 'DOGEUSDT']*6
data = {
    # "symbol":'BNBBTC',
    "interval": 600,
    "startTime": '1 day ago'
    # "endTime"
    # "limit"
}
main = "https://api.binance.com{}"
klines = "/api/v3/klines"
test = "/api/v3/ping"
# info = requests.get(url=main.format(klines),params= data)

# ff = json.loads(info.text)
# print(ff)
results = []


def get_tasks(session):
    tasks = []
    for crypto in cryptos:
        data["symbol"] = crypto
        tasks.append(asyncio.create_task(session.get(url=main.format(klines), params=data, ssl=False)))
    return tasks


async def get_them():
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            results.append(await response.json())

    with open("hehe.json", 'w') as f:
        json_info = json.dumps(results, indent=True)
        f.write(json_info)



starttime = time.time()

"""
for crypto in cryptos:
    data['symbol']=crypto
    response = requests.get(url=main.format(klines),params=data)

"""
asyncio.run(get_them())

print(time.time() - starttime)
# print(cc)

# print(datetime.datetime.strptime('1 day ago'))
