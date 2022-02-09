import btalib
import pandas as pd


class Bollingerbands:
    """
    Bollinger Bands indicator
    """

    @classmethod
    def create_bb(cls, periode: int = 30, klines: pd.DataFrame = None):
        bb = btalib.bbands(klines, period=periode, devs=2.0)
        # bb.df.to_csv(f"{KLINEPATH}", index=True, na_rep=0)  # enregistrer dans le fichier
        return bb.df

    @classmethod
    def price_study(cls, period: int = 20, klines: pd.DataFrame = None):
        """
            study made on klines(dataframe)
            columns = ["mid","top","bot"]
        """

        kline = cls.create_bb(period, klines.copy())
        binanceKlines = klines.copy()

        topColumns = kline['top'][-9:-1]

        midColumns = kline['mid'][-9:-1]

        botColumns = kline['bot'][-9:-1]

        closePrices = binanceKlines['close'][-9:-1]

        if topColumns.mean() > closePrices.mean() > midColumns.mean() > botColumns.mean():
            return 'buy'
        elif topColumns.mean() > midColumns.mean() > botColumns.mean() > closePrices.mean():
            return 'wait'
        else:
            return "sell"
