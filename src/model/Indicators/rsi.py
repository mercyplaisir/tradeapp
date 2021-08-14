import sys

import btalib
import pandas as pd
import numpy as np

#sys.path.append(sys.path[0]+'/..')
from src.controler.tools import BINANCEKLINES, KLINEPATH


class Rsi:
    """
    RSI indicator
    """

    def __init__(self):
        pass

    def createRSI(self, periode: int = 14):
        kline = pd.read_csv(BINANCEKLINES, index_col='date')
        rsiInd = btalib.rsi(kline, period=periode)
        rsiInd.df.to_csv(f"{KLINEPATH}", index=True, na_rep=0)  # enregistrer dans le fichier

    
    def priceStudy(self):
        """
            study made on klines(dataframe)

            columns = ["rsi"]


        """
        self.createRSI()

        kline = pd.read_csv(KLINEPATH, index_col='date')
        binanceKlines = pd.read_csv(BINANCEKLINES, index_col='date')

        kline
        rsiList = kline['rsi'][-9:-1]  # recupere les 9 dernieres valeurs
        
        closePrices = binanceKlines['close'][-9:-1] # recupere les 9 dernieres valeurs

        rsiMean = rsiList.mean()  # calcule la moyenne
        priceMean = closePrices.mean()

        decision = "buy" if rsiList[-1] > rsiMean and closePrices[-1] > priceMean else "sell"

        return decision

    
    def klines(self):
        kline = pd.read_csv(KLINEPATH, index_col='date')
        return kline
