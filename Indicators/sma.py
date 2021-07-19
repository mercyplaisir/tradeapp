
import pandas as pd
import btalib

KLINE_PATH = "./files/klines.csv"



class Sma:
    """
    SMA indicator
    """

    def __init__(self):
        self.createSMA()
        self.setklines()
        
    
    def createSMA(self,period:int =20 ):
        klines = pd.read_csv(KLINE_PATH, index_col='date')
        sma = btalib.sma(klines,period)
        sma.klines.columns = [f"sma{period}"]
        klines.append(sma.klines)
        klines.to_csv(f"{KLINE_PATH}")  # enregistrer dans le fichier

        self.setklines()

            
    def price_study(self):
        """
        columns = ["sma{period}"]
        """

        klines = self.kline

        """
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
        """



    def setklines(self):
        self.kline = pd.read_csv(KLINE_PATH, index_col='date')
