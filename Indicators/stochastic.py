import sys

import btalib
import numpy as np
from pandas.core.frame import DataFrame
import pandas as pd

sys.path.append("..")
from main.tools import BINANCEKLINES, KLINEPATH


class Stochastic:
    """
    Stochastic indicator
    """

    def __init__(self):
        pass

    def createSTOCHASTIC(self):
        kline = pd.read_csv(BINANCEKLINES, index_col='date')

        stoch = btalib.stochastic(kline)
        stoch.df.to_csv(f"{KLINEPATH}")  # enregistrer dans le fichier

    def price_study(self):
        """
            study made on klines(dataframe)

            columns = ["k","d"]


        """
    
        self.createSTOCHASTIC()

        kline = pd.read_csv(KLINEPATH, index_col='date')
        binanceKlines = pd.read_csv(BINANCEKLINES, index_col='date')

        

    
