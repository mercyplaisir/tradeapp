import sys

import btalib
import pandas as pd
import numpy as np

from src.controller.tools import BINANCEKLINES, KLINEPATH


class Macd:
    """
    MACD indicator
    """

    def __init__(self):

        pass

    def createMACD(self, klines: pd.DataFrame = None):
        if not klines:
            kline = pd.read_csv(BINANCEKLINES, index_col='date')
        else:
            kline = klines
        macd = btalib.macd(kline)
        macd.df.to_csv(f"{KLINEPATH}", index=True, na_rep=0)  # enregistrer dans le fichier

    def priceStudy(self, klines: pd.DataFrame = None):
        """
        colums = ["macd","signal","histogram"]
        """
        self.createMACD(klines)
        # calculate the MACD

        kline = pd.read_csv(KLINEPATH, index_col='date')
        binanceKlines = pd.read_csv(BINANCEKLINES)

        kline['decision'] = kline['macd'] > kline['signal']

        listD = list(kline['decision'][-4:-1])

        if listD.count(True) == 3:
            return "buy"
        elif listD.count(True) == 2 or listD.count(False) == 2:
            return "wait"
        else:
            return "sell"
