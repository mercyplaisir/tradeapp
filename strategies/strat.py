
import pandas as pd

from strategies.strategies.base import Strategie
from strategies.indicators import Bollingerbands, Rsi
from strategies.indicators.indic import rsi

def bbrsi( data: pd.DataFrame):
    """bollinger bands and rsi strategy"""
    klines = data.copy(deep=True)

    rsi_decision = Rsi.price_study(klines=klines)
    bb_decision = Bollingerbands.price_study(klines=klines)

    if rsi_decision ==  bb_decision:
        return rsi_decision

    return 'wait'

def sma50_200( data: pd.DataFrame):
    """decision of the strategie"""
    klines = data.copy(deep=True)

def rsi7(data: pd.DataFrame):
    """RSI 7 strategy"""
    response = ['buy','sell','wait']
    rsi_df = rsi(klines=data,periode=7)
    up_limit = 75.0
    down_limit = 25.0
    last_rsi_value = float(rsi_df.iloc[-1]['rsi'])
    if last_rsi_value <= down_limit:
        return 'buy'
    if last_rsi_value >= up_limit:
        return 'sell'
    return 'wait'

    