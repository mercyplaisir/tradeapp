import sys

import btalib
import pandas as pd
import numpy as np

sys.path.append("..")
from main.tools import BINANCEKLINES, KLINEPATH





class Sma:
    """
    SMA indicator
    """

    def __init__(self):
        pass
        
        
    
    def createSMA(self,periode:int=20):
        kline = pd.read_csv(BINANCEKLINES, index_col='date')
        sma = btalib.sma(kline,period = periode)
        sma.df.columns = [f"sma{periode}"]
        sma.df.to_csv(f"{KLINEPATH}",na_rep=0,index=True)  # enregistrer dans le fichier

       

            
    def priceStudy(self,period:int=20):
        """
        -Parameters
        -------------
        Period : it's a sma period 
        

        >>> columns = ["sma{period}"]
        """

        self.createSMA(periode=period)
        
        kline = pd.read_csv(KLINEPATH,index_col='date')
        binanceKlines = pd.read_csv(BINANCEKLINES)


        smaValues = list(kline[f'sma{period}'])
        smaValues.reverse()
        smaValues = np.array(smaValues[0:9])

        closePrices = list(binanceKlines['close'])
        closePrices.reverse()
        closePrices = np.array(closePrices[0:9])

        mean = list(closePrices > smaValues)
        
        decision= 'buy' if mean.count(True) == closePrices.__len__() else 'sell'

        return decision
        
        
        

    def klines(self):
        kline=pd.read_csv(KLINEPATH,index_col='date')
        return kline
    
