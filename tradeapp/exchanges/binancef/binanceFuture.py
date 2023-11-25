import time
import numpy as np
import ccxt
import os
from enum import Enum,auto,StrEnum
import requests
# using datetime module
import pandas as pd
from tools.logs import create_logger,logger_wrapper

from tradeapp.exchanges.binancef.models.order import Order_side, Order_type


log  = create_logger(__name__)  



binance_keys = {
        'apiKey': os.getenv('BINANCEPUBLICKEY'),
        'secret' : os.getenv('BINANCEPRIVATEKEY')
    }

@logger_wrapper(__name__,"connecting to exchange")
def binance_future() -> ccxt.Exchange:
    exchange =  ccxt.binanceusdm(binance_keys)
    # exchange = ccxt.binance({
    # 'apiKey': os.getenv('BINANCEPUBLICKEY'),
    # 'secret' : os.getenv('BINANCEPRIVATEKEY'),
    # 'enableRateLimit': True,
    # 'options': {
    #     'defaultType': 'future',
    #     'adjustForTimeDifference': True,  # ←---- resolves the timestamp
    #     },
    # })
    
    
    return  exchange


@logger_wrapper(__name__,"send a buy order")
def buy_order(exchange:ccxt.Exchange,symbol:str,side:Order_type,type:Order_type,amount:int|float,**kwargs):
    """"""
    kwargs['timestamp'] = binance_timestamp()
    exchange.create_order(
        symbol = symbol,
        type = type,
        side = side, 
        amount = amount,
        params = kwargs
                          )

@logger_wrapper(__name__,"send a sell order")
def sell_order(exchange:ccxt.Exchange,symbol:str,side:Order_type,type:Order_type,amount:int|float,**kwargs):
    """"""
    kwargs['timestamp'] = binance_timestamp()
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
        side= Order_side.BUY,
        type=Order_type.MARKET,
        amount=quantity,
        # positionSide = 'LONG',
        **kwargs
    )
def market_sell_order(exchange:ccxt.Exchange,symbol:str,quantity:float,**kwargs):
    buy_order(
        exchange= exchange,
        symbol=symbol,
        side= Order_side.SELL,
        type=Order_type.MARKET,
        amount=quantity,
        # positionSide = 'LONG',
        **kwargs
    )

@logger_wrapper(__name__,"retreiving balance")
def get_bal_of(ex:ccxt.Exchange,crypto:str):
    # timestamp = binance_timestamp() 
    # print(f"{pd.to_datetime(now_timestamp(),unit='ms')}")
    return ex.fetch_balance({
        # 'timestamp' : binance_timestamp(),
         'timestamp' : now_timestamp(),
         'recvWindow' : 5000})['total'][crypto]
def now_timestamp():
    return int(round(time.time() * 1000))
def binance_timestamp():  
    rs = requests.get("https://fapi.binance.com/fapi/v1/time")
    return rs.json()['serverTime']

@logger_wrapper(__name__,"retreiving klines")
def klines_future(pair:str,interval:str):
    rs = requests.get("https://fapi.binance.com/fapi/v1/indexPriceKlines",params={
        "pair": pair,
        "contractType": "PERPERTUAL",
        "interval" : interval
    })
    df = pd.DataFrame(rs.json(),columns=["open time","open","high","low","close","volume","close time","1","2","3","4","5"])
    df = df.get(["open time","open","high","low","close","close time"])
    df[["open","high","low","close"]] = df[["open","high","low","close"]].astype(float)
    # df = df.set_index([pd.Index([i for i in range(df.shape[0])]),'open time'])
    # print(df)
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
    # print(rs.json())
    Open_time,Open,High,Low,Close,Volume,Close_time,_,_,_,_,_ = rs.json()[0]
    return float(Close)


