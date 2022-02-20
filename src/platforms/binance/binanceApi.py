import json
import random
from re import A
import time
from dataclasses import dataclass
from typing import Type

import pandas as pd
import requests
from binance.client import Client

from src.common.tools import Tool as tl
from src.dbcontroller.mysqlDB import mysqlDB
from src.indicators.study import Study
from src.platforms.binance import Coin
from src.platforms.binance import CryptoPair
from src.platforms.binance import Order
from src.platforms.binance.sensitive import BINANCE_PRIVATE_KEY, BINANCE_PUBLIC_KEY


def connect() -> Client:
    """Connect to binance """
    client = Client(BINANCE_PUBLIC_KEY, BINANCE_PRIVATE_KEY)
    print(">>>Connected successfully to binance success")
    return client


URL =  'https://tradeappapiassistant.herokuapp.com/tradeapp'

STATUS_ENDPOINT = '/status'
HISTORY_ENDPOINT ='/history'

TRADED:list[CryptoPair] = []

@dataclass
class BinanceClient:
    """My Binance account representation"""
    # Timeframe
    TIMEFRAME: str = '15m'  

    # Rescue Value
    rescue_coin:Coin = Coin('USDT')
     
    # track last order,
    lastOrderWasBuy: bool = False  
    
    # Binance instance
    client: Client = connect()  
    # Database Instance
    database: mysqlDB = mysqlDB()

    # Buying price
    boughtAt: int = 0  
    # Selling price
    soldAt: int = 0 
        
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
            
        return Coin(coin_name)

    @coin.setter
    def coin(self, coin: Coin) -> None:
        """coin setter"""
        with open("coin.json", 'w') as f:
            newvalue = json.dumps(coin.name)
            f.write(newvalue)
        
    
    @property
    def cryptopair(self) -> CryptoPair:
        """cryptopair object"""
        with open("cryptopair.json", 'r') as f:
            cryptopair_name = json.load(f)
        
        return CryptoPair(cryptopair_name)

    @cryptopair.setter
    def cryptopair(self, cryptopair: CryptoPair) -> None:
        """cryptopair setter"""
        with open("cryptopair.json", 'w') as f:
            newvalue = json.dumps(cryptopair.name)
            f.write(newvalue)
        

    @property
    def balance(self):
        """Balance getter"""
        return float(self.client.get_asset_balance(self.coin.name))

    def _buy_order(self, cryptopair: CryptoPair) -> Type[Order]:
        """
        Market Buy Order
        cryptopair .ex:BNBBTC, BTCUSDT
        """

        
        order_quantity: float = self._order_quantity(cryptopair)

        orderDetails: dict = self.client.order_market_buy(
            symbol=cryptopair.name, quantity=order_quantity)

        order = Order(**orderDetails)
        order.save()
        self.lastOrderWasBuy = True
        print(f">>>Buy Order passed for {cryptopair}")
        return Order

    def _sell_order(self, cryptopair: CryptoPair) -> Order:
        """
        Market sell Order

        cryptopair .ex:BNBBTC, BTCUSDT
        """
        # coinName: str = cryptopair.replace(self.coin, '')

        order_quantity: float = self._order_quantity(cryptopair)

        orderDetails: dict = self.client.order_market_sell(
            symbol=cryptopair, quantity=order_quantity)
        order = Order(**orderDetails)
        order.save()
        self.lastOrderWasBuy = False
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
        if cryptopair.is_any(self.coin):
            coin_price: float = cryptopair.get_price()  # cryptopair price

            q = balance / coin_price  # quantity
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

    def _pl_calculator(old_number:float,new_number:float):
        """
        PROFIT/LOSS calculator
        """
        return tl.percent_change(old_number, new_number)

    def _pass_order(self, cryptopair: CryptoPair):
        """Analyse and choose the right order to pass"""
        if cryptopair.is_any(self.coin):
            return self._buy_order(cryptopair) if cryptopair.is_basecoin(self.coin) else self._sell_order(cryptopair)
        return Exception("Unable to pass order")

    def run(self):
        """main file to run"""

        while True:
            # get crypto related
            cryptopair_related: list[CryptoPair] = self.coin.get_cryptopair_related()

            # get all klines for each cryptopair
            klines: dict[CryptoPair, pd.DataFrame] = {
                cryptopair: cryptopair.get_klines() for cryptopair in cryptopair_related}

            # clean the cryptopairs_study dict so we only have
            # possible trades
            cryptopairs_study:dict[CryptoPair,pd.DataFrame] = self._crypto_study(klines)

            if len(cryptopairs_study) == 0:
                time.sleep(int(self.TIMEFRAME.replace('m', '')) * 2)
            else:
                cryptopairs = list(cryptopairs_study.keys())
                # choose a crypto pair
                cryptopair: CryptoPair = cryptopairs[random.randint(0, len(cryptopairs) - 1)]

                # pass order (the quantity is calculated in passing order)
                self._pass_order(cryptopair)

                # set new values
                # bought BNBBTC
                old_coin = self.coin #BTC
                self.coin = cryptopair.replace(old_coin) # BNB
                self.cryptopair = cryptopair # BNBBTC

                #track order
                self.track_order()
                

                #sleep time
                # time.sleep(int(self.TIMEFRAME.replace('m', '')) * 5)
    def tract_order(self):
        """track a order so it reverse it's order to make an profit"""

    @staticmethod
    def _decision(klines: pd.DataFrame) -> str:
        """Calculate the prices and return a decision"""
        return Study.decision(klines)

    def _crypto_study(self, klines: dict[CryptoPair, pd.DataFrame]) -> dict[CryptoPair, str]:
        """study cryptopair with it's klines"""
        cryptopairs = list(klines.keys())
        # cryptopairs_names = [cryptopair.name for cryptopair in cryptopairs]
        decision_results: dict[CryptoPair, str] = {}  # {'BNBBTC':'buy'}

        for cryptopair in cryptopairs:
            kline: pd.DataFrame = klines.pop(cryptopair)
            decision = self._decision(kline)
            decision_results[cryptopair] = decision
        return self._cleaner(decision_results)

    def _cleaner(self, study: dict[CryptoPair, str]) -> dict[CryptoPair, str]:
        """Clean a returned study from Study module"""
        cryptopairs: list[CryptoPair] = list(study.keys())
        results: dict[CryptoPair, str] = {}
        for cryptopair in cryptopairs:
            # when i possess ETH
            # ETHBTC must be a 'sell'
            if (cryptopair.is_basecoin(self.coin) and study[cryptopair] == 'sell') or (
                    cryptopair.is_quotecoin(self.coin) and study[cryptopair] == 'buy'
            ):
                results[cryptopair] = study[cryptopair]
        return results

    def __enter__(self):
        """enter special method"""
        data = {
            'status': 'on'
        }
        status_url = URL + STATUS_ENDPOINT
        requests.post(status_url, data=data)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """exit special method"""
        data = {
            'status': 'off'
        }
        status_url = URL + STATUS_ENDPOINT
        requests.post(status_url, data=data)
