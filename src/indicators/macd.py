import btalib
import pandas as pd


class Macd:
    """
    MACD indicator
    """

    @classmethod
    def create_macd(cls, klines: pd.DataFrame) -> pd.DataFrame:
        macd = btalib.macd(klines.copy())

        return macd.df

    @classmethod
    def price_study(cls, klines: pd.DataFrame):
        """
        columns = ["macd","signal","histogram"]
        """
        kline = cls.create_macd(klines.copy())

        kline['decision'] = kline['macd'] > kline['signal']

        listD = list(kline['decision'][-4:-1])

        if listD.count(True) == 3:
            return "buy"
        elif listD.count(True) == 2 or listD.count(False) == 2:
            return "wait"
        else:
            return "sell"
