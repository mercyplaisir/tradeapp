import sys

# from Indicators.stochastic import Stochastic
# from Indicators.macd import Macd
from Indicators.sma import Sma
from Indicators.bb import Bollingerbands
from Indicators.rsi import Rsi

sys.path.append("..")
from view.BinanceApi import Binance


class Study:

    def __init__(self, crypto: str) -> None:
        pass
        # =======================================

    # ==========Decision================
    def Decision(self):
        # ==========update klines============
        Binance.get_klines(coin_to_trade=crypto)
        # =================================

        # ======create indicators==============
        rsiInd = Rsi()
        bbInd = Bollingerbands()
        smaInd = Sma()
        # stochInd = Stochastic()
        # macdInd = Macd()
        # =====================================

        # ======make price study=================
        rsiStudy = rsiInd.priceStudy
        bbStudy = bbInd.priceStudy()
        smaStudy = smaInd.priceStudy()
        # stochInd = stochInd.price_study()
        # macdInd = macdInd.price_study()

        self.studyList = [rsiStudy, bbStudy, smaStudy]

        listLen: int = self.studyList.__len__()

        if self.studyList.count('buy') == listLen:
            return 'buy'
        elif self.studyList.count('sell') >= (listLen - 1):
            return 'sell'
        else:
            return 'wait'
