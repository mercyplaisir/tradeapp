from typing import Protocol
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

import btalib
import pandas as pd
import numpy as np


indicators = ["Macd", "BollingerBands", "Rsi", "Sma", "Stochastic"]

start = 5
count_for_buy = start // 2 + 1
count_for_wait = start // 2


def count_for_decision(
    true_count: int, false_count: int, buy_condition: bool = True
) -> str:
    if true_count >= count_for_buy and buy_condition:
        return "buy"
    if true_count == count_for_wait or false_count == count_for_wait:
        return "wait"
    else:
        return "sell"


class Indicator(Protocol):
    """Abstract class of an indicator"""

    @classmethod
    def create_indicator(cls):
        """create the indicator"""
        pass

    @classmethod
    def price_study(cls):
        """study the given price"""
        pass


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
        macd = kline["macd"][-start:-1]
        signal = kline["signal"][-start:-1]
        histogram = kline["histogram"][-start:-1]

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
        """
        between_bot_top = 9 / 100

        kline: pd.DataFrame = cls.create_indicator(period, klines=klines.copy())
        binanceKlines = klines.copy()

        topColumns: pd.Series[float] = kline["top"][-start:-1]

        midColumns: pd.Series[float] = kline["mid"][-start:-1]

        botColumns: pd.Series[float] = kline["bot"][-start:-1]

        closePrices: pd.Series[float] = binanceKlines["close"][-start:-1]
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


class Rsi(Indicator):
    """
    RSI indicator
    """

    @classmethod
    def create_indicator(cls, periode: int = 14, klines: pd.DataFrame = None):
        """create RSI indicator"""
        rsiInd = btalib.rsi(klines.copy(), period=periode)
        # rsiInd.df.to_csv(f"{KLINEPATH}", index=True, na_rep=0)  # enregistrer dans le fichier
        return rsiInd.df

    @classmethod
    def price_study(cls, klines: pd.DataFrame = None):
        """
        study made on klines(dataframe)

        columns = ["rsi"]
        """

        kline: pd.DataFrame = cls.create_indicator(klines=klines.copy(deep=True))
        binanceKlines = klines.copy(deep=True)

        line_up = 70
        line_down = 30

        # kline
        rsiList = kline["rsi"][-start:-1]  # recupere les  dernieres valeurs
        last_rsi_value: float = rsiList[-1]

        closePrices = binanceKlines["close"][
            -start:-1
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


class Sma(Indicator):
    """
    SMA indicator
    """

    @classmethod
    def create_indicator(cls, periode: int = 20, klines: pd.DataFrame = None):
        sma = btalib.sma(klines.copy(), period=periode)
        sma.df.columns = [f"sma{periode}"]
        return sma.df

    @classmethod
    def price_study(cls, klines: pd.DataFrame = None, period: int = 20):
        """
        -Parameters
        -------------
        Period : it's a sma period

        >>> columns = ["sma{period}"]

        """
        distance = 9 / 100  # distance between the close price and the sma. 9%

        binanceKlines = klines.copy(deep=True)
        kline = cls.create_indicator(period, klines=klines.copy())

        smaValues = np.array(kline[f"sma{period}"][-start:-1])

        closePrices = np.array(binanceKlines["close"][-start:-1])

        dec = closePrices > smaValues + (
            closePrices * distance
        )  # 10% of closeprice between close prices and sma
        dec = list(dec)

        true_count = dec.count(True)
        false_count = dec.count(False)

        return count_for_decision(true_count=true_count, false_count=false_count)


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
        arrayD = list(kline["dec"][-start:-1])

        true_count = arrayD.count(True)
        false_count = arrayD.count(False)

        return count_for_decision(true_count=true_count, false_count=false_count)


if __name__ == "__main__":
    pass
