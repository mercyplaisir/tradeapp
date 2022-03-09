import datetime
import json
from random import seed

import time
from dataclasses import dataclass
from typing import Type

import pandas as pd
# import requests
from binance.client import Client


from common import TIMEFRAME, STATUS_ENDPOINT, send_data
from common.tools import interval_to_milliseconds,track_order,cout
from dbcontroller import DbEngine

from base import Coin, CryptoPair, Order, cryptopair

from base.sensitive import BINANCE_PRIVATE_KEY, BINANCE_PUBLIC_KEY






def connect() -> Client:
    """Connect to binance"""
    client = Client(BINANCE_PUBLIC_KEY, BINANCE_PRIVATE_KEY)
    cout(">>>Connected successfully to binance success")
    return client


TRADED: list[CryptoPair] = []

utils_file = 'base/utils.json'

@dataclass
class BinanceClient:
    """My Binance account representation"""

    # Timeframe

    # Rescue Value
    rescue_coin: Coin = Coin("USDT")

    # Binance instance
    client: Client = connect()
    # Database Instance
    database: DbEngine = DbEngine()

    # price when placed order
    # order_price: float = 0.0

    @property
    def coin(self) -> Coin:
        """return coin object"""
        with open(utils_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            coin_name = data['tracked']['coin']
        return Coin(coin_name)

    @property
    def rescue_cryptopair(self):
        """where to go when it goes down"""
        if self.coin == self.rescue_coin:
            return
        return self.coin + self.rescue_coin

    @coin.setter
    def coin(self, coin: Coin) -> None:
        """coin setter"""
        with open(utils_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        with open(utils_file, "w", encoding="utf-8") as f:
            data['tracked']['coin'] = coin.name
            newvalue = json.dumps(data)
            f.write(newvalue)

    @property
    def cryptopair(self) -> CryptoPair:
        """cryptopair object"""
        with open(utils_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            cryptopair_name = data['tracked']['cryptopair']
        return CryptoPair(cryptopair_name)

    @cryptopair.setter
    def cryptopair(self, cryptopair: CryptoPair) -> None:
        """cryptopair setter"""
        with open(utils_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        with open(utils_file, "w", encoding="utf-8") as f:
            data['tracked']['cryptopair'] = cryptopair.name
            newvalue = json.dumps(data)
            f.write(newvalue)
    @property
    def balance(self):
        """Balance getter"""
        return float(self.client.get_asset_balance(self.coin.name,recvWindow=60000)['free'])

    def run(self):
        """main file to run"""
        cout("run method")
        while True:
            # get crypto related
            cryptopair_related: list = self.coin.get_cryptopair_related()
            
            # get all decision for each cryptopair
            cryptopair_decision_uncleaned: dict[CryptoPair, pd.DataFrame] = {
                cryptopair: cryptopair.decision() for cryptopair in cryptopair_related
            }
            
            # clean the cryptopairs_study dict so we only have
            # possible trades
            cryptopair_decision = self._cleaner(cryptopair_decision_uncleaned)
            
            if len(cryptopair_decision) == 0:
                cout('>>> No opportunity for trading')
                cout(cryptopair_decision_uncleaned)
                sleep_time = interval_to_milliseconds(TIMEFRAME)/1000
                time.sleep(sleep_time)
            else:
                cryptopairs = list(cryptopair_decision.items())  # [("BNB",("buy",3))]
                cout("opportunities on: ",cryptopair_decision)
                # contains nb_of indicators that approved
                nb_indic = [value[1] for _, value  in cryptopairs]  # value= ("buy",1)

                index_of_max = nb_indic.index(
                    max(nb_indic)
                )  # index of the higher value

                cryptopair_study: tuple[CryptoPair, tuple[str, int]] = cryptopairs[
                    index_of_max
                ]  # ("BNB",("buy",3))
                cout(cryptopair_study)

                time.sleep(20)

                choosen_cryptopair, (order_type, _) = cryptopair_study
                # pass order (the quantity is calculated in passing order)
                order: Order = self._pass_order(
                    cryptopair=choosen_cryptopair, order_type=order_type
                )

                # set new values
                # bought BNBBTC
                # old_coin = self.coin  # BTC
                # self.coin = choosen_cryptopair.replace(coin=old_coin)  # BNB
                self.cryptopair = choosen_cryptopair  # BNBBTC

                # track order
                track_order(order=order)
                

    def _pass_order(self, cryptopair: CryptoPair, order_type: str) -> Order:
        """Analyse and choose the right order to pass"""
        order_caller = {"buy": self._buy_order, "sell": self._sell_order}
        caller = order_caller[order_type]

        cout('%s for %s'%(order_type,cryptopair))
        order_details = caller(cryptopair)
        order = Order(**order_details)
        return order.save()

    def _cleaner(
        self, study: dict[CryptoPair, tuple[str, int]]
    ) -> dict[CryptoPair, str]:
        """Clean the given data througths the defined process"""
        cryptopairs: dict[CryptoPair, tuple] = study.items()
        results: dict[CryptoPair, str] = {}
        # clean
        for cryptopair, data in cryptopairs:
            decision, _ = data
            # when i possess ETH
            # ETHBTC must be a 'sell'
            if (cryptopair.is_basecoin(self.coin) and decision == "sell") or (
                cryptopair.is_quotecoin(self.coin) and decision == "buy"
            ):
                results[cryptopair] = data
        return results

    def _buy_order(self, cryptopair: CryptoPair) -> dict:
        """
        Market Buy Order
        cryptopair .ex:BNBBTC, BTCUSDT
        """

        # order_quantity: float = self._order_quantity(cryptopair)
        order_details: dict = self.client.order_market_buy(
            symbol=cryptopair.name,recvWindow=60000,quoteOrderQty=self.balance
        )
        self.coin = cryptopair.replace(self.coin)
        cout(f">>>Buy Order passed for {cryptopair}")
        return order_details

    def _sell_order(self, cryptopair: CryptoPair) -> dict:
        """
        Market sell Order

        cryptopair .ex:BNBBTC, BTCUSDT
        """
        order_quantity: float = self._order_quantity(cryptopair)
        order_details: dict = self.client.order_market_sell(
            symbol=cryptopair, quantity=order_quantity,recvWindow=60000)
        self.coin = cryptopair.replace(self.coin)
        cout(f">>>Sell Order passed for {cryptopair} ")
        return order_details

    def _order_quantity(self, cryptopair: CryptoPair) -> float:
        """
        parameters: -balance. ex: 20$
                    -coin. ex: BTC,ETH

        for use when buying

        return quantity(float)
        """
        balance = self.balance  # balance of the crypto i possess
        coin_price: float = (
            cryptopair.get_price()
        )  # price of the crypto i want to go in
        q: float = balance / coin_price  # quantity

        if coin_price < 0.18:
            return float(str(q)[:3])
        coin_prices: dict[int, range] = {
            2: range(15, -1, -1),
            3: range(16, 49),
            5: range(50, 5000),
            6: range(5000, 10**6),
        }
        for item in coin_prices.items():
            key, value = item
            if coin_price in value:
                return float(str(q)[:key])
        cout('>>> Getting quantity for %s'%cryptopair)

    def __enter__(self):
        """enter special method"""
        send_data("post", STATUS_ENDPOINT, status="on")
        cout('entered')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """exit special method"""
        cout("exiting ....")
        if self.coin.name != 'USDT':
            self._pass_order(self.rescue_cryptopair, "sell")
            self.coin = self.rescue_coin
        send_data(
            "post",
            STATUS_ENDPOINT,
            status="off"
        #     exc_type=exc_type,
        #     exc_val=exc_val,
        #     exc_tb=exc_tb,
        )
        cout("exited")
