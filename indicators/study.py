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

        buy_count = study_list.count("buy")
        sell_count = study_list.count("sell")

        # approv_for_buy = (len(indicators) // 2) + 2 # the middle + 2

        # approv_for_sell = (len(indicators) // 2) + 1 # the middle + 1

        # if study_list.count("buy") >= approv_for_buy:
        #     return ("buy", study_list.count("buy"))
        # elif study_list.count("sell") >= approv_for_sell:
        #     return ("sell", study_list.count("sell"))
        # else:
        #     return ("wait", 0)
        
        if buy_count > sell_count:
            return ("buy", buy_count)
        elif sell_count < buy_count:
            return ("sell", sell_count)
        elif buy_count==sell_count:
            return ("wait", sell_count)
            # return ("wait",len(study_list))
        
        # return study_list