"""Bollinger Bands indicator"""


import pandas as pd
import numpy as np
import btalib

from strategies.indicators.base import Indicator
from strategies.indicators.study import COUNT_START,count_for_decision

import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)


class Bollingerbands(Indicator):
    """
    Bollinger Bands indicator
    """

    @classmethod
    def create_indicator(cls, periode: int = 30, klines: pd.DataFrame = None):
        bb = btalib.bbands(klines, period=periode, devs=2.0)
        # bb.df.to_csv(f"{KLINEPATH}", index=True, na_rep=0)  # enregistrer dans le fichier
        return bb.df

    @classmethod
    def price_study(cls, klines: pd.DataFrame = None, period: int = 20):
        """
        study made on klines(dataframe)
        columns = ["mid","top","bot"]

        buy if : price goes under the bottom line
        """

        indicator_kline: pd.DataFrame = cls.create_indicator(period, klines=klines.copy(deep=True))
        exchangeklines = klines.copy(deep=True)
        decision:str = cls._method2( klines=indicator_kline,exchangeklines=exchangeklines)

        return decision

    @classmethod
    def _method1(cls, kline: pd.DataFrame,exchangeklines:pd.DataFrame):
        """
        if there is a big gistance between the bottom line and the top line 
        which means there is a higher volatility
        """
        between_bot_top = 9 / 100

        topColumns: pd.Series[float] = kline["top"][-COUNT_START:-1]

        midColumns: pd.Series[float] = kline["mid"][-COUNT_START:-1]

        botColumns: pd.Series[float] = kline["bot"][-COUNT_START:-1]

        closePrices: pd.Series[float] = exchangeklines["close"][-COUNT_START:-1]
        last_price: int = closePrices[-1]

        distance_between_bot_top = topColumns > botColumns + (
            topColumns * between_bot_top
        )

        not_higher = topColumns > closePrices
        not_lower = closePrices > botColumns
        price_inside_bb = not_higher * not_lower

        buy_condition = last_price > closePrices.mean()

        decision = distance_between_bot_top * price_inside_bb
        true_count = list(decision).count(True)
        false_count = list(decision).count(False)

        return count_for_decision(
            true_count=true_count, false_count=false_count, buy_condition=buy_condition
        )
    
    @classmethod
    def _method2(cls, kline: pd.DataFrame,exchangeklines:pd.DataFrame):
        """
        if the price goes under the bottom line it's a buy order 
        elif goes above the top line it's a sell order 
        """

        between_bot_top = 4 / 100

        topColumns: pd.Series[float] = kline["top"][-COUNT_START:-1]
        last_top_value = topColumns[-1]

        midColumns: pd.Series[float] = kline["mid"][-COUNT_START:-1]

        botColumns: pd.Series[float] = kline["bot"][-COUNT_START:-1]
        last_bot_value = botColumns[-1]

        closePrices: pd.Series[float] = exchangeklines["close"][-COUNT_START:-1]
        last_price: int = closePrices[-1]

        distance_between_bot_top = last_top_value > last_bot_value + (
            last_top_value * between_bot_top
        )
        buy_decision:bool = last_price < last_bot_value
        sell_decision:bool = last_price > last_top_value

        if buy_decision and distance_between_bot_top:
            return 'buy'
        elif sell_decision and distance_between_bot_top:
            return 'sell'
        else:
            return 'wait'


        
