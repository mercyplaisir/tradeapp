# import sys

import btalib
# import numpy as np
import pandas as pd

# sys.path.append("..")
from src.tools import BINANCEKLINES, KLINEPATH


class Stochastic:
    """
    Stochastic indicator
    """

    def __init__(self):
        pass

    def createSTOCHASTIC(self, klines: pd.DataFrame = None):
        if not klines:
            kline = pd.read_csv(BINANCEKLINES, index_col='date')
        else:
            kline = klines

        stoch = btalib.stochastic(kline)
        stoch.df.to_csv(f"{KLINEPATH}", index=True, na_rep=0)  # enregistrer dans le fichier

    def priceStudy(self, klines: pd.DataFrame = None):
        """
            study made on klines(dataframe)

            columns = ["k","d"]


        """

        self.createSTOCHASTIC(klines)

        kline = pd.read_csv(KLINEPATH, index_col='date')
        # binanceKlines = pd.read_csv(BINANCEKLINES, index_col='date')

        kline['dec'] = kline['k'] > kline['d']
        arrayD = list(kline['dec'][-4:-1])

        if arrayD.count(True) == 3:
            return "buy"
        elif arrayD.count(True) == 2 or arrayD.count(False) == 2:
            return "wait"
        else:
            return "sell"