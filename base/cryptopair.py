"""About Cryptocurrency

class : CRYPTOPAIR,COIN

"""
from abc import ABC
import datetime
from typing import Literal, Protocol


import pandas as pd
import requests

from common import TIMEFRAME
from dbcontroller import DbEngine
from strategies.study import Study
from errors.errors import CoinNotFound

# from base import Coin

db = DbEngine()

real = 'api'
test = ''

BINANCE_API_URL = "https://api.binance.com"

BINANCE_TESTNET_API_URL = "https://testnet.binance.vision"

base_url = BINANCE_API_URL
# TICKER_24H = EXCHANGE_API_URL + "/v3/ticker/24hr?symbol=%s"



class CryptoObject(ABC):
    pass


class CryptoPair(CryptoObject):
    """
    a representation of a cryptopair
    ex: BNBBTC
    """

    def __init__(self, name: str,quotecoin:bool) -> None:

        self.name: str = name
        self._principal_coin = self.basecoin if quotecoin else self.quotecoin
        # self.verify()

    def get_name(self):
        """return Cryptopair name"""
        return self.name

    @property
    def basecoin(self) -> CryptoObject:
        """return a basecoin from a cryptopair
        ex: BNBBTC return BNB"""
        return self.get_basecoin()

    @property
    def quotecoin(self) -> CryptoObject:
        """return quotecoin from a cryptopair
        ex: BNBBTC return BTC"""
        return self.get_quotecoin()
    def verify(self):
        """Verify if the crypto pair really exits in the database"""

        if not self.basecoin:
            raise ValueError("the cryptopair doesn't exit in the database")

        return self.get_quotecoin()
        

    def is_basecoin(self, coin: CryptoObject) -> bool:
        """return True if it iss a basecoin"""
        return self.basecoin == coin

    def is_quotecoin(self, coin: CryptoObject) -> bool:
        """return True if it iss a quotecoin"""
        return self.quotecoin == coin

    def is_any(self, coin: CryptoObject):
        """To see if a coin is in the cryptopair"""
        if self.is_basecoin(coin) or self.is_quotecoin(coin):
            return True
        # if not found
        raise ValueError(f"{coin.name} is not in {self.name} ")

    def replace(self, coin: CryptoObject) -> CryptoObject:
        """return basecoin if the given coin is quotecoin vice-versa"""
        if self.is_basecoin(coin):
            return self.quotecoin
        elif self.is_quotecoin(coin):
            return self.basecoin
        # not found in cryptopair
        raise ValueError(f"{coin.name} is not in {self.name} ")

    def get_price(self) -> float:
        """get price of a cryptopair"""
        url = "%s/api/v3/ticker/24hr?symbol=%s" % (base_url,self.name)
        resp = requests.get(url)
        return float(resp.json()["lastPrice"])

    def get_price_change(self) -> float:
        """gets priceChange of a crypto pair"""
        url = "%s/api/v3/ticker/24hr?symbol=%s" % (base_url,self.name)
        resp = requests.get(url)
        return float(resp.json()["priceChangePercent"])

    def get_klines(self) -> pd.DataFrame:

        """
        Get the klines for the timeframe given and in interval given.
        timeframe ex:1m,5m,15m,1h,2h,6h,8h,12h,1d,1M,1w,3d

        Default timeframe = 15m
        Default interval = 2 days


        colums=["open_time","open_price","close_price","SMA_30","SMA_50","SMA_20",
        "upper_band","lower_band"]
        kline response:
            [
              [
                1499040000000,      // Open time
                "0.01634790",       // Open
                "0.80000000",       // High
                "0.01575800",       // Low
                "0.01577100",       // Close
                "148976.11427815",  // Volume
                1499644799999,      // Close time               6
                "2434.19055334",    // Quote asset volume
                308,                // Number of trades
                "1756.87402397",    // Taker buy base asset volume      '
                "28.46694368",      // Taker buy quote asset volume     'Q'
                "17928899.62484339" // Ignore.  'B'
              ]
            ]


        """
        # klines_list = self.client.get_historical_klines(
        #     self.name, self.TIMEFRAME, f"{interval} ago UTC")
        url: str = f"{base_url}/api/v3/klines?symbol={self.get_name()}&interval={TIMEFRAME}"
        klines_list: list = requests.get(url).json()

        # changer timestamp en date
        for kline in klines_list:
            kline[0] = datetime.datetime.fromtimestamp(kline[0] / 1e3)

        klines: pd.DataFrame = pd.DataFrame(klines_list)  # changer en dataframe

        # delete unuseful columns
        klines.drop(columns=[6, 7, 8, 9, 10, 11], inplace=True)

        klines.columns = [
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]  # rename columns
        klines[['open','close','high','low','volume']] = klines[['open','close','high','low','volume']].astype('float64')
        klines = klines.set_index('date')
        # print(f"klines for {self.name}")
        # klines.to_csv(BINANCEKLINES, index=False)
        return klines

    def __repr__(self) -> str:
        return self.name

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.get_name())
        
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o,str):
            return self.name == __o
        elif isinstance(__o,Coin):
            return self.name == __o.name
        return

    @classmethod
    def _decision(cls, klines: pd.DataFrame) -> Literal['buy','sell','wait']:
        """Calculate the prices and return a decision"""
        return Study.decision(klines)

    def decision(self):
        """study cryptopair with it's klines"""
        klines_df = self.get_klines()
        dec = self._decision(klines=klines_df)
        return dec
    
    def get_basecoin(self)->CryptoObject:
        result = db.select(
            f"select basecoin from relationalcoin where cryptopair='{self.get_name()}'"
        )
        name: str = result[0][0]
        return Coin(name)
        
    def get_quotecoin(self)->CryptoObject:
        result = db.select(
            "select quotecoin from relationalcoin"
            + f" where cryptopair='{self.name}'"
        )

        name: str = result[0][0]
        return Coin(name)

    @classmethod
    def study(cls,data:list[CryptoObject]):
        """study a given list of cryptopsirs
         and return profitable cryptopsirs"""
        cryptopair_decision_uncleaned: dict[CryptoPair, pd.DataFrame] = {
            cryptopair: cryptopair.decision() for cryptopair in data
        }

        # clean the cryptopairs_study dict so we only have
        # possible trades
        return cls._cleaner(cryptopair_decision_uncleaned)
        

    @classmethod
    def _cleaner(cls, study: dict[CryptoObject, str]):# -> dict[cls, str]:
        """Clean the given data througths the defined process"""
        cryptopairs: dict[cls, str] = study.items()
        results: dict[cls, str] = {}
        # clean
        for cryptopair, decision in cryptopairs:
            # when i possess ETH
            # ETHBTC must be a 'sell'
            coin_i_possess =cryptopair._principal_coin

            valid_sell:bool = cryptopair.is_basecoin(coin_i_possess) and decision == "sell"
            valid_buy: bool = cryptopair.is_quotecoin(coin_i_possess) and decision == "buy"
            
            if valid_sell or valid_buy:
                results[cryptopair] = decision
        return results
    
    def sell_quantity(self):
        """calculate the quantity for a sell order"""


