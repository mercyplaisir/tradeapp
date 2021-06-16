
import pandas as pd

KLINE_PATH = "../files/klines.csv"



class Sma:

    kline = pd.read_csv(KLINE_PATH)

    def __init__(self):
        pass

    @classmethod
    def price_study(cls):

        klines = Sma.kline

        j = 0
        for n in range(4):
            diff1 = float(klines.loc[n]['open_price']) > float(
                klines.loc[n]['SMA_30']) > float(klines.loc[n]["SMA_50"])
            diff2 = float(klines.loc[n]['close_price']) > float(
                klines.loc[n]['SMA_30']) > float(klines.loc[n]["SMA_50"])
            j += 1 if diff1 and diff2 else 0

        bool_answer = True if j == 4 else False

        return bool_answer
