import time
import numpy as np
import ccxt
import os
from enum import Enum,auto,StrEnum
import requests
# using datetime module
import pandas as pd
from tools.logs import create_logger,logger_wrapper

from tools.models.order import OrderSide, OrderType
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

# log  = create_logger(__name__)  


binance_keys = {
        'apiKey': os.getenv('BINANCEPUBLICKEY'),
        'secret' : os.getenv('BINANCEPRIVATEKEY')
    }

@logger_wrapper(__name__,"connecting to exchange")
def binance_future() -> ccxt.Exchange:
    exchange =  ccxt.binance(config=binance_keys)

    return  exchange


@logger_wrapper(__name__,"send a buy order")
def buy_order(exchange:ccxt.Exchange,symbol:str,side:OrderSide,type:OrderType,amount:int|float,**kwargs):
    """"""
    # kwargs['timestamp'] = binance_timestamp()
    exchange.create_order(
        symbol = symbol,
        type = type,
        side = side,
        amount = amount,
        params = kwargs
                          )

@logger_wrapper(__name__,"send a sell order")
def sell_order(exchange:ccxt.Exchange,symbol:str,side:OrderSide,type:OrderType,amount:int|float,**kwargs):
    """"""
    # kwargs['timestamp'] = binance_timestamp()
    exchange.create_order(
        symbol = symbol,
        type = type,
        side = side,
        amount = amount,
        params = kwargs
                          )


def market_buy_order(exchange:ccxt.Exchange,symbol:str,quantity:float,**kwargs):
    buy_order(
        exchange= exchange,
        symbol=symbol,
        side= OrderSide.BUY,
        type=OrderType.MARKET,
        amount=quantity,
        # positionSide = 'LONG',
        **kwargs
    )
def market_sell_order(exchange:ccxt.Exchange,symbol:str,quantity:float,**kwargs):
    sell_order(
        exchange= exchange,
        symbol=symbol,
        side= OrderSide.SELL,
        type=OrderType.MARKET,
        amount=quantity,
        # positionSide = 'LONG',
        **kwargs
    )

@logger_wrapper(__name__,"retreiving balance")
def get_bal_of(ex:ccxt.Exchange,crypto:str):
    return ex.fetch_balance()['total'][crypto]
    # return ex.fetch_balance()['total'][crypto]

@logger_wrapper(__name__,"getting current timestamp")
def now_timestamp():
    return int(round(time.time() * 1000))

def binance_timestamp():  
    rs = requests.get("https://fapi.binance.com/fapi/v1/time")
    return rs.json()['serverTime']

@logger_wrapper(__name__,"retreiving klines")
def klines_future(pair:str,interval:str):
    rs = requests.get("https://fapi.binance.com/fapi/v1/klines",params={
        "symbol": pair,
        "interval" : interval,
        "limit":50
    })
    df = pd.DataFrame(rs.json(),columns=["open time","open","high","low","close","volume","close time","1","2","3","4","5"])
    df = df.get(["open time","open","high","low","close","close time"])
    df[["open","high","low","close"]] = df[["open","high","low","close"]].astype(float)
    return df


@logger_wrapper(__name__,"get last price")
def last_price(pair:str):
    rs = requests.get("https://fapi.binance.com/fapi/v1/continuousKlines",
        params={
            'pair':pair,
            'contractType':'PERPETUAL',
            'interval':'1m',
            'limit':1
        })
    print(rs.json())
    Open_time,Open,High,Low,Close,Volume,Close_time,_,_,_,_,_ = rs.json()[0]
    return float(Close)
