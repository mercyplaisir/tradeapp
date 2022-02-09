import btalib
import numpy as np
import pandas as pd


class Sma:
    """
    SMA indicator
    """

    @classmethod
    def create_sma(cls, periode: int = 20, klines: pd.DataFrame = None):
        sma = btalib.sma(klines.copy(), period=periode)
        sma.df.columns = [f"sma{periode}"]
        # enregistrer dans le fichier
        # sma.df.to_csv(f"{KLINEPATH}", na_rep=0, index=True)
        return sma.df

    @classmethod
    def price_study(cls, period: int = 20, klines: pd.DataFrame = None):
        """
        -Parameters
        -------------
        Period : it's a sma period

        >>> columns = ["sma{period}"]
        
        """

        kline = cls.create_sma(period, klines.copy())
        binanceKlines = klines.copy()

        smaValues = np.array(kline[f'sma{period}'][-9:-1])

        closePrices = np.array(binanceKlines['close'][-9:-1])

        dec = closePrices > smaValues
        dec = list(dec)
        decision = 'buy' if dec.count(True) == len(closePrices) else 'sell'

        return decision
