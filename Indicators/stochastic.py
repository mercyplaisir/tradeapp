import btalib
from tools import BINANCEKLINES, KLINEPATH, Tool, FILESTORAGE
import pandas as pd



class Stochastic:
    """
    Stochastic indicator
    """

    def __init__(self):
        pass

    def createSTOCHASTIC(self):
        klines = pd.read_csv(BINANCEKLINES, index_col='date')
        stoch = btalib.stochastic(klines)
        s = klines.append(stoch.df)
        s.to_csv(f"{KLINEPATH}")  # enregistrer dans le fichier
        self.setklines()

    def price_study(self):
        """
            study made on klines(dataframe)

            columns = ["k","d"]


        """
        self.setklines()
        klines = self.kline

    def setklines(self):
        self.kline = pd.read_csv(KLINEPATH, index_col='date')
