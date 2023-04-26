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
