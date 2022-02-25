"""About Cryptocurrency

class : CRYPTOPAIR,COIN

"""

import datetime


import pandas as pd
import requests

from common import TIMEFRAME
from dbcontroller import DbEngine

# from base import Coin

db = DbEngine()


BINANCE_API_URL = "https://api.binance.com"
TICKER_24H = BINANCE_API_URL + "/api/v3/ticker/24hr?symbol=%s"


class Coin:
    ...


class CryptoPair:
    """
    a representation of a cryptopair
    ex: BNBBTC
    """

    def __init__(self, name: str) -> None:

        self.name: str = name
        self.verify()

    def get_name(self):
        """return Cryptopair name"""
        return self.name

    def verify(self):
        """Verify if the crypto pair really exits in the database"""

        result = db.selectDB(
            f"select basecoin from relationalcoin where cryptopair='{self.get_name()}'"
        )
        if len(result) == 0:
            raise ValueError("the cryptopair doesn't exit in the database")

    @property
    def basecoin(self) -> Coin:
        """return a basecoin from a cryptopair
        ex: BNBBTC return BNB"""
        result: list[tuple[str]] = db.selectDB(
            f"select basecoin from relationalcoin where cryptopair='{self.get_name()}'"
        )

        name: str = result[0][0]
        return Coin(name)

    @property
    def quotecoin(self) -> Coin:
        """return quotecoin from a cryptopair
        ex: BNBBTC return BTC"""
        result = db.selectDB(
            "select quotecoin from relationalcoin"
            + f" where cryptopair='{self.get_name()}'"
        )

        name: str = result[0][0]
        return Coin(name)

    def is_basecoin(self, coin: Coin) -> bool:
        """return True if it iss a basecoin"""
        return self.basecoin == coin

    def is_quotecoin(self, coin: Coin) -> bool:
        """return True if it iss a quotecoin"""
        return self.quotecoin == coin

    def is_any(self, coin: Coin):
        """To see if a coin is in the cryptopair"""
        if self.is_basecoin(coin) or self.is_quotecoin(coin):
            return True
        # if not found
        raise ValueError(f"{coin.name} is not in {self.name} ")

    def replace(self, coin: Coin) -> Coin:
        """return basecoin if the given coin is quotecoin vice-versa"""
        if self.is_basecoin(coin):
            return self.quotecoin
        elif self.is_quotecoin(coin):
            return self.basecoin
        # not found in cryptopair
        raise ValueError(f"{coin.name} is not in {self.name} ")

    def get_price(self) -> float:
        """get price of a cryptopair"""
        url = TICKER_24H % (self.name)
        resp = requests.get(url)
        return float(resp.json()["lastPrice"])

    def get_price_change(self) -> float:
        """gets priceChange of a crypto pair"""
        url = TICKER_24H % (self.name)
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
        url: str = f"https://api.binance.com/api/v3/klines?symbol={self.get_name()}&interval={TIMEFRAME}"
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

        # klines.to_csv(BINANCEKLINES, index=False)
        return klines

    def __repr__(self) -> str:
        return self.name
    
    def __str__(self):
        return self.name
    def __hash__(self) -> int:
        hash(self.get_name())


"""
def get_kline(self):
    \"""{
            "e": "kline",     // Event type
            "E": 123456789,   // Event time
            "s": "BNBBTC",    // Symbol
            "k": {
            "t": 123400000, // Kline start time
            "T": 123460000, // Kline close time
            "s": "BNBBTC",  // Symbol
            "i": "1m",      // Interval
            "f": 100,       // First trade ID
            "L": 200,       // Last trade ID
            "o": "0.0010",  // Open price
            "c": "0.0020",  // Close price
            "h": "0.0025",  // High price
            "l": "0.0015",  // Low price
            "v": "1000",    // Base asset volume
            "n": 100,       // Number of trades
            "x": false,     // Is this kline closed?
            "q": "1.0000",  // Quote asset volume
            "V": "500",     // Taker buy base asset volume
            "Q": "0.500",   // Taker buy quote asset volume
            "B": "123456"   // Ignore
            }
        }

        \"""

    async def main():
        client = await AsyncClient.create()
        bm = BinanceSocketManager(client)
        # start any sockets here, i.e a trade socket
        ts = bm.kline_socket(self.name)  # .trade_socket('BNBBTC')
        # then start receiving messages
        async with ts as tscm:
            while True:
                res = await tscm.recv()
                break

        await client.close_connection()
        return res

    while True:
        try:
            loop = asyncio.get_event_loop()
            klines_list: dict[str, dict] = loop.run_until_complete(main())
            kline_data: dict[str, Union[str, int, bool]] = klines_list['k'].copy()
            break
        except asyncio.exceptions.TimeoutError:
            pass

    unwanted: list = ['T', 'q', 'n', 'V', 'Q', 'B', "i", "f", "L", "s", "x"]
    for key in unwanted:
        kline_data.pop(key)

    for kline in kline_data:
        kline['t'] = datetime.datetime.fromtimestamp(kline['t'] / 1e3)

    columns = ['date', 'open', 'close', 'high', 'low', 'volume']
    keys = list(kline_data.keys())
    klines: dict = {}

    for i in range(len(keys)):
        column = columns[i]
        key = keys[i]
        klines[column] = kline_data[key]
    # klines_pd: pd.DataFrame = pd.DataFrame(klines_list)  # changer en dataframe
    # klines_pd.columns = ['date', 'open', 'high', 'low','close', 'volume']  # renommer les colonnes
    crypto_klines: dict[str, dict[str, Union[str, datetime.datetime]]] = {self.name: klines}
    return crypto_klines
    
"""


class Coin:
    """
    Representation of a Coin

    ex: BNB
    """

    def __init__(self, name) -> None:

        self.name: str = name
        self.verify()

    def __repr__(self):
        return f"{self.name}({self.fullname})"

    def get_name(self):
        """return self.name"""
        return self.name

    def verify(self):
        """verify if the given coin name exists in database"""
        result = db.selectDB(
            requete="select fullname from Coin where shortname='"
            + self.get_name()
            + "'"
        )
        if len(result) == 0:
            raise ValueError("the coin doens't exist in the database")

    @property
    def fullname(self):
        """fullname getter"""
        return db.selectDB(
            requete="select fullname from Coin where shortname='"
            + self.get_name()
            + "'"
        )[0][0]

    def get_cryptopair_related(self) -> list[CryptoPair]:
        """return all coins related cryptopair
        where the coin appears to be a quotecoin
         or basecoin"""
        coin_name = self.get_name()
        cryptopairs_name: list[tuple[str]] = db.selectDB(
            requete="select cryptopair from relationalcoin where basecoin ='"
            + coin_name
            + "' or quotecoin ='"
            + coin_name
            + "' "
        )
        return [CryptoPair(cryptopair_name[0]) for cryptopair_name in cryptopairs_name]

    def __add__(self, other: object) -> CryptoPair:
        return CryptoPair(self.name + other.name)

    @staticmethod
    def get_all_coins():
        result:list[tuple[str]] =  db.selectDB(requete="select shortname from Coin")
        return [Coin(name[0]) for name in result]