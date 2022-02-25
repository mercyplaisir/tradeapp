"""Control all indicators"""
import json

import pandas as pd

from indicators import factory,Rsi,Macd,Bollingerbands,Sma,Stochastic


factory.register("rsi", Rsi)
factory.register("macd", Macd)
factory.register("bb", Bollingerbands)
factory.register("sma", Sma)
factory.register("stochastic", Stochastic)

class Study:

    # ==========Decision================
    @classmethod
    def decision(cls, klines: pd.DataFrame):  # cryptopair: str):
        

        indicators_names = factory.get_indicators()

        indicators = [factory.create(name) for name in indicators_names]  # creating indicators
        study_list = [indicator.price_study(klines) for indicator in indicators]    #studying klines
        
        number = (len(study_list)//2)+1

        if study_list.count('buy') >= number:
            return 'buy'
        elif study_list.count('sell') >= number:
            return 'sell'
        else:
            return 'wait'
