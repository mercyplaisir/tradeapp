"""Stochastic Indicator"""


import pandas as pd
import numpy as np
import btalib

from strategies.indicators.base import Indicator
from strategies.indicators.study import COUNT_START,count_for_decision

import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)


class Stochastic(Indicator):
    """
    Stochastic indicator
    """

    @classmethod
    def create_indicator(cls, klines: pd.DataFrame = None):

        stoch = btalib.stochastic(klines.copy())
        # stoch.df.to_csv(f"{KLINEPATH}", index=True, na_rep=0)  # enregistrer dans le fichier
        return stoch.df

    @classmethod
    def price_study(cls, klines: pd.DataFrame = None):
        """
        study made on klines(dataframe)

        columns = ["k","d"]


        """
        line_up = 80
        line_down = 20
        between_2_lines = 7  # between the stochastic lines

        kline:pd.DataFrame = cls.create_indicator(klines=klines.copy())
        
        k_not_higher = line_up > kline["k"]
        k_not_lower = kline["k"] > line_down
        k_range = k_not_higher * k_not_lower
        
        d_not_higher = line_up > kline["d"]
        d_not_lower = kline["d"] > line_down
        d_range = d_not_higher * d_not_lower

        # between lineup and line down
        between_line_up_and_down = k_range * d_range
        up_trend = kline["k"] > kline["d"] + between_2_lines  # uptrend

        kline["dec"] = up_trend * between_line_up_and_down
        arrayD = list(kline["dec"][-COUNT_START:-1])

        true_count = arrayD.count(True)
        false_count = arrayD.count(False)

        return count_for_decision(true_count=true_count, false_count=false_count)

