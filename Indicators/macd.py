import sys

import btalib
import pandas as pd
import numpy as np

sys.path.append("..")
from main.tools import BINANCEKLINES, KLINEPATH





class Macd:
    """
    MACD indicator
    """

    

    def __init__(self):
    
        pass

    def createMACD(self, periode: int = 30):
        klines = pd.read_csv(BINANCEKLINES, index_col='date')
        macd = btalib.macd(klines,period=periode)
        s =  klines.append(macd.df)
        s.to_csv(f"{KLINEPATH}")  # enregistrer dans le fichier
        self.setklines()


    def price_study(self):
        """
        colums = ["macd","signal","histogram"]
        """
        self.setklines()
        klines = self.kline
        #calculate the MACD
        
        pass

    def setklines(self):
        self.kline = pd.read_csv(KLINEPATH, index_col='date')
