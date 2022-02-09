import json
import random
import time
from dataclasses import dataclass, field
from typing import Type

import pandas as pd
from binance.client import Client

from src.dbcontroller.mysqlDB import mysqlDB
from src.indicators.study import Study
from src.platforms.binance.coin import Coin
from src.platforms.binance.crypto import CryptoPair
from src.platforms.binance.order import Order
from src.platforms.binance.sensitive import BINANCE_PRIVATE_KEY, BINANCE_PUBLIC_KEY
from src.tools import Tool as tl


@dataclass
class Binance:  # (Study, BinanceWebsocket):

    TIMEFRAME: str = field(init=False, default="15m")
    _coin: Coin = field(init=False)
    lastOrderWasBuy: bool = field(init=False, default=False, repr=False)

    def __post_init__(self):

        self.client: Client = self.connect()  # binanceClient

        self.database = mysqlDB()
        print(">>>Initialisation terminee")

        self.boughtAt = 0
        self.soldAt = 0

    @property
    def apiPublicKey(self) -> str:
        """public key"""
        return BINANCE_PUBLIC_KEY

    @property
    def apiSecretKey(self):
        """secret key"""
        return BINANCE_PRIVATE_KEY

    @property
    def coin(self) -> Coin:
        """return coin object"""
        with open("coin.json", 'r') as f:
            coin_name = json.load(f)
            self._coin = Coin(coin_name)
        return self._coin

    @coin.setter
    def coin(self, coin_name: str) -> None:
        with open("coin.json", 'w') as f:
            newvalue = json.dumps(coin_name)
            f.write(newvalue)
        self._coin: Coin = Coin(coin_name)

    @property
    def balance(self):
        return float(self.client.get_asset_balance(self.coin.name))

    def connect(self) -> Client:
        """Connect to binance """
        client = Client(self.apiPublicKey, self.apiSecretKey)
        print(">>>connection a BINANCE effectue avec succes")
        return client

    def buy_order(self, cryptopair: CryptoPair) -> Type[Order]:
        """
        Market Buy Order
        cryptopair .ex:BNBBTC, BTCUSDT
        """

        # coinName: str = cryptopair.replace(self.coin, '')
        order_quantity: float = self.orderQuantity(cryptopair)

        orderDetails: dict = self.client.order_market_buy(
            symbol=cryptopair.name, quantity=order_quantity)

        order = Order(**orderDetails)
        order.save()
        self.lastOrderWasBuy = True
        print(f">>>Buy Order passed for {cryptopair}")
        return Order

    def sell_order(self, cryptopair: CryptoPair) -> Order:
        """
        Market sell Order

        cryptopair .ex:BNBBTC, BTCUSDT
        """
        # coinName: str = cryptopair.replace(self.coin, '')

        order_quantity: float = self.orderQuantity(cryptopair)

        orderDetails: dict = self.client.order_market_sell(
            symbol=cryptopair, quantity=order_quantity)
        order = Order(**orderDetails)
        order.save()
        self.lastOrderWasBuy = False
        print(f">>>Sell Order passed for {cryptopair.name}")
        return order

    def orderQuantity(self, cryptopair: CryptoPair) -> float:
        """
                parameters: -balance. ex: 20$
                            -coin. ex: BTC,ETH

                for use when buying

                return quantity(float)
                """
        balance = self.balance  # balance of the crypto i possess
        if cryptopair.is_any(self.coin):
            coin_price: float = cryptopair.get_price()  # prix du cryptopair

            q = balance / coin_price  # Quantite
            coin_prices: dict[int, range] = {
                2: range(15, -1, -1),
                3: range(16, 49),
                5: range(50, 5000),
                6: range(5000, 10 ** 6)
            }
            if coin_price < 0.18:
                return float(str(q)[:3])
            for key in coin_prices.keys():
                if coin_price in coin_prices[key]:
                    return float(str(q)[:key])

    def pl_calculator(self):
        """
        PROFIT/LOSS calculator
        """
        if self.lastOrderWasBuy:
            return "Still in a Buy Trade"
        return tl.percent_change(self.boughtAt, self.soldAt)

    def pass_order(self, cryptopair: CryptoPair):
        if cryptopair.is_any(self.coin):
            return self.buy_order(cryptopair) if cryptopair.is_basecoin(self.coin) else self.sell_order(cryptopair)
        return Exception("Unable to pass order")

    def _crypto_study(self, klines: dict[CryptoPair, pd.DataFrame]) -> dict[str, str]:
        """study cryptopair with it's klines"""
        cryptopairs = list(klines.keys())
        cryptopairs_names = [cryptopair.name for cryptopair in cryptopairs]
        results = {}  # {'BNBBTC':'buy'}

        for cryptopair in cryptopairs:
            kline: pd.DataFrame = klines.pop(cryptopair)
            decision = self.decision(kline)
            results[cryptopair]: list[str] = decision
        return results

    def _cleaner(self, study: dict) -> dict[str, str]:
        cryptopairs = list(study.keys())

        results = {}
        for cryptopair in cryptopairs:
            # when i possess ETH
            # ETHBTC must be a 'sell'
            if (cryptopair.startswith(self.coin) and study[cryptopair] == 'sell') or (
                    cryptopair.is_any(self.coin) and study[cryptopair] == 'buy'
            ):
                results[cryptopair] = study[cryptopair]
        return results

    def run(self):

        while True:
            # get crypto related
            cryptopair_related: list[CryptoPair] = self.coin.get_cryptopair_related()

            # get all klines for each cryptopair
            klines: dict[CryptoPair, pd.DataFrame] = {
                cryptopair: cryptopair.get_klines() for cryptopair in cryptopair_related}

            # get cryptopair with they study results
            cryptopairs_study_unclean:dict[CryptoPair,str] = self._crypto_study(klines)

            # clean the cryptopairs_study dict so we only have
            # possible trades
            cryptopairs_study = self._cleaner(cryptopairs_study_unclean)

            if len(cryptopairs_study) == 0:
                time.sleep(int(self.TIMEFRAME.replace('m', '')) * 5)
            else:
                cryptopairs = list(cryptopairs_study.keys())
                # choose a crypto pair
                cryptopair: CryptoPair = cryptopairs[random.randint(0, len(cryptopairs) - 1)]

                # pass order (the quantity is calculated in passing order)
                self.pass_order(cryptopair)

                # set new coin
                old_coin = self.coin
                self.coin = cryptopair.name.replace(self.coin, '')

                time.sleep(int(self.TIMEFRAME.replace('m', '')) * 5)

    def status(self):
        """send status to to the server """
        pass

    def decision(self, klines: pd.DataFrame):
        """Calculate the prices and return a decision"""
        return Study.decision(klines)
