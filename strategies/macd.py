import pandas as pd



KLINE_PATH = "../files/klines.csv"

class Macd:

    kline = pd.read_csv(KLINE_PATH)

    def __init__(self):
        pass

    @classmethod
    def price_study(cls):
        klines = Macd.kline
        pass
