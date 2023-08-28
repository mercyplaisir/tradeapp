import numpy as np
import ccxt
import os
from enum import Enum,auto,StrEnum
import requests
# using datetime module
import pandas as pd

class Order_side(StrEnum):
    BUY = auto()
    SELL = auto()

    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return  self.name
    
class Order_type(StrEnum):
    LIMIT = auto()
    MARKET = auto()
    STOP = auto()
    TAKE_PROFIT = auto()
    STOP_MARKET = auto()
    TAKE_PROFIT_MARKET = auto()
    TRAILING_STOP_MARKET = auto()

    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return  self.name

binance_keys = {
        'apiKey': os.getenv('BINANCEPUBLICKEY'),
        'secret' : os.getenv('BINANCEPRIVATEKEY')
    }
def binance_future() -> ccxt.Exchange:
    # exchange =  ccxt.binanceusdm(binance_keys)
    exchange = ccxt.binance({
    'apiKey': os.getenv('BINANCEPUBLICKEY'),
    'secret' : os.getenv('BINANCEPRIVATEKEY'),
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',
        },
    })
    
    return  exchange


def buy_order(exchange:ccxt.Exchange,symbol:str,side:Order_type,type:Order_type,amount:int|float,**kwargs):
    """"""
    kwargs['timestamp'] = for_timestamp()
    exchange.create_order(
        symbol = symbol,
        type = type,
        side = side, 
        amount = amount,
        params = kwargs
                          )


def sell_order(exchange:ccxt.Exchange,symbol:str,side:Order_type,type:Order_type,amount:int|float,**kwargs):
    """"""
    kwargs['timestamp'] = for_timestamp()
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

def get_bal_of(ex:ccxt.Exchange,crypto:str):
    return ex.fetch_balance()['total'][crypto]

def for_timestamp():
        
    rs = requests.get("https://fapi.binance.com/fapi/v1/time")
    return rs.json()['serverTime']

def klines_future(pair:str,interval:str):
    rs = requests.get("https://fapi.binance.com/fapi/v1/indexPriceKlines",params={
        "pair": pair,
        "contractType": "PERPERTUAL",
        "interval" : interval
    })
    df = pd.DataFrame(rs.json(),columns=["open time","open","high","low","close","volume","close time","1","2","3","4","5"])
    df = df.get(["open time","open","high","low","close","close time"])
    df[["open","high","low","close"]] = df[["open","high","low","close"]].astype(float)
    return df

def find_support_resistance(data, window_size=10, sensitivity=0.1):
    smoothed_data = []
    for i in range(len(data)):
        start_idx = max(0, i - window_size // 2)
        end_idx = min(len(data), i + window_size // 2 + 1)
        smoothed_value = sum(data[start_idx:end_idx]) / (end_idx - start_idx)
        smoothed_data.append(smoothed_value)
    
    support_levels = []
    resistance_levels = []
    
    for i in range(window_size, len(data) - window_size):
        if data[i] < (1 - sensitivity) * smoothed_data[i]:
            local_minima = True
            for j in range(1, window_size + 1):
                if data[i] > data[i - j] or data[i] > data[i + j]:
                    local_minima = False
                    break
            if local_minima:
                support_levels.append((i, data[i]))
                
        elif data[i] > (1 + sensitivity) * smoothed_data[i]:
            local_maxima = True
            for j in range(1, window_size + 1):
                if data[i] < data[i - j] or data[i] < data[i + j]:
                    local_maxima = False
                    break
            if local_maxima:
                resistance_levels.append((i, data[i]))
                
    return support_levels, resistance_levels

def sup_res(df):
    # Create two functions to calculate if a level is SUPPORT or a RESISTANCE level through fractal identification
    def is_Suppport_Level(df, i):
        support = df['low'][i] < df['low'][i - 1] and df['low'][i] < df['low'][i + 1] and df['low'][i + 1] < df['low'][i + 2] and df['low'][i - 1] < df['low'][i - 2]
        return support


    def is_Resistance_Level(df, i):
        resistance = df['high'][i] > df['high'][i - 1] and df['high'][i] > df['high'][i + 1] and df['high'][i + 1] > df['high'][i + 2] and df['high'][i - 1] > df['high'][i - 2]
        return resistance

    # Creating a list and feeding it the identified support and resistance levels via the Support and Resistance functions
    levels = []
    level_types = []
    for i in range(2, df.shape[0] - 2):

        if is_Suppport_Level(df, i):
            levels.append((i, df['low'][i].round(2)))
            level_types.append('Support')

        elif is_Resistance_Level(df, i):
            levels.append((i, df['high'][i].round(2)))
            level_types.append('Resistance')

        # Clean noise in data by discarding a level if it is near another
        # (i.e. if distance to the next level is less than the average candle size for any given day - this will give a rough estimate on volatility)
    mean = np.mean(df['high'] - df['low'])

    # This function, given a price value, returns True or False depending on if it is too near to some previously discovered key level.
    def distance_from_mean(level):
        return np.sum([abs(level - y) < mean for y in levels]) == 0

    # Optimizing the analysis by adjusting the data and eliminating the noise from volatility that is causing multiple levels to show/overlapp
    levels = []
    level_types = []
    for i in range(2, df.shape[0] - 2):

        if is_Suppport_Level(df, i):
            level = df['low'][i].round(2)

            if distance_from_mean(level):
                levels.append((i, level))
                level_types.append('Support')

        elif is_Resistance_Level(df, i):
            level = df['high'][i].round(2)

            if distance_from_mean(level):
                levels.append((i, level))
                level_types.append('Resistance')
    
    return levels



kline = klines_future(pair='BTCUSDT',interval='4h')
# print(kline.loc[:,'close'])
# rs = find_support_resistance(kline.loc[:,'close'],window_size=400)
print(sup_res(kline))