import sys

import btalib
import pandas as pd
import numpy as np

sys.path.append("..")
from main.tools import BINANCEKLINES, KLINEPATH


class Rsi:
    """
    RSI indicator
    """

    def __init__(self):
        pass

    def createRSI(self,periode:int=14):
        kline = pd.read_csv(BINANCEKLINES,index_col='date')
        rsiInd = btalib.rsi(kline,period = periode)
        rsiInd.df.to_csv(f"{KLINEPATH}",index=True,na_rep=0)  # enregistrer dans le fichier
       

    def priceStudy(self):
        """
            study made on klines(dataframe)

            columns = ["rsi"]


        """
        self.createRSI()
       
        kline = pd.read_csv(KLINEPATH,index_col='date')
        binanceKlines = pd.read_csv(BINANCEKLINES,index_col='date')

        rsiList = [xx for xx in kline['rsi']]#mets les valeurs du dataframe dans la liste
        rsiList.reverse()#renverse la liste pour que les derniers donnes soit les premier
        rsiList = np.array((rsiList[0:9] ))# je garde les 9 premieres et convertisse en array
        
        closePrices = list(binanceKlines['close'])
        closePrices.reverse()
        closePrices = np.array(closePrices[0:9])

        rsiMean = rsiList.mean()#calcule la moyenne
        priceMean = closePrices.mean()

        decision = "buy" if rsiList[0]>(rsiMean+3) and closePrices[0]>priceMean else "sell"
        
        return decision


    def klines(self):
        kline = pd.read_csv(KLINEPATH, index_col='date')
        return kline






    
