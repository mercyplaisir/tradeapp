"""MACD indicator"""
import pandas as pd
import numpy as np
import btalib

from strategies.indicators.base import Indicator
from strategies.indicators.study import COUNT_START,count_for_decision

import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)


class Macd(Indicator):
    """
    MACD indicator
    """

    @classmethod
    def create_indicator(cls, klines: pd.DataFrame) -> pd.DataFrame:
        macd = btalib.macd(klines.copy())

        return macd.df

    @classmethod
    def price_study(cls, klines: pd.DataFrame):
        """
        columns = ["macd","signal","histogram"]
        """
        distance = 0.9

        kline = cls.create_indicator(klines=klines.copy())
        macd = kline["macd"][-COUNT_START:-1]
        signal = kline["signal"][-COUNT_START:-1]
        histogram = kline["histogram"][-COUNT_START:-1]

        histogram_up = histogram > 0
        between_histogram_macd_ok = histogram >= macd + distance
        uptrend = macd >= signal
        between_signal_macd = macd > signal + 0.3

        decision = (
            uptrend * histogram_up * between_histogram_macd_ok * between_signal_macd
        )

        true_count = list(decision).count(True)
        false_count = list(decision).count(False)

        return count_for_decision(true_count=true_count, false_count=false_count)

