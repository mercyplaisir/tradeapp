from typing import Protocol


import btalib
import pandas as pd
import numpy as np


indicators = ["Macd", "BollingerBands", "Rsi", "Sma", "Stochastic"]







class Indicator(Protocol):
    """Abstract class of an indicator"""

    @classmethod
    def create_indicator(cls,*args):
        """create the indicator"""
        pass

    @classmethod
    def price_study(cls,*args):
        """study the given price"""
        pass




if __name__ == "__main__":
    pass
