"""Representation of an Order object"""

import asyncio
import datetime
import time
from dataclasses import dataclass,field

# import requests
from binance import BinanceSocketManager, AsyncClient
import sys
sys.path.append('..')
from common import TAKE_PROFIT, percent_change, URL, HISTORY_ENDPOINT, send_data


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

    @classmethod
    def profit_change(cls,newvalue):
        cls.profit = newvalue

    def save(self):
        """save by sending order to the assistant server"""
        send_data("post", HISTORY_ENDPOINT, **self.dict())

    def dict(self):
        """return dict object of all variable of the class"""
        self.__dict__.pop('fills')
        return self.__dict__
    

    def track_order(self):
        """Create a loop tracking the order until the TAKEPROFIT hitted"""
        order_symbol = self.symbol
        order_price = self.price
        buy_order = True if self.side == "BUY" else False

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

                    if (buy_order and pourcentage_change >= TAKE_PROFIT) or (
                        not buy_order and pourcentage_change >= -TAKE_PROFIT
                    ):
                        print("profit")
                        self.profit_change(pourcentage_change)
                        # release function
                        break
                    else:
                        print(
                            f"price:{price} - profit:{pourcentage_change}"
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
#   "symbol": "XRPBTC",
#   "orderId": 28,
#   "orderListId": -1,# //Unless OCO, value will be -1
#   "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
#   "transactTime": 1507725176595,
#   "price": "0.250",
#   "origQty": "10.00000000",
#   "executedQty": "10.00000000",
#   "cummulativeQuoteQty": "10.00000000",
#   "status": "FILLED",
#   "timeInForce": "GTC",
#   "type": "MARKET",
#   "side": "SELL",
#   'fills':[2,3]
# }

# order1=Order(**d)
# print(order1.dict())
# # order2 = Order(**d)
# order1.save()
# # Order.change()
# order1.change()

# print(order2.profit)
# print(Order.profit)
# Order.profit = 4
# print(order2.profit)
# print(Order.profit)

# print(Order.profit)