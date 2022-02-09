# import sys

import btalib
# import numpy as np
import pandas as pd


# sys.path.append("..")


class Stochastic:
    """
    Stochastic indicator
    """

    @classmethod
    def create_stochastic(cls, klines: pd.DataFrame = None):

        stoch = btalib.stochastic(klines.copy())
        # stoch.df.to_csv(f"{KLINEPATH}", index=True, na_rep=0)  # enregistrer dans le fichier
        return stoch

    @classmethod
    def price_study(cls, klines: pd.DataFrame = None):
        """
            study made on klines(dataframe)

            columns = ["k","d"]


        """

        kline = cls.create_stochastic(klines.copy())

        kline['dec'] = kline['k'] > kline['d']
        arrayD = list(kline['dec'][-4:-1])

        if arrayD.count(True) == 3:
            return "buy"
        elif arrayD.count(True) == 2 or arrayD.count(False) == 2:
            return "wait"
        else:
            return "sell"
