
import pandas as pd

KLINE_PATH = "../files/klines.csv"



class Sma:
    """
    SMA indicator
    """
    kline = pd.read_csv(KLINE_PATH)

    def __init__(self):
        pass

    @classmethod
    def price_study(cls):

        klines = Sma.kline

        #creer un SMA_30
        klines['SMA_30'] = klines.iloc[:, 1].rolling(window=15).mean()

        #creer un SMA50
        klines['SMA_50'] = klines.iloc[:, 1].rolling(window=30).mean()


        j = 0
        for n in range(4):
            diff1 = float(klines.loc[n]['open_price']) > float(
                klines.loc[n]['SMA_30']) > float(klines.loc[n]["SMA_50"])
            diff2 = float(klines.loc[n]['close_price']) > float(
                klines.loc[n]['SMA_30']) > float(klines.loc[n]["SMA_50"])
            j += 1 if diff1 and diff2 else 0

        bool_answer = True if j == 4 else False

        return bool_answer
