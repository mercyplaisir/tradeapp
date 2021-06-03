from os import name, sendfile
from BinanceApi import Binance
import pandas as pd
import json

from tools import Tool


"""
methods in Strategie:
                        - minute15_trend
                        - minute5_trend

methods in bollinger bands:
                            
"""


class Strategie:

    def __init__(self):
        self.client = Binance()
        pass

    


    def minute15_trend(self, coin_to_trade: str, coinPrice: float):
        """
        tendance d'un crypto dans un timeframe de 1heure



        """
    
    
        klines = self.client.get_klines(coin_to_trade, '15m', '1 day')
        

        return klines

    def minute5_trend(self, coin_to_trade: str, coinPrice: float):
        """
        tendance d'un crypto dans un timeframe de 1heure
        """
        klines = self.client.get_klines(coin_to_trade, '5m', '1 day')
        
        return klines



class Bollingerbands(Strategie):

    def __init__(self):
        super().__init__(self)

    

    def price_study(self, klines: pd.DataFrame, advanced: bool):
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

    
    def __init__(self):
        super().__init__(self)
    

    
        

            


class Macd(Strategie):
    
    def __init__(self):
        super().__init__(self)
