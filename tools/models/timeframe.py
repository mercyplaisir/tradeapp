""" Timeframe Enum for different timeframes """
from dataclasses import dataclass

@dataclass
class Timeframe:
    """ Timeframe Enum for different timeframes"""
    M1 = '1m'
    M5 = '5m'
    M15 = '15m'
    M30 = '30m'
    H1 = '1h'
    H4 = '4h'
    DAY = '1d'
    WEEK = '1w'


if __name__ == "__main__":
    print(Timeframe.M15)
    print(repr(Timeframe.H1))
    print(str(Timeframe.M5))
    print(Timeframe.DAY == '1d')
    print(hash(Timeframe.WEEK))
