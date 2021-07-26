import btalib
from tools import BINANCEKLINES, KLINEPATH, Tool, FILESTORAGE
import pandas as pd



class Rsi:
    """
    RSI indicator
    """

    def __init__(self):
        self.createRSI()
        self.setklines()

    def createRSI(self, period: int = 14):
        klines = pd.read_csv(BINANCEKLINES)
        stoch = btalib.rsi(klines, period)
        s = klines.append(stoch.df)
        s.to_csv(f"{KLINEPATH}")  # enregistrer dans le fichier
        self.setklines()

    def price_study(self,coinPrice:int=None):
        """
            study made on klines(dataframe)

            columns = ["rsi"]


        """
        self.setklines()
        klines = self.kline






    def setklines(self):
        self.kline = pd.read_csv(KLINEPATH)
