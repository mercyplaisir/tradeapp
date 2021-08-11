from view.tools import BINANCEKLINES, KLINEPATH
import sys

import btalib
import pandas as pd
import numpy as np

sys.path.append("..")


class Sma:
    """
    SMA indicator
    """

    def __init__(self):
        pass

    def createSMA(self, periode: int = 20):
        kline = pd.read_csv(BINANCEKLINES, index_col='date')
        sma = btalib.sma(kline, period=periode)
        sma.df.columns = [f"sma{periode}"]
        # enregistrer dans le fichier
        sma.df.to_csv(f"{KLINEPATH}", na_rep=0, index=True)

    def priceStudy(self, period: int = 20):
        """
        -Parameters
        -------------
        Period : it's a sma period 
        

        >>> columns = ["sma{period}"]
        """

        self.createSMA(periode=period)

        kline = pd.read_csv(KLINEPATH, index_col='date')
        binanceKlines = pd.read_csv(BINANCEKLINES)

        smaValues = kline[f'sma{period}'][-9:-1]

        closePrices = binanceKlines['close'][-9:-1]

        dec = list(closePrices > smaValues)

        decision = 'buy' if dec.count(True) == len(closePrices) else 'sell'

        return decision

    def klines(self):
        kline = pd.read_csv(KLINEPATH, index_col='date')
        return kline
