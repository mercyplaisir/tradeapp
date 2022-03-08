"""Control all indicators"""


import pandas as pd

from indicators import factory, Rsi, Macd, Bollingerbands, Sma, Stochastic


factory.register("rsi", Rsi)
factory.register("macd", Macd)
factory.register("bb", Bollingerbands)
factory.register("sma", Sma)
factory.register("stochastic", Stochastic)


class Study:
    """Class for Study"""

    # ==========Decision================
    @classmethod
    def decision(cls, klines: pd.DataFrame):  # cryptopair: str):
        """For getting a decision"""

        indicators_names = factory.get_indicators()

        indicators = [
            factory.create({'type' : name}) for name in indicators_names
        ]  # creating indicators
        study_list = [
            indicator.price_study(klines=klines) for indicator in indicators
        ]  # studying klines

        number = (len(indicators) // 2) + 2

        if study_list.count("buy") >= number:
            return ("buy", study_list.count("buy"))
        elif study_list.count("sell") >= number:
            return ("sell", study_list.count("sell"))
        else:
            return ("wait", 0)
