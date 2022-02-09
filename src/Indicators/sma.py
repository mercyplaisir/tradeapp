import btalib
import pandas as pd
import numpy as np

# sys.path.append("..")
from src.tools import BINANCEKLINES, KLINEPATH


class Sma:
    """
    SMA indicator
    """

    def __init__(self):
        pass

    def createSMA(self, periode: int = 20, klines: pd.DataFrame = None):
        if not klines:
            kline = pd.read_csv(BINANCEKLINES, index_col='date')
        else:
            kline = klines
        sma = btalib.sma(kline, period=periode)
        sma.df.columns = [f"sma{periode}"]
        # enregistrer dans le fichier
        sma.df.to_csv(f"{KLINEPATH}", na_rep=0, index=True)

    def priceStudy(self,period:int = 20, klines: pd.DataFrame = None):
        """
        -Parameters
        -------------
        Period : it's a sma period 
        

        >>> columns = ["sma{period}"]
        
        """

        self.createSMA(period , klines)

        kline = pd.read_csv(KLINEPATH, index_col='date')
        binanceKlines = pd.read_csv(BINANCEKLINES)

        smaValues = np.array(kline[f'sma{period}'][-9:-1])

        closePrices = np.array(binanceKlines['close'][-9:-1])

        dec = closePrices > smaValues
        dec = list(dec)
        decision = 'buy' if dec.count(True) == len(closePrices) else 'sell'

        return decision

    def klines(self):
        kline = pd.read_csv(KLINEPATH, index_col='date')
        return kline
