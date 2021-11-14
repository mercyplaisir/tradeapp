import sys

import btalib
import pandas as pd
import numpy as np

# sys.path.append(sys.path[0]+'/..')
from src.controller.tools import BINANCEKLINES, KLINEPATH



class Rsi:
    """
    RSI indicator
    """

    def __init__(self):
        pass

    #@staticmethod
    def createRSI(self,periode: int = 14, klines: pd.DataFrame = None):
        """create RSI indicator"""
        if not klines:
            kline = pd.read_csv(BINANCEKLINES, index_col='date')
        else:
            kline = klines

        rsiInd = btalib.rsi(kline, period=periode)
        rsiInd.df.to_csv(f"{KLINEPATH}", index=True, na_rep=0)  # enregistrer dans le fichier

        return rsiInd.df

    def priceStudy(self, klines: pd.DataFrame = None):
        """
            study made on klines(dataframe)

            columns = ["rsi"]
        """
        self.createRSI(klines)

        kline = pd.read_csv(KLINEPATH, index_col='date')
        binanceKlines = pd.read_csv(BINANCEKLINES, index_col='date')

        # kline
        rsiList = kline['rsi'][-9:-1]  # recupere les 9 dernieres valeurs

        closePrices = binanceKlines['close'][-9:-1]  # recupere les 9 dernieres valeurs

        rsiMean = rsiList.mean()  # calcule la moyenne
        priceMean = closePrices.mean()

        decision = "buy" if rsiList[-1] > rsiMean and closePrices[-1] > priceMean else "sell"

        return decision

    def klines(self):
        kline = pd.read_csv(KLINEPATH, index_col='date')
        return kline
