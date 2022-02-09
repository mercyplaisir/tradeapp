import json

import pandas as pd

from src.indicators import factory
from src.indicators.bb import Bollingerbands
from src.indicators.macd import Macd
from src.indicators.rsi import Rsi
from src.indicators.sma import Sma
from src.indicators.stochastic import Stochastic


class Study:

    # ==========Decision================
    @classmethod
    def decision(cls, klines: pd.DataFrame):  # cryptopair: str):
        factory.register("rsi", Rsi)
        factory.register("macd", Macd)
        factory.register("bb", Bollingerbands)
        factory.register("sma", Sma)
        factory.register("stochastic", Stochastic)

        """# ======make price study=================
        rsiStudy = Rsi.price_study(klines)
        bbStudy = Bollingerbands.price_study(klines)
        smaStudy = Sma.price_study(klines)
        stochInd = Stochastic.price_study(klines)
        macdInd = Macd.price_study(klines)
        #study_list = [rsiStudy, bbStudy, smaStudy, stochInd, macdInd]
        """
        with open("./indicators.json", 'r') as f:
            data = json.load(f)

        indicators = [factory.create(item) for item in data]  # creating indicators
        study_list = []
        for indicator in indicators:
            study_list.append(indicator.price_study(klines))

        if study_list.count('buy') >= (len(study_list) - 1):
            return 'buy'
        elif study_list.count('sell') >= (len(study_list) - 2):
            return 'sell'
        else:
            return 'wait'
