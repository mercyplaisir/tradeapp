import sys

import btalib
import numpy as np
from pandas.core.frame import DataFrame
import pandas as pd

sys.path.append("..")
from main.tools import BINANCEKLINES, KLINEPATH


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

        topColumns = [xx for xx in kline['top']]
        topColumns.reverse()
        topColumns = np.array(topColumns[0:9])

        midColumns = [xx for xx in kline['mid']]
        midColumns.reverse()
        midColumns = np.array(midColumns[0:9])

        botColumns:np.ndarray = [xx for xx in kline['bot']]
        botColumns.reverse()
        botColumns:np.ndarray = np.array(botColumns[0:9])
        
        closePrices = list(binanceKlines['close'])
        closePrices.reverse()
        closePrices = np.array(closePrices[0:9])

        topMean = topColumns.mean()
        midMean = midColumns.mean()
        botMean = botColumns.mean()
        priceMean = closePrices.mean()

        decision = "buy" if topMean>priceMean>midMean else "sell"

        return decision



    def klines(self):
        kline:DataFrame = pd.read_csv(KLINEPATH, index_col='date')
        return kline
