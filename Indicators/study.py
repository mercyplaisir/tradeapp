import sys

from Indicators.stochastic import Stochastic
from Indicators.macd import Macd
from Indicators.sma import Sma
from Indicators.bb import Bollingerbands
from Indicators.rsi import Rsi

sys.path.append("..")
from view.BinanceApi import Binance


class Study(Binance):

    def __init__(self, crypto: str) -> None:
        super().__init__()
        self.crypto = crypto
        # =======================================

    # ==========Decision================
    def Decision(self):
        # ==========update klines============
        self.get_klines(coin_to_trade = self.crypto)
        # =================================

        # ======create indicators==============
        rsiInd = Rsi()
        bbInd = Bollingerbands()
        smaInd = Sma()
        stochInd = Stochastic()
        macdInd = Macd()
        # =====================================

        # ======make price study=================
        rsiStudy = rsiInd.priceStudy
        bbStudy = bbInd.priceStudy()
        smaStudy = smaInd.priceStudy()
        stochInd = stochInd.price_study()
        macdInd = macdInd.price_study()

        self.studyList = [rsiStudy, bbStudy, smaStudy,stochInd,macdInd]

        

        if self.studyList.count('buy') == len(self.studyList):
            return 'buy'
        elif self.studyList.count('sell') >= range(3,(len(self.studyList)+1)):
            return 'sell'
        else:
            return 'wait'
