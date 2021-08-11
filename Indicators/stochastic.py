import sys

import btalib
import numpy as np
import pandas as pd

sys.path.append("..")
from view.tools import BINANCEKLINES, KLINEPATH


class Stochastic:
    """
    Stochastic indicator
    """

    def __init__(self):
        pass

    def createSTOCHASTIC(self):
        kline = pd.read_csv(BINANCEKLINES, index_col='date')

        stoch = btalib.stochastic(kline)
        stoch.df.to_csv(f"{KLINEPATH}", index=True, na_rep=0) # enregistrer dans le fichier

    def price_study(self):
        """
            study made on klines(dataframe)

            columns = ["k","d"]


        """
    
        self.createSTOCHASTIC()

        kline = pd.read_csv(KLINEPATH, index_col='date')
        binanceKlines = pd.read_csv(BINANCEKLINES, index_col='date')

        kline['dec'] = kline['k'] > kline['d']
        arrayD = list(kline['dec'][-4:-1])

        if arrayD.count(True) == 3:
            return "buy" 
        elif arrayD.count(True) == 2 or arrayD.count(False) ==2:
            return  "wait"
        else:
            return "sell"


        

    
