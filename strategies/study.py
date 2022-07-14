"""Control all indicators"""
from typing import Callable, Literal

import pandas as pd
from strategies.strat import rsi7

choosen_strategie = rsi7
def study(klines: pd.DataFrame, strategie:Callable = choosen_strategie) -> Literal['buy','sell','wait']:  # cryptopair: str)
    """"""
    given_strategie_decision:str = strategie(data=klines)
    return given_strategie_decision



        