"""the sma50 and 200"""
import pandas as pd

from strategies.base import Strategie

class Sma50_200(Strategie):
    """representation of sma50 200 strategie"""
    
    @classmethod
    def decision(cls, data: pd.DataFrame):
        """decision of the strategie"""
        klines = data.copy(deep=True)