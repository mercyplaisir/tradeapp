import pandas as pd
import btalib


KLINE_PATH = "../files/klines.csv"

class Macd:
    """
    MACD indicator
    """

    kline = pd.read_csv(KLINE_PATH)

    def __init__(self):
        pass

    @classmethod
    def price_study(cls):
        klines = Macd.kline
        #calculate the MACD
        macd = btalib.macd(klines)
        pass
