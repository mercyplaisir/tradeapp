import sys

from src.model.Indicators.stochastic import Stochastic
from src.model.Indicators.macd import Macd
from src.model.Indicators.sma import Sma
from src.model.Indicators.bb import Bollingerbands
from src.model.Indicators.rsi import Rsi

#sys.path.append("..")
from src.api.binanceApi import Binance


class Study:

    def __init__(self, binanceObj:Binance) -> None:
        self.binance = binanceObj
        # =======================================

    # ==========Decision================
    def Decision(self,cryptopair:str):
        # ==========update klines============
        self.binance.get_klines(cryptopair)
        # =================================

        # ======create indicators==============
        rsiInd = Rsi()
        bbInd = Bollingerbands()
        smaInd = Sma()
        stochInd = Stochastic()
        macdInd = Macd()
        # =====================================

        # ======make price study=================
        rsiStudy = rsiInd.priceStudy()
        bbStudy = bbInd.priceStudy()
        smaStudy = smaInd.priceStudy()
        stochInd = stochInd.price_study()
        macdInd = macdInd.price_study()

        self.studyList = [rsiStudy, bbStudy, smaStudy,stochInd,macdInd]

        

        if self.studyList.count('buy') >= (len(self.studyList)-1):
            return 'buy'
        elif self.studyList.count('sell') >= (len(self.studyList)-2):
            return 'sell'
        else:
            return 'wait'
