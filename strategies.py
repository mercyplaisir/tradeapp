
import pandas as pd


"""
methods in Strategie:
                        - minute15_trend
                        - minute5_trend

methods in bollinger bands:
                            
"""

KLINE_PATH = "./files/klines.csv"






class Strategie:

    def __init__(self):
        #self.client = Binance()
        pass


    def klines(self, coin_to_trade="BNBBTC", timeframe="15m", interval="2 days"):
        """
        timeframe:1m,5m,15m,1h,2h,6h,8h,12h,1d,1M,1w,3d
        """
        return self.client.get_klines(coin_to_trade,timeframe,interval)


    def minute15_trend(self):
        """
        tendance d'un crypto dans un timeframe de 15minutes

        """
        klines = pd.read_csv(KLINE_PATH)
        return klines








