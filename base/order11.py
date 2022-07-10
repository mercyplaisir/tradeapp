"""Representation of an Order object"""

import asyncio
import datetime
import time
from dataclasses import dataclass,field

# import requests
from binance import BinanceSocketManager, AsyncClient
import sys

# from common.tools import STOP_LOSS, cout
sys.path.append('..')
from common import TAKE_PROFIT, percent_change, HISTORY_ENDPOINT, send_data,cout,STOP_LOSS
from base import CryptoPair

@dataclass
class Order:
    """Representation of an Order passed by binance API

      {
    "symbol": "BTCUSDT",
    "orderId": 28,
    "orderListId": -1,# //Unless OCO, value will be -1
    "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
    "transactTime": 1507725176595,
    "price": "0.30000000",
    "origQty": "10.00000000",
    "executedQty": "10.00000000",
    "cummulativeQuoteQty": "10.00000000",
    "status": "FILLED",
    "timeInForce": "GTC",
    "type": "MARKET",
    "side": "SELL"
      }

    """

    # orderDetails : dict
    symbol: str
    orderId: int
    orderListId: int
    clientOrderId: str
    transactTime: int
    price: str
    origQty: str
    executedQty: str
    cummulativeQuoteQty: str
    status: str
    timeInForce: str
    type: str
    side: str
    fills:list =field(init=True,default=None)

    profit:float = field(init=False,default=0.0)

    def __post_init__(self):
      if float(self.price) == 0.0:
        self.price = CryptoPair(self.symbol).get_price()

    @classmethod
    def profit_change(cls,newvalue):
        cls.profit += newvalue

    # def save(self):
    #     """save by sending order to the assistant server"""
    #     send_data("post", HISTORY_ENDPOINT, **self.dict())
    #     return self

    def dict(self):
        """return dict object of all variable of the class"""
        d=self.__dict__
        if d.get('fills'):
          d.pop('fills')
        return d
    

    def track_order(self):
            """Create a loop tracking the order until the TAKEPROFIT hitted"""
            order_symbol = self.symbol
            order_price = self.price
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



# d={
#   "symbol": "BTCUSDT",
#   "orderId": 28,
#   "orderListId": -1, #//Unless OCO, value will be -1
#   "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
#   "transactTime": 1507725176595,
#   "price": "0.0000000",
#   "origQty": "10.00000000",
#   "executedQty": "10.00000000",
#   "cummulativeQuoteQty": "10.00000000",
#   "status": "FILLED",
#   "timeInForce": "GTC",
#   "type": "MARKET",
#   "side": "SELL",
#   "fills": [
#     {
#       "price": "4000.00000000",
#       "qty": "1.00000000",
#       "commission": "4.00000000",
#       "commissionAsset": "USDT",
#       "tradeId": 56
#     },
#     {
#       "price": "3999.00000000",
#       "qty": "5.00000000",
#       "commission": "19.99500000",
#       "commissionAsset": "USDT",
#       "tradeId": 57
#     },
#     {
#       "price": "3998.00000000",
#       "qty": "2.00000000",
#       "commission": "7.99600000",
#       "commissionAsset": "USDT",
#       "tradeId": 58
#     },
#     {
#       "price": "3997.00000000",
#       "qty": "1.00000000",
#       "commission": "3.99700000",
#       "commissionAsset": "USDT",
#       "tradeId": 59
#     },
#     {
#       "price": "3995.00000000",
#       "qty": "1.00000000",
#       "commission": "3.99500000",
#       "commissionAsset": "USDT",
#       "tradeId": 60
#     }
#   ]
# }


# order1=Order(**d)
# print(order1)