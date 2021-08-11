import sys

import btalib
import numpy as np
from pandas.core.frame import DataFrame
import pandas as pd

sys.path.append("..")
from view.tools import BINANCEKLINES, KLINEPATH


class Bollingerbands:
    """
    Bollinger Bands indicator
    """


    def __init__(self):
        pass
    
    def createBB(self,periode:int=30):
        kline = pd.read_csv(BINANCEKLINES, index_col='date')
        
        bb = btalib.bbands(kline,period = periode,devs=2.0)
        bb.df.to_csv(f"{KLINEPATH}",index=True,na_rep=0)#enregistrer dans le fichier
        
        

    
    def priceStudy(self, period:int=20):
        """
            study made on klines(dataframe)

            columns = ["mid","top","bot"]


        """
        self.createBB(periode=period)

        kline = pd.read_csv(KLINEPATH, index_col='date')
        binanceKlines = pd.read_csv(BINANCEKLINES, index_col='date')

        topColumns = kline['top'][-9:-1]
        
        midColumns = kline['mid'][-9:-1]

        botColumns = kline['bot'][-9:-1]
        
        closePrices = binanceKlines['close'][-9:-1]

        decision = "buy" if topColumns.mean() > closePrices.mean() > midColumns.mean() >botColumns.mean() else "sell"

        return decision



    def klines(self):
        kline:DataFrame = pd.read_csv(KLINEPATH, index_col='date')
        return kline
