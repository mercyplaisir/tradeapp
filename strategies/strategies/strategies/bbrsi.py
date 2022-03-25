"""bollinger bands and rsi strategies"""
import pandas as pd

from strategies.base import Strategie
from strategies.indicators import Bollingerbands, Rsi


class BbRsi(Strategie):
    """bollinger bands and rsi startegies class"""

    @classmethod
    def decision(cls, data: pd.DataFrame):
        """decision of the strategie"""
        klines = data.copy(deep=True)

        rsi_decision = Rsi.price_study(klines=klines)
        bb_decision = Bollingerbands.price_study(klines=klines)

        if rsi_decision ==  bb_decision:
            return rsi_decision

        return 'wait'
