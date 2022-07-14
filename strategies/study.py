"""Control all indicators"""
from typing import Callable, Literal

import pandas as pd
# from strategies.strategies import BbRsi
# from strategies.strategies.base import Strategie

from strategies.strat import rsi7

choosen_strategie = rsi7
def study(klines: pd.DataFrame, strategie:Callable = choosen_strategie) -> Literal['buy','sell','wait']:  # cryptopair: str)
    """"""
    given_strategie_decision:str = strategie(data=klines)
    return given_strategie_decision


"""class Study:
    \"""Class for Study\"""

    # ==========Decision================
    @classmethod
    def decision(cls, klines: pd.DataFrame, strategie:Callable = choosen_strategie) -> Literal['buy','sell','wait']:  # cryptopair: str):
        \"""For getting a decision from a given strategie\"""

        given_strategie_decision:str = strategie(data=klines)
        return given_strategie_decision
"""

        