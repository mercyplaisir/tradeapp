from http.client import GATEWAY_TIMEOUT
import time
import os
from typing import List, Dict, Protocol, override
from urllib import response

import numpy as np
import ccxt
from enum import Enum,auto,StrEnum
import requests
# using datetime module
import pandas as pd
from tools.logs import create_logger,logger_wrapper

from tools.models import order
from tools.models.order import OrderSide, OrderType
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

from .exchange import Exchange
from dataclasses import dataclass


@dataclass
class Order:
    """ Order dataclass """
    symbol: str
    side: OrderSide
    type: OrderType
    amount: float
    params: dict

class TimeframeProtocol(Protocol):
    """ Timeframe Protocol"""

# log  = create_logger(__name__)
class BinanceFuture(Exchange):
    """Binance Future, binance future wrapper

    """
    def __init__(self,apikey,secretkey)->None:
        self.exchange = ccxt.binance({
            'apiKey': apikey,
            'secret': secretkey,
            'options': {
                'defaultType': 'future',
            },
        })

    #@logger_wrapper(__name__,"send a buy order")
    def buy_order(self,order:Order):
        """send a buy order"""
        return self.exchange.create_order(
        symbol = order.symbol,
        type = order.type,
        side = order.side,
        amount = order.amount,
        params = order.params
                          )
        
    #@logger_wrapper(__name__,"send a sell order")
    def sell_order(self,order:Order):
        """send a sell order"""
        return self.exchange.create_order(
        symbol = order.symbol,
        type = order.type,
        side = order.side,
        amount = order.amount,
        params = order.params
                          )
    def fetch_cryptopairs(self):
        """fetch all available crypto pairs"""
        pass

    #@logger_wrapper(__name__,"retreiving klines")
    def klines(self,pair:str,interval:str,*args, **kwargs) -> pd.DataFrame:
        """query klines/candles data"""
        rs:requests.Response = requests.get("https://fapi.binance.com/fapi/v1/klines",timeout=30,params={
            "symbol": pair,
            "interval" : interval,
            "limit":50
        })
        df_bulkdata:pd.DataFrame = pd.DataFrame(rs.json(),columns=["open time","open","high","low","close","volume","close time","1","2","3","4","5"])
        df:pd.DataFrame|None  = df_bulkdata.get(["open time","open","high","low","close","close time"])
        if df is None:
            assert False, "no data retrieved"
        df[["open","high","low","close"]] = df[["open","high","low","close"]].astype(float)
        return df    
    
    #@logger_wrapper(__name__,"get last price")
    @classmethod
    def last_price(cls,pair:str)    -> float:   
        """fetch last price of a given pair"""
        rs = requests.get("https://fapi.binance.com/fapi/v1/continuousKlines",
                        timeout=30,
                        params={
                            'pair':pair,
                            'contractType':'PERPETUAL',
                            'interval':'1m',
                            'limit':1
                        })
        # print(rs.json())
        Open_time,Open,High,Low,close,Volume,Close_time,_,_,_,_,_ = rs.json()[0]
        return float(close)
    
    def get_balance(self,pair:str):
        """fetch balance of a given crypto"""
        return self.exchange.fetch_balance()['total'][pair]

    def place_order(self,order_details:dict):
        """place an order"""
        pass
    def cancel_order(self,order_id:str):
        """cancel an order"""
        pass
    def order_status(self,order_id:str):
        """fetch order status"""
        pass
    def fetch_open_orders(self):
        """fetch all open orders"""
        pass
    def limit_order(self):
        """send a limit order"""
        pass
    def limit_buy_order(self):
        """send a limit buy order"""
        pass
    def limit_sell_order(self):
        """send a limit sell order"""
        pass   
    def binance_timestamp(self):  
        rs = requests.get("https://fapi.binance.com/fapi/v1/time")
        return rs.json()['serverTime']

    def market_buy_order(self,symbol:str,quantity:float,**kwargs):
        order = Order(symbol=symbol,side=OrderSide.BUY,type=OrderType.MARKET,amount=quantity,params=kwargs)
        self.buy_order(order=order)
    
    def market_sell_order(self,symbol:str,quantity:float,**kwargs):
        order = Order(symbol=symbol,
                      side=OrderSide.SELL,
                      type=OrderType.MARKET,
                      amount=quantity,
                      params=kwargs)
        return self.sell_order(order=order)


# binance_keys = {
#         'apiKey': os.getenv('BINANCEPUBLICKEY'),
#         'secret' : os.getenv('BINANCEPRIVATEKEY')
#     }

#@logger_wrapper(__name__,"connecting to exchange")
def binance_future() -> ccxt.Exchange:
    """connect to binance future exchange

        Returns:
            ccxt.Exchange: ccxt binance future exchange instance
        """
    exchange =  ccxt.binance(config=binance_keys)

    return  exchange
