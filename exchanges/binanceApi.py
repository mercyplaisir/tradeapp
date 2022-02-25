import json
import random

import time
from dataclasses import dataclass
from typing import Type

import pandas as pd
import requests
from binance.client import Client


from common.tools import TIMEFRAME, URL, STATUS_ENDPOINT
from dbcontroller import DbEngine
from indicators.study import Study
from base import Coin, CryptoPair, Order

from base.sensitive import BINANCE_PRIVATE_KEY, BINANCE_PUBLIC_KEY


def connect() -> Client:
    """Connect to binance"""
    client = Client(BINANCE_PUBLIC_KEY, BINANCE_PRIVATE_KEY)
    print(">>>Connected successfully to binance success")
    return client


TRADED: list[CryptoPair] = []


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
    def api_public_key(self) -> str:
        """public key"""
        return BINANCE_PUBLIC_KEY

    @property
    def api_secret_key(self):
        """secret key"""
        return BINANCE_PRIVATE_KEY

    @property
    def coin(self) -> Coin:
        """return coin object"""
        with open("coin.json", "r", encoding="utf-8") as f:
            coin_name = json.load(f)

        return Coin(coin_name)

    @coin.setter
    def coin(self, coin: Coin) -> None:
        """coin setter"""
        with open("coin.json", "w", encoding="utf-8") as f:
            newvalue = json.dumps(coin.name)
            f.write(newvalue)

    @property
    def cryptopair(self) -> CryptoPair:
        """cryptopair object"""
        with open("cryptopair.json", "r", encoding="utf-8") as f:
            cryptopair_name = json.load(f)

        return CryptoPair(cryptopair_name)

    @cryptopair.setter
    def cryptopair(self, cryptopair: CryptoPair) -> None:
        """cryptopair setter"""
        with open("cryptopair.json", "w", encoding="utf-8") as f:
            newvalue = json.dumps(cryptopair.name)
            f.write(newvalue)

    @property
    def balance(self):
        """Balance getter"""
        return float(self.client.get_asset_balance(self.coin.name))

    def run(self):
        """main file to run"""

        while True:
            # get crypto related
            cryptopair_related: list[CryptoPair] = self.coin.get_cryptopair_related()

            # get all klines for each cryptopair
            klines: dict[CryptoPair, pd.DataFrame] = {
                cryptopair: cryptopair.get_klines() for cryptopair in cryptopair_related
            }

    def _buy_order(self, cryptopair: CryptoPair) -> Type[Order]:
        """
        Market Buy Order
        cryptopair .ex:BNBBTC, BTCUSDT
        """

        order_quantity: float = self._order_quantity(cryptopair)

        order_details: dict = self.client.order_market_buy(
            symbol=cryptopair.name, quantity=order_quantity
        )

        order = Order(**order_details)
        order.save()

        print(f">>>Buy Order passed for {cryptopair}")
        return Order

    def _sell_order(self, cryptopair: CryptoPair) -> Order:
        """
        Market sell Order

        cryptopair .ex:BNBBTC, BTCUSDT
        """
        order_quantity: float = self._order_quantity(cryptopair)
        order_details: dict = self.client.order_market_sell(
            symbol=cryptopair, quantity=order_quantity
        )
        order = Order(**order_details)
        order.save()

        print(f">>>Sell Order passed for {cryptopair.name}")
        return order

    def _order_quantity(self, cryptopair: CryptoPair) -> float:
        """
        parameters: -balance. ex: 20$
                    -coin. ex: BTC,ETH

        for use when buying

        return quantity(float)
        """
        balance = self.balance  # balance of the crypto i possess
        coin_price: float = cryptopair.get_price()  # cryptopair price
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

    def _pass_order(self, cryptopair: CryptoPair, order_type: str) -> Order:
        """Analyse and choose the right order to pass"""

        if order_type == "buy":
            return self._buy_order(cryptopair)
        elif order_type == "sell":
            return self._sell_order(cryptopair)

            # clean the cryptopairs_study dict so we only have
            # possible trades
            cryptopairs_study: dict[CryptoPair, str] = self._crypto_study(klines)

            if len(cryptopairs_study) == 0:
                time.sleep(int(TIMEFRAME.replace("m", "")) * 2)
            else:
                cryptopairs = list(cryptopairs_study.keys())
                # choose a crypto pair
                random_num = random.randint(0, len(cryptopairs) - 1)
                cryptopair_study: tuple[CryptoPair, str] = list(
                    cryptopairs_study.items()
                )[random_num]
                choosen_cryptopair, order_type = cryptopair_study
                # pass order (the quantity is calculated in passing order)
                order: Order = self._pass_order(
                    cryptopair=choosen_cryptopair, order_type=order_type
                )

                # set new values
                # bought BNBBTC
                old_coin = self.coin  # BTC
                self.coin = choosen_cryptopair.replace(coin=old_coin)  # BNB
                self.cryptopair = choosen_cryptopair  # BNBBTC

                # track order
                order.track_order()

    @staticmethod
    def _decision(klines: pd.DataFrame) -> str:
        """Calculate the prices and return a decision"""
        return Study.decision(klines)

    def _crypto_study(
        self, klines: dict[CryptoPair, pd.DataFrame]
    ) -> dict[CryptoPair, str]:
        """study cryptopair with it's klines"""
        cryptopairs = klines.items()
        # cryptopairs_names = [cryptopair.name for cryptopair in cryptopairs]
        decision_results: dict[CryptoPair, str] = {}  # {'BNBBTC':'buy'}

        for cryptopair, klines_df in cryptopairs:
            decision: str = self._decision(klines=klines_df)
            decision_results[cryptopair] = decision
        return self._cleaner(decision_results)

    def _cleaner(self, study: dict[CryptoPair, str]) -> dict[CryptoPair, str]:
        """Clean a returned study from Study module"""
        cryptopairs: dict[CryptoPair, str] = study.items()
        results: dict[CryptoPair, str] = {}
        #clean
        for cryptopair, decision in cryptopairs:
            # when i possess ETH
            # ETHBTC must be a 'sell'
            if (cryptopair.is_basecoin(self.coin) and decision == "sell") or (
                cryptopair.is_quotecoin(self.coin) and decision == "buy"
            ):
                results[cryptopair] = decision
        return results

    def __enter__(self):
        """enter special method"""
        data = {"status": "on"}
        status_url = URL + STATUS_ENDPOINT
        requests.post(status_url, data=data)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """exit special method"""
        data = {"status": "off"}
        status_url = URL + STATUS_ENDPOINT
        requests.post(status_url, data=data)
