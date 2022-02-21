from operator import truediv
import time
from binance import AsyncClient,BinanceSocketManager
import asyncio
import datetime
from typing import Union
from src.common.tools import Tool as tl



def get_kline():
        """{
              "e": "kline",     // Event type
              "E": 123456789,   // Event time
              "s": "BNBBTC",    // Symbol
              "k": {
                "t": 123400000, // Kline start time
                "T": 123460000, // Kline close time
                "s": "BNBBTC",  // Symbol
                "i": "1m",      // Interval
                "f": 100,       // First trade ID
                "L": 200,       // Last trade ID
                "o": "0.0010",  // Open price
                "c": "0.0020",  // Close price
                "h": "0.0025",  // High price
                "l": "0.0015",  // Low price
                "v": "1000",    // Base asset volume
                "n": 100,       // Number of trades
                "x": false,     // Is this kline closed?
                "q": "1.0000",  // Quote asset volume
                "V": "500",     // Taker buy base asset volume
                "Q": "0.500",   // Taker buy quote asset volume
                "B": "123456"   // Ignore
              }
            }

            """
        lastorderwasbuy = True

        async def main():
            client = await AsyncClient.create()
            bm = BinanceSocketManager(client)
            # start any sockets here, i.e a trade socket
            ts = bm.kline_socket('BNBBTC')  # .trade_socket('BNBBTC')
            # then start receiving messages
            async with ts as tscm:
                while True:
                    response = await tscm.recv()
                    price=float(response['k']['c'])
                    if (lastorderwasbuy and tl.percent_change(0.00995900,price)>=3) or (not lastorderwasbuy and tl.percent_change(0.00995900,price)>=-3):
                        print('profit')
                        break
                    else :
                        print(f'price:{price} - profit:{tl.percent_change(0.00995900,price)} - still waiting...')
                        time.sleep(2.5)
            await client.close_connection()
            # return response
            


        while True:
            try:
                loop = asyncio.get_event_loop()
                # klines_list: dict[str, dict] = loop.run_until_complete(main())
                loop.run_until_complete(main())
                break
            except asyncio.exceptions.TimeoutError:
                pass
        
get_kline()
