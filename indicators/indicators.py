from abc import ABC,abstractmethod
from typing import Protocol

import btalib
import pandas as pd
import numpy as np


__all__ = ['Macd','BollingerBands','Rsi','Sma','Stochastic']

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
        kline = cls.create_indicator(klines=klines.copy())

        kline['decision'] = kline['macd'] > kline['signal']

        listD = list(kline['decision'][-4:-1])

        if listD.count(True) == 3:
            return "buy"
        elif listD.count(True) == 2 or listD.count(False) == 2:
            return "wait"
        else:
            return "sell"



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

        kline = cls.create_indicator(period, klines=klines.copy())
        binanceKlines = klines.copy()

        topColumns = kline['top'][-9:-1]

        midColumns = kline['mid'][-9:-1]

        botColumns = kline['bot'][-9:-1]

        closePrices = binanceKlines['close'][-9:-1]

        if topColumns.mean() > closePrices.mean() > midColumns.mean() > botColumns.mean():
            return 'buy'
        elif topColumns.mean() > midColumns.mean() > botColumns.mean() > closePrices.mean():
            return 'wait'
        else:
            return "sell"


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

        kline = cls.create_indicator(klines=klines.copy(deep=True))
        binanceKlines = klines.copy()

        # kline
        rsiList = kline['rsi'][-9:-1]  # recupere les 9 dernieres valeurs

        closePrices = binanceKlines['close'][-9:-1]  # recupere les 9 dernieres valeurs

        rsiMean = rsiList.mean()  # calcule la moyenne
        priceMean = closePrices.mean()

        decision = "buy" if rsiList[-1] > rsiMean and closePrices[-1] > priceMean else "sell"

        return decision



class Sma(Indicator):
    """
    SMA indicator
    """

    @classmethod
    def create_indicator(cls, periode: int = 20, klines: pd.DataFrame = None):
        sma = btalib.sma(klines.copy(), period=periode)
        sma.df.columns = [f"sma{periode}"]
        # enregistrer dans le fichier
        # sma.df.to_csv(f"{KLINEPATH}", na_rep=0, index=True)
        return sma.df

    @classmethod
    def price_study(cls, klines: pd.DataFrame = None, period: int = 20):
        """
        -Parameters
        -------------
        Period : it's a sma period

        >>> columns = ["sma{period}"]
        
        """

        kline = cls.create_indicator(period, klines=klines.copy())
        binanceKlines = klines.copy()

        smaValues = np.array(kline[f'sma{period}'][-9:-1])

        closePrices = np.array(binanceKlines['close'][-9:-1])

        dec = closePrices > smaValues
        dec = list(dec)
        decision = 'buy' if dec.count(True) == len(closePrices) else 'sell'

        return decision



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

        kline = cls.create_indicator(klines=klines.copy())

        kline['dec'] = kline['k'] > kline['d']
        arrayD = list(kline['dec'][-4:-1])

        if arrayD.count(True) == 3:
            return "buy"
        elif arrayD.count(True) == 2 or arrayD.count(False) == 2:
            return "wait"
        else:
            return "sell"


if __name__ =='__main__':
    pass