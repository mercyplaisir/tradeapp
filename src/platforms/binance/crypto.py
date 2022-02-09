import asyncio
import datetime
from dataclasses import dataclass
from typing import Union

import requests
from binance import AsyncClient, BinanceSocketManager

from src.platforms.binance.coin import Coin
from src.dbcontroller.mysqlDB import mysqlDB


@dataclass
class CryptoPair(object):
    """
    a representation of a cryptopair
    ex: BNBBTC
    """
    name: str
    database = mysqlDB()

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
        return self.is_basecoin(coin) or self.is_quotecoin(coin)

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

    def get_kline(self):
        """{
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

            """

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
    def get_klines(self, cryptopair: CryptoPair, interval: str = "2 days"):
           
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
           
            klines_list = self.client.get_historical_klines(
                cryptopair, self.TIMEFRAME, f"{interval} ago UTC")
    
            # changer timestamp en date
            for kline in klines_list:
                kline[0] = datetime.datetime.fromtimestamp(kline[0] / 1e3)
    
            klines = pd.DataFrame(klines_list)  # changer en dataframe
            # supprimer les collonnes qui ne sont pas necessaires
            klines.drop(columns=[6, 7, 8, 9, 10, 11], inplace=True)
    
            klines.columns = ['date', 'open', 'high', 'low',
                              'close', 'volume']  # renommer les colonnes
            klines.to_csv(BINANCEKLINES, index=False)
            # return klines
            # print(">>>klines telecharger")
        """
