"""Control all indicators"""


import pandas as pd
from strategies.strategies import BbRsi
from strategies.strategies.base import Strategie


# factory.register("rsi", Rsi)
# factory.register("macd", Macd)
# factory.register("bb", Bollingerbands)
# factory.register("sma", Sma)
# factory.register("stochastic", Stochastic)


choosen_strategie = BbRsi()

class Study:
    """Class for Study"""

    # ==========Decision================
    @classmethod
    def decision(cls, klines: pd.DataFrame, strategie:Strategie = choosen_strategie):  # cryptopair: str):
        """For getting a decision from a given strategie"""

        given_strategie_decision:str = strategie.decision(data=klines)
        return given_strategie_decision


        # indicators_names = factory.get_indicators()

        # indicators = [
        #     factory.create({'type' : name}) for name in indicators_names
        # ]  # creating indicators
        # study_list = [
        #     indicator.price_study(klines=klines) for indicator in indicators
        # ]  # studying klines

        # buy_count = study_list.count("buy")
        # sell_count = study_list.count("sell")
        # wait_count = study_list.count("wait")

        # approv_for_buy = (len(indicators) // 2) + 1 # the middle + 2
        # approv_for_sell = (len(indicators) // 2) + 1 # the middle + 1

        # if buy_count >= approv_for_buy:
        #     return ("buy", buy_count)
        # elif sell_count >= approv_for_sell:
        #     return ("sell", sell_count)
        # else:
        #     return ("wait", wait_count)
        
        