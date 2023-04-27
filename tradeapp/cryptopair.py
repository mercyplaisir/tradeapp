"""
represent pair
"""
from typing import Dict, List, Protocol, Any, Self
import ccxt

import pandas as pd
import numpy as np


from .tools import Signal
from .tools import Timeframe
from .tools import Trend
from .tools import OrderType


class Crypto:
    def __init__(self, name: str, ex: ccxt.Exchange) -> None:
        self.name = name
        self.ex = ex

    def __str__(self) -> str:
        return f"{self.name}"

    @property
    def balance(self) -> float | int:
        return self._balance()[0]

    @property
    def locked(self) -> float | int:
        pass

    @property
    def total(self) -> float | int:
        pass

    def _balance(self):
        data: Dict[str, float | int] = self.get_balance()
        free, used, total = data.values()
        return free, used, total

    def get_balance(self) -> Dict:
        return self.ex.fetch_balance(currency=self.name)


class CryptoPair:
    """
    represent a crypto Pair
    ex:'BTCUSDT' - BTC/USDT
    base currency ↓
                BTC / USDT
                ETH / BTC
                DASH / ETH
                        ↑ quote currency
    """

    def __init__(self, exchange: ccxt.Exchange, kwargs: Dict) -> None:
        """
        Args:
            details (Dict):
            {   "symbol": "ETHBTC",
                "status": "TRADING",
                "baseAsset": "ETH",
                "baseAssetPrecision": "8",
                "quoteAsset": "BTC",
                "quotePrecision": "8",
                "quoteAssetPrecision": "8",
                "baseCommissionPrecision": "8",
                "quoteCommissionPrecision": "8"
            }
        """
        assert kwargs["symbol"], "symbol name not provided"
        assert kwargs["status"] == "TRADING", f"{kwargs['symbol']} status is not trading"
        self.exchange = exchange
        self.__dict__.update(kwargs)

    @property
    def trend(self):
        """return the trend

        Returns:
            Trend ( object): the trend object
        """
        return self.get_trend()

    def get_symbol(self):
        """
        return the symbol
        Returns:
            _type_: _description_
        """
        return self.symbol

    def get_base_asset(self):
        """return the base asset as crpto object

        Returns:
            _type_: _description_
        """
        return Crypto(self.baseAsset, ex=self.exchange)

    def get_quoteAsset(self):
        """return the quote asset as Crypto object"""
        return Crypto(self.quoteAsset, ex=self.exchange)

    def buy_order(self) -> None:
        """buy order

        Returns:
            Dict[str, str]: order details
        """
        amount = self.get_quoteAsset().balance / self.get_price()

        order_data = self.exchange.create_order(
            symbol=self.get_symbol(),
            type=OrderType.MARKET,
            side=Signal.BUY,
            amount=round(amount, self.baseAssetPrecision),
        )
        return order_data

    def sell_order(self) -> None:
        """sell ordPer

        Returns:
            Dict[str, str]: order details
        """
        balance = self.get_base_asset().balance
        order_data = self.exchange.create_order(
            symbol=self.get_symbol(),
            type=OrderType.MARKET,
            side=Signal.SELL,
            amount=round(balance, self.quoteAssetPrecision),
        )
        return order_data

    def get_ohlc(self, timeframe=Timeframe.DAY):
        """
        getting price data
        """
        data = self.exchange.fetch_ohlcv(
            symbol=f"{self.get_base_asset()}/{self.get_quoteAsset()}",
            timeframe=timeframe,
        )
        data = pd.DataFrame(
            data, columns=["Time", "Open", "High", "Low", "Close", "Volume"]
        )
        data["Time"] = pd.to_datetime(data["Time"], unit="ms")
        # change index to time column
        data = data.set_index("Time")
        return data

    @classmethod
    def load_cryptopair_from(cls, data: Dict[ccxt.Exchange, List[dict]]):
        """create Cryptopairs instance using list of data given

        Args:
            data (List[dict]): _description_

        Returns:
            _type_: _description_
        """
        assert len(data) > 0, "data can't be empty"
        exchange = list(data.keys())[0]
        return [CryptoPair(kwargs=d) for d in data.values()]

    def __str__(self) -> str:
        return f"looking at {self.get_symbol()} \n "

    def get_support_and_resistance(
        self, timeframe=Timeframe.DAY
    ) -> Dict[str, List[float | int]]:
        """return resistance and support on given data

        Args:
            df (pd.DataFrame): contains ohlc of given crypto
        """
        # method 1: fractal candlestick pattern
        # determine bullish fractal
        df: pd.DataFrame = self.get_ohlc(timeframe=timeframe)

        def is_support(df, i):
            cond1 = df["Low"][i] < df["Low"][i - 1]
            cond2 = df["Low"][i] < df["Low"][i + 1]
            cond3 = df["Low"][i + 1] < df["Low"][i + 2]
            cond4 = df["Low"][i - 1] < df["Low"][i - 2]
            return cond1 and cond2 and cond3 and cond4

        # determine bearish fractal
        def is_resistance(df, i):
            cond1 = df["High"][i] > df["High"][i - 1]
            cond2 = df["High"][i] > df["High"][i + 1]
            cond3 = df["High"][i + 1] > df["High"][i + 2]
            cond4 = df["High"][i - 1] > df["High"][i - 2]
            return cond1 and cond2 and cond3 and cond4

        # to make sure the new level area does not exist already
        def is_far_from_level(value, levels, df):
            ave = np.mean(df["High"] - df["Low"])
            return np.sum([abs(value - level) < ave for _, level in levels]) == 0

        # a list to store resistance and support levels
        levels = []
        high_low = {"resistances": [], "supports": []}
        for i in range(2, df.shape[0] - 2):
            if is_support(df, i):
                low = df["Low"][i]

                if is_far_from_level(low, levels, df):
                    levels.append((i, low))
                    high_low["supports"].append(low)
            elif is_resistance(df, i):
                high = df["High"][i]
                if is_far_from_level(high, levels, df):
                    levels.append((i, high))
                    high_low["resistances"].append(high)
        return high_low

    def get_trend(self, timeframe=Timeframe.DAY) -> Trend:
        """give the trend of the current stock

        Args:
            df (pd.DataFrame): contains ohlc data of given crypto
        """
        # data
        df = self.get_ohlc(timeframe=timeframe)
        sma_size = 200
        # Get the trend of the market by using sma200
        # Get list of 5 last closed price
        price: List[float] = df["Close"][-5:].to_list()
        # calculate sma
        df[f"SMA_{sma_size}"] = df["Close"].rolling(window=sma_size).mean()
        sma_value: List[float] = df[f"SMA_{sma_size}"][-5:].to_list()
        # condition
        cond = price > sma_value
        if cond:
            return Trend.UPTREND
        return Trend.DOWNTREND

    