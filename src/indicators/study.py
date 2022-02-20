"""Control all indicators"""
import json

import pandas as pd

from src.indicators import factory
from src.indicators.bb import Bollingerbands
from src.indicators.macd import Macd
from src.indicators.rsi import Rsi
from src.indicators.sma import Sma
from src.indicators.stochastic import Stochastic

factory.register("rsi", Rsi)
factory.register("macd", Macd)
factory.register("bb", Bollingerbands)
factory.register("sma", Sma)
factory.register("stochastic", Stochastic)

class Study:

    # ==========Decision================
    @classmethod
    def decision(cls, klines: pd.DataFrame):  # cryptopair: str):
        

        with open("./indicators.json", 'r') as f:
            data = json.load(f)

        indicators = [factory.create(item) for item in data]  # creating indicators
        study_list = [indicator.price_study(klines) for indicator in indicators]    #studying klines
        
        if study_list.count('buy') >= (len(study_list) - 1):
            return 'buy'
        elif study_list.count('sell') >= (len(study_list) - 2):
            return 'sell'
        else:
            return 'wait'
