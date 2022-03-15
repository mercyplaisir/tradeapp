"""Rsi Indicator"""
import pandas as pd
import numpy as np
import btalib

from strategies.indicators.base import Indicator
from strategies.indicators.tools import COUNT_START,count_for_decision
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)


class Rsi(Indicator):
    """
    RSI indicator
    """

    @classmethod
    def create_indicator(cls, klines: pd.DataFrame , periode: int = 14):
        """create RSI indicator"""
        rsiInd = btalib.rsi(klines.copy(), period=periode)
        # rsiInd.df.to_csv(f"{KLINEPATH}", index=True, na_rep=0)  # enregistrer dans le fichier
        return rsiInd.df

    @classmethod
    def price_study(cls, klines: pd.DataFrame):
        """
        study made on klines(dataframe)

        columns = ["rsi"]
        """

        indicator_kline: pd.DataFrame = cls.create_indicator(klines=klines.copy(deep=True))
        exchangeklines = klines.copy(deep=True)
        decision:str = cls._method2( kline=indicator_kline,exchangeklines=exchangeklines)

        return decision

    @classmethod
    def _method1(cls,kline:pd.DataFrame,exchangeklines:pd.DataFrame):

        line_up = 70
        line_down = 30

        # kline
        rsiList = kline["rsi"][-COUNT_START:-1]  # recupere les  dernieres valeurs
        last_rsi_value: float = rsiList[-1]

        closePrices = exchangeklines["close"][
            -COUNT_START:-1
        ]  # recupere les  dernieres valeurs
        last_close_price: float = closePrices[-1]

        rsiMean: float = rsiList.mean()  # calcule la moyenne
        priceMean: float = closePrices.mean()

        not_higher = line_up > rsiList
        not_lower = rsiList > line_down
        between_range = not_higher * not_lower

        buy_condition = last_rsi_value > rsiMean and last_close_price > priceMean
        true_count = list(between_range).count(True)
        false_count = true_count = list(between_range).count(False)

        return count_for_decision(
            true_count=true_count, false_count=false_count, buy_condition=buy_condition
        )

    @classmethod
    def _method2(cls,kline:pd.DataFrame,exchangeklines:pd.DataFrame):
        """simple rsi strategie"""
        line_up = 70
        line_down = 30

        
        rsiList = kline["rsi"][-COUNT_START:-1]  # recupere les  dernieres valeurs
        last_rsi_value: float = rsiList[-1]

        # closePrices = exchangeklines["close"][
        #     -COUNT_START:-1
        # ]  # recupere les  dernieres valeurs
        # last_close_price: float = closePrices[-1]

        buy_decision = last_rsi_value < line_down
        sell_decision = last_rsi_value > line_up

        if buy_decision:
            return 'buy'
        elif sell_decision:
            return 'sell'
        else:
            return 'wait'