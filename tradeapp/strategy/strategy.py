"""
    Implementation of strategies
"""
from typing import Dict,List

import pandas as pd
import numpy as np

from tradeapp.cryptopair import CryptoPair
from tradeapp.tools import OrderType
from tradeapp.tools import Trend
from tradeapp.tools import Timeframe
from tradeapp.tools import get_trend
from tradeapp.tools import get_support_and_resistance

def follow_trend_strat(cry:CryptoPair) -> OrderType:
    """the strategy is to follow the trend, if up search buy positions if down search sell positions
    """
    daily_data = cry.get_ohlc(timeframe= Timeframe.DAY)
    h4_data = cry.get_ohlc(timeframe= Timeframe.H4)
    m15_data = cry.get_ohlc(timeframe= Timeframe.M15)
    #get trend for daily timeframe
    trend_daily:Trend = get_trend(daily_data)
    #get trend for 4hour
    trend_4hour:Trend = get_trend(h4_data)
    #get trend for 15minutes
    trend_15m:Trend = get_trend(m15_data)

    #if not equal dont lose time
    if not trend_15m == trend_4hour == trend_daily:
        return
    #get support and resistance on 4h timeframe
    sup_res = get_support_and_resistance(df = h4_data)
    


