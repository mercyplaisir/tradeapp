import pandas as pd

KLINE_PATH = "../files/klines.csv"


class Bollingerbands:

    kline = pd.read_csv(KLINE_PATH)

    def __init__(self):
        pass

    @classmethod
    def price_study(cls, advanced: bool = True):
        """
            study made on klines(dataframe)
        """
        klines = Bollingerbands.kline
        if not advanced:
            j = 0
            for n in range(4):
                diff = float(klines.loc[n]['close_price']) > float(klines.loc[n]['SMA_20']) and float(
                    klines.loc[n]['open_price']) > float(klines.loc[n]['SMA_20'])
                j += 1 if diff else 0

            bool_answer = True if j == 4 else False
        #-------------------------------------------------------------------------------

        elif advanced:
            #SMA20                      close price du 1er bougie arriere    openprice du 2eme bougie arriere     openprice du 1er bougie arriere     close price du 2eme bougie arriere
            dif1 = float(klines.loc[0]['SMA_20']) > float(klines.loc[1]['close_price']) > float(klines.loc[2]['open_price']) > float(
                klines.loc[1]['open_price']) >= float(klines.loc[2]['close_price'])
            dif2 = float(klines.loc[2]['open_price']) <= Tool.percent_calculator(
                float(klines.loc[1]['close_price']), -2)

            bool_answer = True if dif1 and dif2 else False

        return bool_answer
