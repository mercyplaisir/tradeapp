import btalib
from tools import BINANCEKLINES, KLINEPATH, Tool, FILESTORAGE
import pandas as pd



class Bollingerbands:
    """
    Bollinger Bands indicator
    """


    def __init__(self):
        self.createBB()
        self.setklines()

    def createBB(self,period:int=30):
        klines = pd.read_csv(BINANCEKLINES, index_col='date')
        bb = btalib.bbands(klines,period,devs=2.0)
        s = klines.append(bb.df)
        s.to_csv(f"{KLINEPATH}")#enregistrer dans le fichier
        self.setklines()

    
    def price_study(self, advanced: bool = True):
        """
            study made on klines(dataframe)

            columns = ["mid","top","bot"]


        """
        self.setklines()
        klines = self.kline

       
    def setklines(self):
        self.kline = pd.read_csv(KLINEPATH, index_col='date')
