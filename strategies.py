from BinanceApi import Binance
import pandas as pd
import json

from tools import Tool


"""
functions in this file:
                        - price_study
                        - minute15_trend
                        - minute5_trend
"""


class Strategie:

    def __init__(self):
        self.client = Binance()
        pass

    


    def minute15_trend(self, coin_to_trade: str, coinPrice: float):
        """
        tendance d'un crypto dans un timeframe de 1heure



        """
        up_trend = False
        try:
            klines = self.client.get_klines(coin_to_trade, '15m', '1 day')

            up_trend = self.price_study(coin_to_trade, klines, False, coinPrice)

            if up_trend:
                print('uptrend for 15min')
            else:
                print('no trend for 15min')

        except:
            up_trend = False

        return up_trend

    def minute5_trend(self, coin_to_trade: str, coinPrice: float):
        """
        tendance d'un crypto dans un timeframe de 1heure
        """

        up_trend = False
        try:
            klines = self.client.get_klines(coin_to_trade, '5m', '1day')

            up_trend = self.price_study(coin_to_trade, klines, True, coinPrice)

            if up_trend:
                print('uptrend for 5min')
            else:
                print('no trend for 5min')
        except:
            up_trend = False
        return up_trend
    pass    




class Bollingerbands(Strategie):

    def __init__(self):
        super().__init__()

    def price_study(self, coin_to_trade: str, klines: pd.DataFrame, advanced: bool, coinPrice: float):
        """
            study made on klines(dataframe)
            """
        if not advanced:

            a = []
            for n in range(0, 3):
                if float(klines.loc[n]['close_price']) > float(klines.loc[n]['SMA_20']) and float(klines.loc[n]['open_price']) > float(klines.loc[n]['SMA_20']):
                    y = True
                    a.append(y)
                else:
                    y = False
                    a.append(y)
            j = 0
            for i in a:
                if i == True:
                    j += 1
                else:
                    break
            if j == 4:
                bool_answer = True
            else:
                bool_answer = False
        #-------------------------------------------------------------------------------

        elif advanced:
                  #SMA20                      close price du 1er bougie arriere    openprice du 2eme bougie arriere     openprice du 1er bougie arriere     close price du 2eme bougie arriere
            if float(klines.loc[0]['SMA_20']) > float(klines.loc[1]['close_price']) > float(klines.loc[2]['open_price']) > float(klines.loc[1]['open_price']) >= float(klines.loc[2]['close_price']):
                if float(klines.loc[2]['open_price']) <= Tool.percent_calculator(float(klines.loc[1]['close_price']), -2):
                    bool_answer = True
            else:
                bool_answer = False

        return bool_answer


class Sma(Strategie):
    pass


class Macd(Strategie):
    pass
