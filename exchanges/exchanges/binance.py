import datetime
import json


import requests
from binance.client import Client


from common.tools import cout,get_config_file,send_data,set_new_data

from exchanges.base import Exchange

from base.sensitive import (
    BINANCE_PRIVATE_KEY,
    BINANCE_PUBLIC_KEY,
    BINANCE_PRIVATE_KEY_TEST,
    BINANCE_PUBLIC_KEY_TEST,
)

base_url = "https://api.binance.com"

def connect(test: bool) -> Client:
    """Connect to binance"""
    if test:
        client = Client(BINANCE_PUBLIC_KEY_TEST, BINANCE_PRIVATE_KEY_TEST, testnet=True)
    elif not test:
        client = Client(BINANCE_PUBLIC_KEY, BINANCE_PRIVATE_KEY)
    cout(">>>Connected successfully to binance success")
    return client



# @dataclass
class BinanceClient(Exchange):
    """My Binance account representation"""

    def __init__(self, testnet: bool = False) -> None:

        # Rescue Value
        self.rescue_coin: str = "USDT"

        self.testnet: bool = testnet  # for testing

        # Binance instance
        self.client: Client = connect(test=testnet)

    @property
    def coin(self) -> str:
        """return coin object"""
        
        return get_config_file()['coin']
    @property
    def rescue_cryptopair(self):
        """where to go when it goes down"""
        return self.coin + self.rescue_coin

    @coin.setter
    def coin(self, coin_name) -> None:
        """coin setter"""
        set_new_data(coin=coin_name)

    @property
    def cryptopair(self) -> str:
        """cryptopair object"""
        return get_config_file()['cryptopair']
    @cryptopair.setter
    def cryptopair(self, cryptopair) -> None:
        """cryptopair setter"""
        set_new_data(cryptopair=cryptopair)

    @property
    def balance(self):
        """Balance getter"""
        return float(
            self.client.get_asset_balance(self.coin, recvWindow=60000)["free"]
        )

    
    def pass_order(self, cryptopair_name: str, order_type: str) ->dict:
        """Analyse and choose the right order to pass"""
        order_caller = {"buy": self.buy_order, "sell": self.sell_order}
        caller = order_caller[order_type]

        cout("%s for %s" % (order_type, cryptopair_name))
        order_details = caller(cryptopair_name)


        old_coin = self.coin
        self.coin = cryptopair_name.replace(old_coin)
        
        #send order to the api
        send_data('post','/order',order_details)
        return order_details



    def buy_order(self, cryptopair_name: str) -> dict:
        """
        Market Buy Order
        cryptopair .ex:BNBBTC, BTCUSDT
        """
        # order_quantity: float = self._order_quantity(cryptopair)
        order_details: dict = self.client.order_market_buy(
            symbol = cryptopair_name,
            recvWindow = 60000,
            quoteOrderQty = self.balance
        )
        
        cout(f">>>Buy Order passed for {cryptopair_name}")
        return order_details

    def sell_order(self, cryptopair_name: str) -> dict:
        """
        Market sell Order

        cryptopair .ex:BNBBTC, BTCUSDT
        """
        # order_quantity: float = self._order_quantity(cryptopair)
        balance = self.balance  # balance of the crypto i possess

        coin_price: float = self.get_price(cryptopair_name)
        q: float = balance * coin_price  # quantity
        q = float(round(q, 8))
        order_details: dict = self.client.order_market_sell(
            symbol=cryptopair_name,
            recvWindow=60000,
            # quantity=balance,
            quoteOrderQty=q,
        )

        cout(f">>>Sell Order passed for {cryptopair_name} ")
        return order_details
    
    def get_price(self,name:str) -> float:
        """get price of a cryptopair"""
        url = "https://api.binance.comapi/v3/ticker/24hr?symbol=%s" % (name)
        resp = requests.get(url)
        return float(resp.json()["lastPrice"])

    def __enter__(self):
        """enter special method"""
        send_data(
            "post",
            "/all",
            status="on",
            enterTime=datetime.datetime.now()
        )
        cout("entered")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """exit special method"""
        cout("exiting ....")
        if self.coin != "USDT":
            self.pass_order(self.rescue_cryptopair, "sell")
            self.coin = self.rescue_coin
        errors = {"type": exc_type, "value": exc_val}
        config_file = get_config_file()
        send_data(
            "post",
            "/all",
            status="off",
            errors=errors,
            coin=self.coin,
            cryptopair=self.cryptopair,
            exitTime=datetime.datetime.now(),
            **config_file
        )
        cout("exited")
