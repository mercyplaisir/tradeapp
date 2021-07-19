import btalib
from tools import Tool, FILESTORAGE
import pandas as pd

KLINE_PATH = f'../{FILESTORAGE}/klines.csv'


class Bollingerbands:
    """
    Bollinger Bands indicator
    """


    def __init__(self):
        self.createBB()
        self.setklines()

    def createBB(self,period:int=30):
        klines = pd.read_csv(KLINE_PATH, index_col='date')
        bb = btalib.bbands(klines,period,devs=2.0)
        klines.append(bb.df)
        klines.to_csv(f"{KLINE_PATH}")#enregistrer dans le fichier
        self.setklines()

    @classmethod
    def price_study(cls, advanced: bool = True):
        """
            study made on klines(dataframe)

            columns = ["mid","top","bot"]


        """
        klines = Bollingerbands.kline

        # calculate sma20
        klines['SMA_20'] = klines.iloc[:, 1].rolling(window=20).mean()

        # calculate the Bollinger Bands
        klines['rstd'] = klines.iloc[:, 1].rolling(window=20).std()
        klines['upper_band'] = klines['SMA_20'] + 2 * klines['rstd']
        klines['lower_band'] = klines['SMA_20'] - 2 * klines['rstd']

        if not advanced:
            j = 0
            for n in range(4):
                diff = float(klines.loc[n]['close_price']) > float(klines.loc[n]['SMA_20']) and float(
                    klines.loc[n]['open_price']) > float(klines.loc[n]['SMA_20'])
                j += 1 if diff else 0

            bool_answer = True if j == 4 else False
            return bool_answer
        # -------------------------------------------------------------------------------

        elif advanced:

            dif1 = float(klines.loc[0]['SMA_20']) > float(klines.loc[1]['close_price']) > float(
                klines.loc[2]['open_price']) > float(
                klines.loc[1]['open_price']) >= float(klines.loc[2]['close_price'])
            dif2 = float(klines.loc[2]['open_price']) <= Tool.percent_calculator(
                float(klines.loc[1]['close_price']), -2)

            bool_answer = True if dif1 and dif2 else False

            return bool_answer

    def setklines(self):
        self.kline = pd.read_csv(KLINE_PATH, index_col='date')