class Coin(CryptoObject):
    """
    Representation of a Coin

    ex: BNB
    """

    def __init__(self, name) -> None:

        self.name: str = name
        # self.verify()

    def __repr__(self):
        return f"{self.name}({self.fullname})"

    def get_name(self):
        """return self.name"""
        return self.name

    def verify(self):
        """verify if the given coin name exists in database"""
        result = db.select(
            request="select fullname from Coin where shortname='"
            + self.get_name()
            + "'"
        )
        if len(result) == 0:
            raise CoinNotFound("the coin does not exist in the database")

    @property
    def fullname(self):
        """fullname getter"""
        return db.select(
            request="select fullname from Coin where shortname='"
            + self.get_name()
            + "'"
        )[0][0]
    
    @property
    def price(self):
        url = "https://testnet.binance.vision/api/v3/ticker/price?symbol=%s" % (self.name+'USDT')
        resp = requests.get(url).json()
        return float(resp["price"])


    def get_cryptopair_related(self) -> list[CryptoObject]:
        """return all coins related cryptopair
        where the coin appears to be a quotecoin
         or basecoin"""
        coin_name = self.get_name()
        cryptopairs_basecoins: list[tuple[str]] = db.select(
            request="select cryptopair from relationalcoin where basecoin ='"
            + coin_name +"' "
        )
        basecoins = [CryptoPair(cryptopair_name[0],quotecoin=False) for cryptopair_name in cryptopairs_basecoins]
        cryptopairs_name: list[tuple[str]] = db.select(
            request="select cryptopair from relationalcoin where quotecoin ='"
            + coin_name
            + "' "
        )
        quotecoins = [CryptoPair(cryptopair_name[0],quotecoin=True) for cryptopair_name in cryptopairs_name]
        return basecoins + quotecoins


    @staticmethod
    def get_all_coins():
        """Return all coins stored in the database"""
        result: list[tuple[str]] = db.select(request="select shortname from Coin")
        return [Coin(name[0]) for name in result]
    
    def __add__(self, other: object) -> CryptoPair:
        return CryptoPair(self.name + other.name)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o,str):
            return self.name == __o
        elif isinstance(__o,Coin):
            return self.name == __o.name
        return

