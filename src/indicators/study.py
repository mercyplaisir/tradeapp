import pandas as pd

from src.indicators.stochastic import Stochastic
from src.indicators.macd import Macd
from src.indicators.sma import Sma
from src.indicators.bb import Bollingerbands
from src.indicators.rsi import Rsi




class Study:

    def __init__(self):  # , binanceObj:Binance) -> None:
        # self.binance = binanceObj
        # =======================================
        self.studyList = None
        pass

    # ==========Decision================
    def Decision(self, klines: pd.DataFrame = None ):#cryptopair: str):
        # ==========update klines============
        #self.binance.get_klines(cryptopair)
        # =================================

        # ======create indicators==============
        rsiInd = Rsi()
        bbInd = Bollingerbands()
        smaInd = Sma()
        stochInd = Stochastic()
        macdInd = Macd()
        # =====================================

        # ======make price study=================
        rsiStudy = rsiInd.priceStudy(klines)
        bbStudy = bbInd.priceStudy(klines)
        smaStudy = smaInd.priceStudy(klines)
        stochInd = stochInd.priceStudy(klines)
        macdInd = macdInd.priceStudy(klines)

        self.studyList = [rsiStudy, bbStudy, smaStudy, stochInd, macdInd]

        if self.studyList.count('buy') >= (len(self.studyList) - 1):
            return 'buy'
        elif self.studyList.count('sell') >= (len(self.studyList) - 2):
            return 'sell'
        else:
            return 'wait'
