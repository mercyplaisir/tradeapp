"""Control all indicators"""


import pandas as pd
from strategies.strategies import BbRsi
from strategies.strategies.base import Strategie


# factory.register("rsi", Rsi)
# factory.register("macd", Macd)
# factory.register("bb", Bollingerbands)
# factory.register("sma", Sma)
# factory.register("stochastic", Stochastic)

COUNT_START = 5 # for indicators study

def count_for_decision(
    true_count: int, false_count: int, buy_condition: bool = True
) -> str:

    
    count_for_dec = COUNT_START // 2 + 1
    count_for_wait = COUNT_START // 2
    if true_count >= count_for_dec and buy_condition:
        return "buy"
    elif false_count >= count_for_dec:
        return "sell"
    elif true_count==count_for_wait or false_count==count_for_wait :
        return "wait"
        # return f"truecount:{true_count}, falsecount:{false_count} "

choosen_strategie = BbRsi()

class Study:
    """Class for Study"""

    # ==========Decision================
    @classmethod
    def decision(cls, klines: pd.DataFrame, strategie:Strategie = choosen_strategie):  # cryptopair: str):
        """For getting a decision from a given strategie"""

        given_strategie_decision = strategie.decision(data=klines)
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
        
        