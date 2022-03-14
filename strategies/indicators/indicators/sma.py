"""Simple Moving Average Indicator"""

import pandas as pd
import numpy as np
import btalib

from strategies.indicators.base import Indicator
from strategies.study import COUNT_START,count_for_decision


import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)


class Sma(Indicator):
    """
    SMA indicator
    """

    @classmethod
    def create_indicator(cls, klines: pd.DataFrame, periode: int = 20 ):
        sma = btalib.sma(klines.copy(), period=periode)
        sma.df.columns = [f"sma{periode}"]
        return sma.df

    @classmethod
    def price_study(cls, klines: pd.DataFrame , period: int = 20):
        """
        -Parameters
        -------------
        Period : it's a sma period

        >>> columns = ["sma{period}"]

        """
        distance = 9 / 100  # distance between the close price and the sma. 9%

        binanceKlines = klines.copy(deep=True)
        kline = cls.create_indicator(period, klines=klines.copy())

        smaValues = np.array(kline[f"sma{period}"][-COUNT_START:-1])

        closePrices = np.array(binanceKlines["close"][-COUNT_START:-1])

        dec = closePrices > smaValues + (
            closePrices * distance
        )  # 10% of closeprice between close prices and sma
        dec = list(dec)

        true_count = dec.count(True)
        false_count = dec.count(False)

        return count_for_decision(true_count=true_count, false_count=false_count)
