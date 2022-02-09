import asyncio
import json
from binance import AsyncClient
import datetime

from src.tools import Tool as tl


# async def main():

#     client = await AsyncClient.create(api_key=BINANCE_PUBLIC_KEY,api_secret=BINANCE_PRIVATE_KEY)
#     exchange_info = await client.get_exchange_info()
#     tickers = await client.get_all_tickers()
#     symbol_info = await client.get_symbol_info('BNBBTC')
#     kline = await client.get_klines(symbol='BNBBTC',interval='1m')
#     await client.close_connection()
#     #print(kline)
#     with open('df.json','w') as f:
#         ll=json.dumps(tickers,indent=True)
#         f.write(ll)
#     with open('kline.json','w') as f:
#         ll=json.dumps(kline,indent=True)
#         f.write(ll)

# if __name__ == "__main__":

#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())

def get_kline():
    async def main():
        client = await AsyncClient.create()
        # exchange_info = await client.get_exchange_info()
        # tickers = await client.get_all_tickers()
        # symbol_info = await client.get_symbol_info('BNBBTC')
        klines = await client.get_klines(symbol='BNBBTC', interval='1d')
        await client.close_connection()
        # print(kline)
        # with open('df.json','w') as f:
        #     ll=json.dumps(tickers,indent=True)
        #     f.write(ll)

        kline = klines[-1]

        # for kline in klines:
        #     #print(kline[0])
        kline[0] = str(datetime.datetime.fromtimestamp(int(kline[0] / 1000)))
        kline[6] = str(datetime.datetime.fromtimestamp(int(kline[6] / 1000)))
        with open('kline.json', 'w') as f:
            ll = json.dumps(klines, indent=True)
            f.write(ll)

        return {'price': float(kline[4]), 'priceChange': tl.percent_change(float(kline[1]), float(kline[4]))}

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(main())


print(get_kline())
