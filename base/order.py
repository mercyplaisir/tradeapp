"""Representation of an Order object"""

import asyncio
import datetime
import time
from dataclasses import dataclass,field

# import requests
from binance import BinanceSocketManager, AsyncClient
import sys
sys.path.append('..')
from common import TAKE_PROFIT, percent_change, URL, HISTORY_ENDPOINT, send_data,track_order


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
        return self

    def dict(self):
        """return dict object of all variable of the class"""
        self.__dict__.pop('fills')
        return self.__dict__
    

    

d={
  "symbol": "BTCUSDT",
  "orderId": 28,
  "orderListId": -1, #//Unless OCO, value will be -1
  "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
  "transactTime": 1507725176595,
  "price": "60000",
  "origQty": "10.00000000",
  "executedQty": "10.00000000",
  "cummulativeQuoteQty": "10.00000000",
  "status": "FILLED",
  "timeInForce": "GTC",
  "type": "MARKET",
  "side": "SELL",
  "fills": [
    {
      "price": "4000.00000000",
      "qty": "1.00000000",
      "commission": "4.00000000",
      "commissionAsset": "USDT",
      "tradeId": 56
    },
    {
      "price": "3999.00000000",
      "qty": "5.00000000",
      "commission": "19.99500000",
      "commissionAsset": "USDT",
      "tradeId": 57
    },
    {
      "price": "3998.00000000",
      "qty": "2.00000000",
      "commission": "7.99600000",
      "commissionAsset": "USDT",
      "tradeId": 58
    },
    {
      "price": "3997.00000000",
      "qty": "1.00000000",
      "commission": "3.99700000",
      "commissionAsset": "USDT",
      "tradeId": 59
    },
    {
      "price": "3995.00000000",
      "qty": "1.00000000",
      "commission": "3.99500000",
      "commissionAsset": "USDT",
      "tradeId": 60
    }
  ]
}


order1=Order(**d)
track_order(order=order1)
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