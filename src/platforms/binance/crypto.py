import datetime
from dataclasses import dataclass

import pandas as pd
import requests

from src.dbcontroller.mysqlDB import mysqlDB
from src.platforms.binance.coin import Coin


@dataclass
class CryptoPair(object):
    """
    a representation of a cryptopair
    ex: BNBBTC
    """
    name: str
    database = mysqlDB()
    TIMEFRAME = "5m"

    def __post_init__(self):
        self.verify()

    def verify(self):
        """Verify if the crypto pair really exits in the database"""

        nn = self.database.selectDB(f"select basecoin from relationalcoin" +
                                    " where cryptopair='" + self.name + "'")
        if len(nn) == 0:
            raise ValueError("the cryptopair doesn't exit in the database")

    @property
    def basecoin(self) -> Coin:
        """return a basecoin from a cryptopair
        ex: BNBBTC return BNB"""
        nn = self.database.selectDB(f"select basecoin from relationalcoin" +
                                    " where cryptopair='" + self.name + "'")

        name: str = nn[0][0]
        return Coin(name)

    @property
    def quotecoin(self) -> Coin:
        """return quotecoin from a cryptopair 
        ex: BNBBTC return BTC"""
        nn = self.database.selectDB(f"select quotecoin from relationalcoin" +
                                    " where cryptopair='" + self.name + "'")

        name: str = nn[0][0]
        return Coin(name)

    def is_basecoin(self, coin: Coin) -> bool:
        """return True if it iss a basecoin"""
        return self.name.startswith(coin.name)

    def is_quotecoin(self, coin: Coin) -> bool:
        """return True if it iss a quotecoin"""
        return self.name.endswith(coin.name)

    def is_any(self, coin: Coin):
        """To see if a coin is in the cryptopair"""
        if self.is_basecoin(coin) or self.is_quotecoin(coin):
            return True
        else:
            raise ValueError(f"{coin.name} is not in {self.name} ")
    
    def replace(self,coin:Coin)->Coin:
        """return basecoin if the given coin is quotecoin vice-versa"""
        if self.is_basecoin(coin):
            return self.quotecoin
        elif self.is_quotecoin(coin):
            return self.basecoin
        else:
            raise ValueError(f"{coin.name} is not in {self.name} ")

    def get_price(self) -> float:
        """get price of a cryptopair"""
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={self.name}"
        resp = requests.get(url)
        return float(resp.json()['lastPrice'])

    def get_price_change(self) -> float:
        """gets priceChange of a crypto pair"""
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={self.name}"
        resp = requests.get(url)
        return float(resp.json()['priceChangePercent'])
    

    def get_klines(self, interval: str = "2 days"):

        """
            Get the klines for the timeframe given and in interval given.
            timeframe ex:1m,5m,15m,1h,2h,6h,8h,12h,1d,1M,1w,3d

            Default timeframe = 15m
            Default interval = 2 days


            colums=["open_time","open_price","close_price","SMA_30","SMA_50","SMA_20","upper_band","lower_band"]
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

            stores the klines in a csv file
        """
        # klines_list = self.client.get_historical_klines(
        #     self.name, self.TIMEFRAME, f"{interval} ago UTC")
        url: str = f"https://api.binance.com/api/v3/klines?symbol={self.name}&interval={self.TIMEFRAME}"
        klines_list: list = requests.get(url).json()

        # changer timestamp en date
        for kline in klines_list:
            kline[0] = datetime.datetime.fromtimestamp(kline[0] / 1e3)

        klines = pd.DataFrame(klines_list)  # changer en dataframe

        # delete unuseful columns
        klines.drop(columns=[6, 7, 8, 9, 10, 11], inplace=True)

        klines.columns = ['date', 'open', 'high', 'low',
                          'close', 'volume']  # rename columns

        # klines.to_csv(BINANCEKLINES, index=False)
        return klines
