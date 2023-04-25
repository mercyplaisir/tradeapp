"""function tools
    """






from enum import Enum,auto

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

    def __str__(self) -> str:
        return f'{self.name}'


def get_trend(data:pd.DataFrame):
    """give the trend of the current stock

    Args:
        data (pd.DataFrame): contains ohlc data of given crypto
    """
def get_support_and_resistance(data:pd.DataFrame):
    """return resistance and support on given data

    Args:
        daa (pd.DataFrame): contains ohlc of given crypto
    """

print(Trend.DOWNTREND)
