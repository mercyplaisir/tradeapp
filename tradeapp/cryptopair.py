"""
represent pair
"""
import io
from typing import Dict, List, Protocol, Any, Self
import pathlib

import ccxt
import pandas as pd
import numpy as np
import mplfinance as mpf



from tradeapp.tools import Signal
from tradeapp.tools import Timeframe
from tradeapp.tools import Trend
from tradeapp.tools import OrderType


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

    def __init__(self, exchange: ccxt.Exchange, symbol:str) -> None:
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
                "quoteAssetPrecision": "8",
                "quoteCommissionPrecision": "8"
            }
        """
        assert symbol, "symbol name not provided"
        self.exchange = exchange
        self.symbol = symbol
        self._generate_data()

    def _check(self):
        if not self.exchange.symbols:
            self.exchange.load_markets(True)
        cond = self.symbol in self.exchange.symbols
        assert cond, "symbol not available in the exchange try another one"
    def _generate_data(self):
        self._check()
        data = self.exchange.market(symbol= self.symbol)['info']
        for key in data:
            setattr(self,key,data[key])
        

    @property
    def trend(self):
        """return the trend

        Returns:
            Trend ( object): the trend object
        """
        return self.get_trend()

    def get_base_asset(self):
        """return the base asset as crpto object

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
            symbol=self.symbol(),
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
            symbol=self.symbol(),
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

    
    def __str__(self) -> str:
        return f"looking at {self.symbol()} \n "

    def get_support_and_resistance(
        self, timeframe: Timeframe = Timeframe.DAY, s_r:bool = True
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

        # a list to store resistance and support levels
        levels = []
        # to make sure the new level area does not exist already
        def is_far_from_level(value, levels, df):
            ave = np.mean(df["High"] - df["Low"])
            return np.sum([abs(value - level) < ave for  level in levels]) == 0

        high_low = {"resistances": [], "supports": []}
        for i in range(2, df.shape[0] - 2):
            if is_support(df, i):
                low = df["Low"][i]

                if is_far_from_level(low, levels, df):
                    levels.append( low)
                    high_low["supports"].append(low)
            elif is_resistance(df, i):
                high = df["High"][i]
                if is_far_from_level(high, levels, df):
                    levels.append( high)
                    high_low["resistances"].append(high)
        if not s_r:
            return levels
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
    
    def generate_image(self):
        data = self.get_ohlc()
        levels = self.get_support_and_resistance(s_r=False)
        #print([True for ind in data.index if ind in [l[0] for l in levels]].count(False))
        path = pathlib.Path("./graph.png")
        buf = io.BytesIO()
        kwargs = dict(type='candle',mav=(50,200),volume=True,figratio=(20,8),figscale=0.8,savefig=dict(fname=buf,dpi=500,pad_inches=1000))

        # levels_plot = mpf.make_addplot(levels,color='#606060')
        
        mpf.plot(data.iloc[:,-10:],**kwargs,style='binance',hlines= levels)
        buf.seek(0)
        return buf


    