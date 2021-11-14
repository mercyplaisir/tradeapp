import random
import time
from datetime import datetime
import asyncio

import pandas as pd
import aiohttp
import requests

from .binanceApi import Binance
from src.model.Indicators.study import Study

class VirtualClient(Binance,Study):

    def __init__(self, publickey: str = None, secretkey: str = None, coin: str = None):
        super().__init__(publickey=publickey, secretkey=secretkey, coin=coin)
    def run(self):

        while True:
            # get crypto related
            cryptopair_related: list = self._get_crypto_pair_related(coin=self.coin)

            # get all klines for each cryptopair
            klines: dict = self._get_many_klines(cryptopair_related)

            #get cryptopair with they study results
            cryptopairs_study_unclean = self._crypto_study(klines)

            #clean the cryptopairs_study dict so we only have
            #possible trades
            cryptopairs_study = self._cleaner(cryptopairs_study_unclean)

            if len(cryptopairs_study) == 0:
                time.sleep(self.timeframe*5)
            else:
                cryptopairs = list(cryptopairs_study.keys())
                #choose a crypto pair
                cryptopair = cryptopairs[random.randint(0, len(cryptopairs)-1)]

                #pass order (the quantity is calculated in passing order)
                self.passOrder(cryptopair)

                #set new coin
                self.coin = cryptopair.replace(self.coin,'')

                time.sleep(self.timeframe*5)