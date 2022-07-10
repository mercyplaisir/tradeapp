# handles order

import asyncio
import time
from typing import Callable
import pandas as pd

import requests
from binance import BinanceSocketManager, AsyncClient

from common import (TAKE_PROFIT,
 percent_change,
   cout,
   STOP_LOSS)

base_url = "https://api.binance.com"

filename = 'orders.csv'

storage = f'data\{filename}'

class Order:
    """Representation of an order"""
    profit = 0.0 # for profit made all along
    def __init__(self, crypto_name:str) -> None:
        self.cryptopair = crypto_name
        self.order = {} # passed order details
    
    def get_price(self) -> float:
        """get price of a cryptopair"""
        url = "%s/api/v3/ticker/24hr?symbol=%s" % (base_url,self.cryptopair)
        resp = requests.get(url)
        return float(resp.json()["lastPrice"])

    @classmethod
    def profit_change(cls,newvalue):
        cls.profit += newvalue
    
    def buy(self,func:Callable):
        """For buy order 
        params:
        ::func: buy order function,
        ::name: name of the crypto to buy"""
        order_details = func(self.cryptopair)
        self.save(order_details)

    def sell(self,func:Callable):
        """For sell order 
        params:
        ::func: sell order function
        ::name : name of the crypto to sell"""
        order_details = func(self.cryptopair)
        self.save(order_details)
    def clean(self):
        if float(self.order.get('price')) == 0.0:
            self.order['price'] = self.get_price()

    def save(self,**kwargs):
        """save order"""
        self.order = kwargs
        self.clean(self.order)
        if kwargs.get('fills'):
          kwargs['fills'] = [1]
        data = pd.DataFrame(kwargs)

        data.to_csv(storage,mode='a',header=False,index=False) 

        self.track_order()


    def track_order(self):
            """Create a loop tracking the order until the TAKEPROFIT hitted"""
            order_symbol = self.order.get('symbol')
            order_price = self.order.get('price')
            buy_order = True if self.side == "BUY" else False

            cout(f'orderPrice:{order_price}')
            async def main():
                client = await AsyncClient.create()
                socket_manager = BinanceSocketManager(client)
                # start any sockets here, i.e a trade socket
                kline = socket_manager.kline_socket(order_symbol)  # .trade_socket('BNBBTC')
                # then start receiving messages
                async with kline as tscm:
                    while True:
                        response = await tscm.recv()
                        price = float(response["k"]["c"])

                        pourcentage_change = percent_change(float(order_price), price)

                        profit_in_buy = buy_order and pourcentage_change >= TAKE_PROFIT
                        profit_in_sell = not buy_order and -pourcentage_change >= TAKE_PROFIT
                        
                        profit = profit_in_buy or profit_in_sell

                        loss_in_buy = buy_order and -pourcentage_change >=  STOP_LOSS
                        loss_in_sell = not buy_order and pourcentage_change >= STOP_LOSS

                        loss = loss_in_buy or loss_in_sell

                        if profit or loss :
                            cout("tracking ended")
                            self.profit_change(pourcentage_change)
                            break
                        else:
                            cout(
                                f"price:{price} - profit:{round(pourcentage_change,2)} - all time profit : {round(self.profit,2)}"
                                + " - still waiting..."
                            )
                            time.sleep(2.5)
                await client.close_connection()
                # return response

            while True:
                try:
                    loop = asyncio.get_event_loop()

                    loop.run_until_complete(main())
                    break
                except asyncio.exceptions.TimeoutError:
                    pass

    
