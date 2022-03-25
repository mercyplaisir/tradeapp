"""Control all indicators"""
from typing import Literal

import pandas as pd
from strategies.strategies import BbRsi
from strategies.strategies.base import Strategie


choosen_strategie = BbRsi()

class Study:
    """Class for Study"""

    # ==========Decision================
    @classmethod
    def decision(cls, klines: pd.DataFrame, strategie:Strategie = choosen_strategie) -> Literal['buy','sell','wait']:  # cryptopair: str):
        """For getting a decision from a given strategie"""

        given_strategie_decision:str = strategie.decision(data=klines)
        return given_strategie_decision


        