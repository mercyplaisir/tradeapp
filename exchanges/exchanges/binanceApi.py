import datetime
import json
import random

import time
from dataclasses import dataclass
from typing import Type

import pandas as pd

# import requests
from binance.client import Client


from common import TIMEFRAME, send_data
from common.tools import interval_to_milliseconds, track_order, cout

from base import Coin, CryptoPair, Order

from base.sensitive import (
    BINANCE_PRIVATE_KEY,
    BINANCE_PUBLIC_KEY,
    BINANCE_PRIVATE_KEY_TEST,
    BINANCE_PUBLIC_KEY_TEST,
)


def connect(test: bool) -> Client:
    """Connect to binance"""
    if test:
        client = Client(BINANCE_PUBLIC_KEY_TEST, BINANCE_PRIVATE_KEY_TEST, testnet=True)
    elif not test:
        client = Client(BINANCE_PUBLIC_KEY, BINANCE_PRIVATE_KEY)
    cout(">>>Connected successfully to binance success")
    return client


TRADED: list[CryptoPair] = []

utils_file = "base/utils.json"

sleep_time = "5m"
capital = 100


# @dataclass
class BinanceClient:
    """My Binance account representation"""

    def __init__(self, testnet: bool = False) -> None:

        # Rescue Value
        self.rescue_coin: Coin = Coin("USDT")

        self.testnet: bool = testnet  # for testing

        # Binance instance
        self.client: Client = connect(test=testnet)

    @property
    def coin(self) -> Coin:
        """return coin object"""
        with open(utils_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            coin_name = data["tracked"]["coin"]
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
            data["tracked"]["coin"] = coin.name
            newvalue = json.dumps(data)
            f.write(newvalue)

    @property
    def cryptopair(self) -> CryptoPair:
        """cryptopair object"""
        with open(utils_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            cryptopair_name = data["tracked"]["cryptopair"]
        return CryptoPair(cryptopair_name)

    @cryptopair.setter
    def cryptopair(self, cryptopair: CryptoPair) -> None:
        """cryptopair setter"""
        with open(utils_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        with open(utils_file, "w", encoding="utf-8") as f:
            data["tracked"]["cryptopair"] = cryptopair.name
            newvalue = json.dumps(data)
            f.write(newvalue)

    @property
    def balance(self):
        """Balance getter"""
        return float(
            self.client.get_asset_balance(self.coin.name, recvWindow=60000)["free"]
        )

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
                cout(">>> No opportunity for trading")
                cout(cryptopair_decision_uncleaned)

                sleep_time_sec = interval_to_milliseconds(sleep_time) / 1000
                time.sleep(sleep_time_sec)
            else:
                cryptopairs = list(cryptopair_decision.items())  # [("BNB""buy"))]
                cryptopairs_size = len(cryptopairs) - 1
                cout("opportunities on: ", cryptopair_decision)

                cryptopair_study: tuple[CryptoPair, str] = cryptopairs[
                    random.randint(0, cryptopairs_size)
                ]  # ("BNB",("buy",3))
                cout(cryptopair_study)

                # time.sleep(20)

                choosen_cryptopair,order_type = cryptopair_study
                # pass order (the quantity is calculated in passing order)
                order: Order = self._pass_order(
                    cryptopair=choosen_cryptopair, order_type=order_type
                )

                self.cryptopair = choosen_cryptopair  # BNBBTC

                # track order
                track_order(order=order)
                send_data(
                    "post",
                    "/all",
                    profit=order.profit,
                    coin=self.coin,
                    cryptopair=self.cryptopair,
                )

                # cout(order.profit)

    def _pass_order(self, cryptopair: CryptoPair, order_type: str) -> Order:
        """Analyse and choose the right order to pass"""
        order_caller = {"buy": self._buy_order, "sell": self._sell_order}
        caller = order_caller[order_type]

        cout("%s for %s" % (order_type, cryptopair))
        order_details = caller(cryptopair)
        order = Order(**order_details)
        return order.save()

    def _cleaner(self, study: dict[CryptoPair, str]) -> dict[CryptoPair, str]:
        """Clean the given data througths the defined process"""
        cryptopairs: dict[CryptoPair, str] = study.items()
        results: dict[CryptoPair, str] = {}
        # clean
        for cryptopair, decision in cryptopairs:
            # when i possess ETH
            # ETHBTC must be a 'sell'
            if (cryptopair.is_basecoin(self.coin) and decision == "sell") or (
                cryptopair.is_quotecoin(self.coin) and decision == "buy"
            ):
                results[cryptopair] = decision
        return results

    def _buy_order(self, cryptopair: CryptoPair) -> dict:
        """
        Market Buy Order
        cryptopair .ex:BNBBTC, BTCUSDT
        """
        # order_quantity: float = self._order_quantity(cryptopair)
        order_details: dict = self.client.order_market_buy(
            symbol=cryptopair.name, recvWindow=60000, quoteOrderQty=self.balance
        )
        self.coin = cryptopair.replace(self.coin)
        cout(f">>>Buy Order passed for {cryptopair}")
        return order_details

    def _sell_order(self, cryptopair: CryptoPair) -> dict:
        """
        Market sell Order

        cryptopair .ex:BNBBTC, BTCUSDT
        """
        # order_quantity: float = self._order_quantity(cryptopair)
        balance = self.balance  # balance of the crypto i possess

        coin_price: float = cryptopair.get_price()
        q: float = balance * coin_price  # quantity
        q = float(round(q, 8))
        order_details: dict = self.client.order_market_sell(
            symbol=cryptopair,
            recvWindow=60000,
            # quantity=balance,
            quoteOrderQty=q,
        )

        self.coin = cryptopair.replace(self.coin)
        cout(f">>>Sell Order passed for {cryptopair} ")
        return order_details

    def __enter__(self):
        """enter special method"""
        send_data("post", "/all", status="on", enterTime=datetime.datetime.now())
        cout("entered")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """exit special method"""
        cout("exiting ....")
        if self.coin.name != "USDT":
            self._pass_order(self.rescue_cryptopair, "sell")
            self.coin = self.rescue_coin
        errors = {"type": exc_type, "value": exc_val}
        send_data(
            "post",
            "/all",
            status="off",
            errors=errors,
            coin=self.coin,
            cryptopair=self.cryptopair,
            exitTime=datetime.datetime.now(),
        )
        cout("exited")
