from typing import Union
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


    def passOrder(self, cryptopair: str):
        cryptopair = cryptopair
        basecoin_or_quotecoin = self._basecoin_or_quotecoin(cryptopair=cryptopair, coin=self.coin)
        price = self._get_price(cryptopair=cryptopair)
        coin_for_order = self._getBasecoin_cryptopair(cryptopair)
        quantity = self.orderQuantity(coin_for_order)

        if basecoin_or_quotecoin == 'quotecoin':
            # BNBBTC from btc to bnb you buy
            self._buyOrder(
                quantity=quantity,
                coin_for_order=coin_for_order,
                action='buy',
                price=price
            )
        elif basecoin_or_quotecoin == 'basecoin':

            # BNBBTC from bnb to btc you sell
            self._sellOrder(
                quantity=quantity,
                coin_for_order=coin_for_order,
                action='sell',
                price=price
            )

    def _buyOrder(self, **kwargs):
        """Virtual buy"""
        # modify 'virtualbalance' table
        # create new balance for the new crypto
        self.database.requestDB(
            f"UPDATE virtualbalance SET Balance = {kwargs['quantity']} where shortname = {kwargs['coin_for_order']} ")
        # delete balance on crypto i use to hold
        self.database.requestDB(f"UPDATE virtualbalance SET Balance = {0} where shortname = {self.coin} ")
        # modify 'virtualtrade' table
        self.database.requestDB(
            f"insert into virtualtrade(basecoin ,quotecoin,ordertype,quantity,tradetime) values('{kwargs['coin_for_order']}','{self.coin}','{kwargs['action']}','{kwargs['quantity']}','{str(datetime.now())}') ")
        # swap crypto
        self.coin = kwargs["coin_for_order"]

    def _sellOrder(self, **kwargs):
        """Virtual sell"""
        # modify 'virtualbalance' table
        # create new balance for the new crypto
        self.database.requestDB(
            f"UPDATE virtualbalance SET Balance = {kwargs['quantity']} where shortname = {kwargs['coin_for_order']} ")
        # delete balance on crypto i use to hold
        self.database.requestDB(f"UPDATE virtualbalance SET Balance = {0} where shortname = {self.coin} ")
        # modify 'virtualtrade' table
        self.database.requestDB(
            f"insert into virtualtrade(basecoin ,quotecoin,ordertype,quantity,tradetime) values('{kwargs['coin_for_order']}','{self.coin}','{kwargs['action']}','{kwargs['quantity']}','{str(datetime.now())}') ")
        # swap crypto
        self.coin = kwargs["coin_for_order"]

    def _getcoinsrelated(self, coin: str):
        # return all coins related quotecoins or basecoin

        infos = self.database.selectDB("select quotecoin from relationalcoin where basecoin ='" + coin + "'")
        basecoins = [info[0] for info in infos]

        infos = self.database.selectDB("select basecoin from relationalcoin where quotecoin ='" + coin + "'")
        quotecoins = [info[0] for info in infos]

        return {'quotecoins': quotecoins, 'basecoins': basecoins}

    def _get_crypto_pair_related(self, coin: str = None):
        cryptoinfo = self.database.selectDB(
            "select cryptopair from relationalcoin where basecoin ='" + coin + "'or quotecoin='" + coin + "'")

        cryptoinfo = [crypto[0] for crypto in cryptoinfo]
        return list(dict.fromkeys(cryptoinfo))

    def _getBasecoin_cryptopair(self, cryptopair):
        # sqlcon = mysqlDB()
        nn = self.database.selectDB(f"select  basecoin from relationalcoin where cryptopair='" + cryptopair + "'")
        if isinstance(nn, list) and len(nn) != 0:
            return nn[0][0]
        elif len(nn) == 0:
            return 'result not found'

    def _getQuotecoin_cryptopair(self, cryptopair):
        # sqlcon = mysqlDB()
        nn = self.database.selectDB(f"select  quotecoin from relationalcoin where cryptopair='" + cryptopair + "'")
        if isinstance(nn, list) and len(nn) != 0:
            return nn[0][0]
        elif len(nn) == 0:
            return 'result not found'

    @staticmethod
    def _basecoin_or_quotecoin(cryptopair: str = None, coin: str = None):
        if cryptopair.startswith(coin):

            return 'basecoin'
        elif cryptopair.endswith(coin):

            return 'quotecoin'

    def _get_many_klines(self, cryptopairs: list)->dict['cryptopair','klines']:
        """kline response:
            [
              [
                1499040000000,      // Open time
                "0.01634790",       // Open
                "0.80000000",       // High
                "0.01575800",       // Low
                "0.01577100",       // Close
                "148976.11427815",  // Volume
                1499644799999,      // Close time
                "2434.19055334",    // Quote asset volume
                308,                // Number of trades
                "1756.87402397",    // Taker buy base asset volume
                "28.46694368",      // Taker buy quote asset volume
                "17928899.62484339" // Ignore.
              ]
            ]
        """
        kline_uri = "https://api.binance.com/api/v3/klines"
        data = {
            # "symbol":'BNBBTC',
            "interval": self.timeframe,
            # "startTime": '1 day ago'
            # "endTime"
            "limit": 100
        }
        cryptoklines = {}
        for cryptopair in cryptopairs:
            data['symbol'] = cryptopair
            klines_list = requests.get(url=kline_uri, params=data)

            for kline in klines_list:
                kline[0] = datetime.datetime.fromtimestamp(kline[0] / 1e3)
                kline[6] = datetime.datetime.fromtimestamp(kline[6] / 1e3)
            klines = pd.DataFrame(klines_list)  # changer en dataframe
            # supprimer les collonnes qui ne sont pas necessaires
            klines.drop(columns=[6, 7, 8, 9, 10, 11], inplace=True)

            klines.columns = ['date', 'open', 'high', 'low',
                              'close', 'volume']  # renommer les colonnes

            cryptoklines = {cryptopair: klines}

        return cryptoklines

    def _crypto_study(self, klines:dict)->dict[str,str]:
        """study cryptopair with it's klines"""
        cryptopairs = list(klines.keys())

        results = {} #{'BNBBTC':'buy'}
        for cryptopair in cryptopairs:
            decision = self.Decision(klines[cryptopair])
            results[cryptopair] = decision
        return results

    def run(self):
        # get crypto related
        cryptopair_related: list = self._get_crypto_pair_related(coin=self.coin)

        # get all klines for each cryptopair
        klines: dict = self._get_many_klines(cryptopair_related)

        #get cryptopair with they study results
        cryptopairs_study = self._crypto_study(klines)
