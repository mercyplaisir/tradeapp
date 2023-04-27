"""
    Implementation of strategies
"""
from typing import Dict,List

import pandas as pd
import numpy as np

from tradeapp.cryptopair import CryptoPair
from tradeapp.tools import Signal
from tradeapp.tools import Trend
from tradeapp.tools import Timeframe

def follow_trend_strat_spot(cry:CryptoPair) -> Signal|None:
    """the strategy is to follow the trend, if up search buy positions if down search sell positions
    """
    dist_price_support = 2.5
    cond1 = (cry.trend == Trend.UPTREND)
    #if not uptrend dont lose time
    if not cond1:
        return None
    #get support and resistance on 4h timeframe
    sup_res = cry.get_support_and_resistance(timeframe= Timeframe.H4)
    resistances,supports = sup_res['resistances'],sup_res['supports']
    def around_the(a:int|float,b:int|float):
        if b>a:
            return (abs(b/a) -1) * 100
        return (abs(a/b) -1) *100
    # closes prices
    data = cry.get_ohlc(timeframe= Timeframe.M15)
    closes_prices = data['Close'][-5:].to_list()
    # if closes prices are around supports in an uptrend then buy
    for close_price in closes_prices:
        for support in supports:
            if around_the(close_price,support) < dist_price_support:
                return Signal.BUY
    return None
    # if high prices are around resistances in an downtrend then sell

def follow_trend_strat_future(cry:CryptoPair) -> Signal:
    """the strategy is to follow the trend, if up search buy positions if down search sell positions
    """
    dist_price_support = 2.5
    #get support and resistance on 4h timeframe
    sup_res = cry.get_support_and_resistance(timeframe= Timeframe.H4)
    resistances,supports = sup_res['resistances'],sup_res['supports']
    def around_the(a:int|float,b:int|float):
        if b>a:
            return (abs(b/a) -1) * 100
        return (abs(a/b) -1) *100
    # closes prices
    data = cry.get_ohlc(timeframe= Timeframe.M15)
    low_prices = data['Low'][-5:].to_list()
    high_prices = data['High'][-5:].to_list()
    # if closes prices are around supports in an uptrend then buy
    if cry.trend == Trend.UPTREND:
        for low_price in low_prices:
            for support in supports:
                if around_the(low_price,support) < dist_price_support:
                    return Signal.BUY
    # if high prices are around resistances in an downtrend then sell
    if cry.trend == Trend.DOWNTREND:
        for high_price in high_prices:
            for resistance in resistances:
                if around_the(high_price,resistance) <dist_price_support:
                    return Signal.SELL
    return None
