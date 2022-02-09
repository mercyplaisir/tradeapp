import btalib
import pandas as pd


class Rsi:
    """
    RSI indicator
    """

    @classmethod
    def create_rsi(cls, periode: int = 14, klines: pd.DataFrame = None):
        """create RSI indicator"""
        rsiInd = btalib.rsi(klines.copy(), period=periode)
        # rsiInd.df.to_csv(f"{KLINEPATH}", index=True, na_rep=0)  # enregistrer dans le fichier
        return rsiInd.df

    @classmethod
    def price_study(cls, klines: pd.DataFrame = None):
        """
            study made on klines(dataframe)

            columns = ["rsi"]
        """

        kline = cls.create_rsi(klines.copy())
        binanceKlines = klines.copy()

        # kline
        rsiList = kline['rsi'][-9:-1]  # recupere les 9 dernieres valeurs

        closePrices = binanceKlines['close'][-9:-1]  # recupere les 9 dernieres valeurs

        rsiMean = rsiList.mean()  # calcule la moyenne
        priceMean = closePrices.mean()

        decision = "buy" if rsiList[-1] > rsiMean and closePrices[-1] > priceMean else "sell"

        return decision
