"""function tools
    """






from enum import Enum,auto
from typing import List, Tuple

import pandas as pd
import numpy as np


class OrderType(Enum):
    BUY = auto()
    SELL = auto()
    
    def __str__(self) -> str:
        return f'{self.name.lower}'


class Trend(Enum):
    UPTREND = auto()
    DOWNTREND = auto()
    
    def __str__(self) -> str:
        return f'{self.name}'

class Timeframe(Enum):
    M1 = '1m'
    M5 = '5m'
    M15 = '15m'
    M30 = '30m'
    H1 = '1h'
    H4 = '4h'
    DAY = '1d'
    WEEK = '1w'

    def __repr__(self) -> str:
        return  f'{self.value}'

    def __str__(self) -> str:
        return  f'{self.value}'
    def __eq__(self, __value: object) -> bool:
        return self.value==__value
    def __hash__(self) -> int:
        return hash(self.value)

def get_trend(df:pd.DataFrame) -> Trend:
    """give the trend of the current stock

    Args:
        df (pd.DataFrame): contains ohlc data of given crypto
    """
    # TODO implement the trend
    sma_size = 200
    # Get the trend of the market by using sma200
    # Get list of 5 last closed price
    price : List[float] = df['Close'][-5:].to_list()
    # calculate sma 
    df[f'SMA_{sma_size}'] = df['Close'].rolling(window=sma_size).mean()
    sma_value : List[float] = df[f'SMA_{sma_size}'][-5:].to_list()
    # condition
    cond = price > sma_value
    if cond:
        return Trend.UPTREND
    return Trend.DOWNTREND


def get_support_and_resistance(df:pd.DataFrame) -> List[Tuple[int,str]]:
    """return resistance and support on given data

    Args:
        df (pd.DataFrame): contains ohlc of given crypto
    """
    #method 1: fractal candlestick pattern
  # determine bullish fractal 
    def is_support(df,i):  
        cond1 = df['Low'][i] < df['Low'][i-1]   
        cond2 = df['Low'][i] < df['Low'][i+1]   
        cond3 = df['Low'][i+1] < df['Low'][i+2]   
        cond4 = df['Low'][i-1] < df['Low'][i-2]  
        return (cond1 and cond2 and cond3 and cond4) 
    # determine bearish fractal
    def is_resistance(df,i):  
        cond1 = df['High'][i] > df['High'][i-1]   
        cond2 = df['High'][i] > df['High'][i+1]   
        cond3 = df['High'][i+1] > df['High'][i+2]   
        cond4 = df['High'][i-1] > df['High'][i-2]  
        return (cond1 and cond2 and cond3 and cond4)
    # to make sure the new level area does not exist already
    def is_far_from_level(value, levels, df):    
        ave =  np.mean(df['High'] - df['Low'])    
        return np.sum([abs(value-level)<ave for _,level in levels])==0
    # a list to store resistance and support levels
    levels = []
    high_low = {
    'highs': [],
    'lows' : []
    }
    for i in range(2, df.shape[0] - 2):  
        if is_support(df, i):    
            low = df['Low'][i]  
            
            if is_far_from_level(low, levels, df):      
                levels.append((i, low))  
                high_low['lows'].append(low)
        elif is_resistance(df, i):    
            high = df['High'][i]
            if is_far_from_level(high, levels, df):      
                levels.append((i, high))
                high_low['highs'].append(high) 
    return levels


